"""Create an isolated browser fixture using unchanged app code and explicit mocks.
Never included in the Pages/Docker allowlists. No installation or external call.
"""
from pathlib import Path
import argparse
import shutil

ROOT = Path(__file__).resolve().parents[1]
MOCKS = r'''
const qaMode=new URL(location.href).searchParams.get('fixture');
let qaSourceFailure=qaMode==='source-error';
if(qaMode==='clipboard')Object.defineProperty(navigator,'clipboard',{
  configurable:true,value:{writeText:async()=>{throw Error('Controlled clipboard denial');}}
});
const originalFetch=window.fetch.bind(window);
window.fetch=async(input,...args)=>{
  const url=String(input);
  if(qaMode==='data-error'&&url.includes('knowledge.json'))throw Error('Controlled data failure');
  if(qaSourceFailure&&url.includes('data/articles/'))throw Error('Controlled source failure');
  const response=await originalFetch(input,...args);
  if(qaMode==='hostile'&&url.includes('knowledge.json')){
    const data=await response.json();
    data.nodes[0].title='<img src=x onerror="document.documentElement.dataset.qaXss=1">';
    data.nodes[0].summary='<script>document.documentElement.dataset.qaXss=2</script>';
    data.references[0].url='javascript:document.documentElement.dataset.qaXss=3';
    return new Response(JSON.stringify(data),{status:200,headers:{'Content-Type':'application/json'}});
  }
  return response;
};
addEventListener('DOMContentLoaded',()=>{
 const button=document.createElement('button');button.id='fixture-recover';
 button.textContent='QA: recuperar transporte da fonte';
 button.style.cssText='position:fixed;right:0;top:90px;z-index:100;color:white;background:black';
 button.onclick=()=>{qaSourceFailure=false;button.textContent='QA: transporte recuperado';};
 document.body.append(button);
});
'''


def main(output):
    if output.exists():
        raise ValueError('Fixture directory exists; preserve it and choose another')
    output.mkdir(parents=True)
    for name in ['app.js', 'styles.css']:
        shutil.copy2(ROOT / name, output / name)
    for name in ['data', 'assets']:
        shutil.copytree(ROOT / name, output / name)
    index = (ROOT / 'index.html').read_text(encoding='utf8')
    index = index.replace('<script type="module" src="app.js">',
                          '<script src="qa-mocks.js"></script><script type="module" src="app.js">')
    (output / 'index.html').write_text(index, encoding='utf8', newline='\n')
    (output / 'qa-mocks.js').write_text(MOCKS, encoding='utf8', newline='\n')
    print('Fixture created:', output, 'app.js unchanged; transport mocks explicit')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    main(parser.parse_args().out)
