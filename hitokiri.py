#!/usr/bin/python
import re
import sys
import os
import json

VER = 'v0.1'
BASEDIR = os.path.dirname(os.path.realpath(__file__))
DIR = BASEDIR + os.sep + 'atks' + os.sep


def exit(message, code=1):
    print('{}'.format(message))
    sys.exit(code)


def run(config):
    with open(config[0], 'r') as f:
        ln = 1
        for line in f:
            for atk in config[1]['attacks']:
                p = re.compile(atk['pattern'])
                if not p.search(line):
                    continue
                print('{}:{}: Possible {}'.format(
                    config[0],
                    ln,
                    atk['name']
                ))
            ln = ln + 1


def load_config(path):
    fext = os.path.splitext(path)[1]
    fext = fext[1:]
    if not fext:
        exit('hitokiri: invalid input file')
    if not os.path.exists(path):
        exit('hitokiri: input file doesn\'t exist')
    try:
        with open('{}{}.json'.format(DIR, fext)) as f:
            return path, json.loads(f.read())
    except FileNotFoundError:
        exit('hitokiri: {}.json not found'.format(fext))
    except Exception:
        exit('hitokiri: error occurred while opening config file')


def main():
    if len(sys.argv) != 2:
        exit("hitokiri: try 'hitokiri -h' for more information")
    if sys.argv[1] == '-h':
        exit('Usage: \n hitokiri <options>\n hitokiri <file>'
             '\n\n -v\t\tVersion number'
             '\n -h\t\tThis help', 0)
    elif sys.argv[1] == '-v':
        exit('Hitokiri {}'.format(VER), 0)
    run(load_config(sys.argv[1]))


if __name__ == "__main__":
    main()
