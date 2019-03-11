import subprocess
import sys
from os import path

from settings import BUILD_DIR, PACKAGE_DIR, SRC_DIR


def run_command(params, **kwargs):
    print("[cmd] {}".format(' '.join(params)))
    if kwargs:
        print("[cmd_kwargs] {}".format(kwargs))

    subprocess.run(params, **kwargs)

def build(pip_download):
    if pip_download:
        print("Downloading packages...")
        run_command(['pip', 'install', '-q', '-r', 'requirements.txt', '--target', PACKAGE_DIR])

    function_zip_file = path.join(BUILD_DIR, 'function.zip')
    print("Adding package to zip...")
    run_command(['zip', '-q', '-r', function_zip_file, '.'], cwd=PACKAGE_DIR)

    print("Adding src to zip...")
    run_command(['zip', '-g', '-r', function_zip_file, '.', '-i', '*.py'], cwd=SRC_DIR)

def deploy():
    print("Deploying to AWS lambda...")
    run_command(['aws', 'lambda', 'update-function-code',
            '--function-name', 'ocgull',
            '--zip-file', 'fileb://build/function.zip'])


if __name__ == '__main__':
    pip_download = True if '-pip' in sys.argv else False
    build(pip_download)
    deploy()
