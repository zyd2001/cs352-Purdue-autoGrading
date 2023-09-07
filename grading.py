#!/usr/bin/env python3

import os, sys
import subprocess
from datetime import datetime

os.chdir(sys.argv[1])

cwd = os.getcwd()

zips = os.listdir()

# unzip all files from brightspace
for z in zips:
    if '.zip' in z:
        subprocess.run(["unzip", "-o", z])


# only keep most recent submission
submissions = {}

for d in os.listdir():
    if os.path.isdir(d):
        parts = d.split(' - ')
        name = parts[1].split()[0].strip()
        if name in submissions:
            time = datetime.strptime(parts[2].strip(), "%b %d, %Y %H%M")
            if submissions[name]["time"] < time:
                subprocess.run(["rm", "-rf", submissions[name]['dir']])
                submissions[name] = {"time": datetime.strptime(parts[2].strip(), "%b %d, %Y %H%M"), "dir" : d}
            else:
                subprocess.run(["rm", "-rf", d])
        else:
            submissions[name] = {"time": datetime.strptime(parts[2].strip(), "%b %d, %Y %H%M"), "dir" : d}

processes = []

for d in os.listdir():
    if os.path.isdir(d):
        os.chdir(d)
        logFile = open('log', "w")
        p = subprocess.Popen(["../../{}Grading.sh".format(sys.argv[1]), d], stdout=logFile, stderr=logFile)
        print('start {}'.format(d))
        processes.append(p)
        os.chdir('..')

for p in processes:
    p.wait()

output = open("result.csv", "w")

# collect result
for d in os.listdir():
    if os.path.isdir(d):
        os.chdir(d)
        parts = d.split(' - ')
        name = parts[1].split()[0].strip()
        print('collecting result for {}'.format(name))
        res = subprocess.run(['tail', '-n', '3', 'log'], stdout=subprocess.PIPE, universal_newlines=True)
        result = [x for x in res.stdout.split('\n') if x]
        output.write(name)
        output.write(',')
        if result[1] == 'OK':
            num = int(result[0].split()[1])
            output.write('{},{},{}%\n'.format(num, num, 100))
        elif 'FAILED' in result[1]:
            num = int(result[0].split()[1])
            failed = int(result[1].split('=')[1].strip(')'))
            output.write('{},{},{}%\n'.format(num - failed, num, (num - failed) / num * 100))
        else:
            print('Error {}'.format(name))
            output.write('Error\n')
        os.chdir('..')

