import subprocess
from os import path


CURRENT_DIR = path.dirname(path.realpath(__file__))
PROJECT_ROOT = path.normpath(path.join(CURRENT_DIR, '../'))
BUILD_DIR = path.join(PROJECT_ROOT, 'build/')
SRC_DIR = path.join(PROJECT_ROOT, 'src/')

def build():
    print("Building zip...")
    function_zip_file = path.join(BUILD_DIR, 'function.zip')
    ocgull_file = path.join(SRC_DIR, 'ocgull.py')
    subprocess.run(['zip', '-j', '-r', function_zip_file, ocgull_file])

def deploy():
    print("Deploying to AWS lambda...")
    subprocess.run(['aws', 'lambda', 'update-function-code',
            '--function-name', 'ocgull',
            '--zip-file', 'fileb://build/function.zip'])


if __name__ == '__main__':
    build()
    deploy()
