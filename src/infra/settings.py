from os import path

CURRENT_DIR = path.dirname(path.realpath(__file__))
PROJECT_ROOT = path.normpath(path.join(CURRENT_DIR, '../../'))

BUILD_DIR = path.join(PROJECT_ROOT, 'build/')
SRC_DIR = path.join(PROJECT_ROOT, 'src/')
PACKAGE_DIR = path.join(BUILD_DIR, 'package/')
