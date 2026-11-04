"""Probe only this Compose project; preserve receipts and keep the service running."""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import hashlib
import json
import subprocess
import time
from urllib.request import urlopen
from urllib.error import HTTPError

ROOT = Path(__file__).resolve().parents[1]


def run(*args):
    return subprocess.check_output(args, cwd=ROOT, text=True, encoding='utf8', stderr=subprocess.STDOUT).strip()


def inspect():
    cid = run('docker', 'compose', 'ps', '-q', 'web')
    return json.loads(run('docker', 'inspect', cid))[0]


def ready():
    for _ in range(45):
        state = inspect()
        if state['State'].get('Health', {}).get('Status') == 'healthy':
            return state
        time.sleep(1)
    raise AssertionError('Container did not become healthy in 45 seconds')


def main(output, exercise_restart):
    if output.exists():
        raise ValueError('Refusing to overwrite previous Docker receipt')
    from check_release import object_manifest,required_inputs
    initial_files=object_manifest()
    initial_inputs={name:initial_files[name] for name in required_inputs('docker',initial_files)}
    checks = []
    def need(ok, name):
        checks.append({'check': name, 'pass': bool(ok)})
        if not ok:
            raise AssertionError(name)
    result = {'checked_at': datetime.now(timezone.utc).isoformat(), 'checks': checks}
    try:
        before = ready()
        host = before['HostConfig']
        need(before['Config']['User'] == '101:101', 'Non-root UID/GID')
        need(host['ReadonlyRootfs'], 'Read-only root filesystem')
        need('ALL' in host['CapDrop'] and any('no-new-privileges' in s for s in host['SecurityOpt']), 'Dropped capabilities / no new privileges')
        need(host['PortBindings']['8080/tcp'][0]['HostIp'] == '127.0.0.1', 'Loopback binding')
        need(host['RestartPolicy']['Name'] == 'unless-stopped', 'Restart policy')
        need(host['Memory'] == 128 * 1024 ** 2 and host['PidsLimit'] == 64, 'Resource bounds')
        need(run('docker', 'compose', 'exec', '-T', 'web', 'id', '-u') == '101', 'Effective process UID')
        for name in ['index.html', 'app.js', 'styles.css', 'data/knowledge.json', 'data/context.txt', 'assets/brand/heuristik-mark.svg']:
            with urlopen('http://127.0.0.1:4173/' + name, timeout=5) as response:
                body = response.read()
                need(response.status == 200 and body == (ROOT / name).read_bytes(), 'HTTP / bytes ' + name)
        with urlopen('http://127.0.0.1:4173/healthz', timeout=5) as response:
            need(response.read() == b'ok\n', 'Health HTTP response')
        try:
            urlopen('http://127.0.0.1:4173/unknown-heuristik-test-path', timeout=5)
            need(False, 'Unknown path rejected')
        except HTTPError as exc:
            need(exc.code == 404, 'Unknown path rejected')
        if exercise_restart:
            stopped=subprocess.run(['docker','compose','exec','-T','web','sh','-c','kill -TERM 1'],cwd=ROOT,capture_output=True)
            result['process_exit_probe_returncode']=stopped.returncode
            time.sleep(2)
            after = ready()
            need(after['Id'] == before['Id'] and after['RestartCount'] > before['RestartCount'], 'Automatic recovery after own process exit')
            run('docker', 'compose', 'up', '-d', '--force-recreate', 'web')
            recreated = ready()
            need(recreated['Id'] != before['Id'], 'Own service recreated')
            with urlopen('http://127.0.0.1:4173/data/knowledge.json', timeout=5) as response:
                need(response.read() == (ROOT/'data/knowledge.json').read_bytes(), 'Knowledge persists across recreation')
        current = inspect()
        current_files=object_manifest()
        need(all(current_files.get(name)==sha for name,sha in initial_inputs.items()),'Tested Docker inputs unchanged')
        result['tested_files']=initial_inputs
        result.update(status='PASS', image=current['Image'], health=current['State']['Health']['Status'], restart_count=current['RestartCount'], nginx=run('docker','compose','exec','-T','web','nginx','-v'), scope='Local image/HTTP/content, constraints and optional process-exit/recreation. Not host reboot, frozen-process auto-heal, Pages or human acceptance.')
    except Exception as exc:
        result.update(status='FAIL', error=str(exc))
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf8', newline='\n')
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(result['status'] != 'PASS')


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--out', type=Path, required=True)
    ap.add_argument('--exercise-restart', action='store_true')
    args = ap.parse_args()
    main(args.out, args.exercise_restart)
