import subprocess
from os import path

CURRENT_DIR = path.dirname(path.realpath(__file__))
PROJECT_ROOT = path.normpath(path.join(CURRENT_DIR, '../'))
BUILD_DIR = path.join(PROJECT_ROOT, 'build/')
SRC_DIR = path.join(PROJECT_ROOT, 'src/')
PACKAGE_DIR = path.join(BUILD_DIR, 'package/')

def run_command(params, **kwargs):
    print("[cmd] {}".format(' '.join(params)))
    if kwargs:
        print("[cmd_kwargs] {}".format(kwargs))

    subprocess.run(params, **kwargs)

def build():
    # print("Downloading packages...")
    # run_command(['pip', 'install', '-r', 'requirements.txt', '--target', PACKAGE_DIR])

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
    build()
    deploy()
