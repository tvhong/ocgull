import subprocess
import sys
from os import path

from infra.settings import SRC_DIR

if __name__ == '__main__':
    subprocess.run(['python', '-m', 'unittest', *sys.argv[1:]],
            cwd=path.join(SRC_DIR))
