# Nginx Configuration
upstream backend {
    server {{UPSTREAM_HOST}}:{{UPSTREAM_PORT}};
}
server {
    server_name {{SERVER_NAME}};
    access_log {{LOG_PATH}};
    root {{ROOT_PATH}};
    proxy_pass http://backend;
}
