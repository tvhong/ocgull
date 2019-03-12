import subprocess

from settings import SRC_DIR

if __name__ == '__main__':
    subprocess.run(['python', '-m', 'unittest'], cwd=SRC_DIR)
