import subprocess
from os import path

CURRENT_DIR = path.dirname(path.realpath(__file__))
PROJECT_ROOT = path.normpath(path.join(CURRENT_DIR, '../'))
SRC_DIR = path.join(PROJECT_ROOT, 'src/')

if __name__ == '__main__':
    subprocess.run(['python', '-m', 'unittest'], cwd=SRC_DIR)
