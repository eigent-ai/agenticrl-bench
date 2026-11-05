import os

BASE_DIR = "/opt/deploy-tool"


def export_env(config):
    export_path = os.path.join(BASE_DIR, "scripts", "export_env.sh")
    with open(export_path, 'w') as f:
        f.write("#!/bin/bash\n")
        f.write("# Environment variables for service deployment\n\n")
        for svc_name, svc_config in config['services'].items():
            prefix = svc_name.upper().replace('-', '_')
            f.write(f"export {prefix}_HOST={svc_config['host']}\n")
            f.write(f"export {prefix}_PORT={svc_config['port']}\n")
            f.write(f"export {prefix}_DB_PASSWORD={svc_config['db_password']}\n")
            f.write(f"export {prefix}_API_KEY={svc_config['api_key']}\n")
            f.write("\n")
    os.chmod(export_path, 0o755)
