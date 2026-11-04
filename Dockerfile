# Stable Alpine multi-architecture manifest resolved from Docker Hub, 2026-11-04.
FROM nginxinc/nginx-unprivileged:stable-alpine@sha256:f5116ed4606f3eb015dd4a8e28cb9b351476dc0ad4bc6e9f93b19cec130cdf03
LABEL org.opencontainers.image.title="Heuristik Space" org.opencontainers.image.source="https://github.com/rabelojunior81-collab/heuristik-space"
COPY deploy/nginx.conf /etc/nginx/nginx.conf
COPY index.html app.js styles.css 404.html /usr/share/nginx/html/
COPY assets/ /usr/share/nginx/html/assets/
COPY data/ /usr/share/nginx/html/data/
COPY docs/GOVERNANCE.md docs/ASSETS.md docs/ASSETS.json docs/RESEARCH.md docs/ARCHITECTURE.md docs/OPERATIONS.md /usr/share/nginx/html/docs/
USER 101:101
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 CMD wget -q -O /dev/null http://127.0.0.1:8080/healthz || exit 1
ENTRYPOINT ["nginx"]
CMD ["-g", "daemon off;"]
