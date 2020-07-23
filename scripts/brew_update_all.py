#!/usr/local/bin/python

import subprocess
subprocess.call("brew update", shell=True)
map(lambda x:subprocess.call("brew upgrade " + x, shell=True),
    subprocess.check_output('brew outdated', shell=True).split())
