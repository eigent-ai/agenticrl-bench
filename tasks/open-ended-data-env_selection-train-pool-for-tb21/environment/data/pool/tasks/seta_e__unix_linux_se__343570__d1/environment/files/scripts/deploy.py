import subprocess
import sys

def deploy(version):
    result = subprocess.run(['./deploy.sh', version], capture_output=True)
    return result.returncode

if __name__ == '__main__':
    code = deploy(sys.argv[1] if len(sys.argv) > 1 else 'latest')
    sys.exit(code)
