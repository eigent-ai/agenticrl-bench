import subprocess
import os

SCRIPTS_DIR = "/opt/deploy-tool/scripts"


def restart_service(svc_name, svc_config):
    script_path = os.path.join(SCRIPTS_DIR, "restart_service.sh")

    cmd = [script_path, svc_name, str(svc_config['port']), svc_config['db_password']]
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    stdout, stderr = process.communicate()

    if process.returncode != 0:
        raise RuntimeError(f"Service restart failed for {svc_name}: {stderr.decode()}")

    return stdout.decode()
