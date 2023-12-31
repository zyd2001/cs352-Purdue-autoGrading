#!/usr/bin/env python3

import os, sys
import subprocess
from datetime import datetime
import pandas
import re

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
            time = datetime.strptime(parts[2].strip(), "%b %d, %Y %I:%M %p")
            if submissions[name]["time"] < time:
                subprocess.run(["rm", "-rf", submissions[name]['dir']])
                submissions[name] = {"time": datetime.strptime(parts[2].strip(), "%b %d, %Y %I:%M %p"), "dir" : d}
            else:
                subprocess.run(["rm", "-rf", d])
        else:
            submissions[name] = {"time": datetime.strptime(parts[2].strip(), "%b %d, %Y %I:%M %p"), "dir" : d}

processes = []

for d in os.listdir():
    if os.path.isdir(d):
        os.chdir(d)
        logFile = open('log', "w")
        p = subprocess.Popen(["../grading.sh".format(sys.argv[1]), d], stdout=logFile, stderr=logFile)
        print('start {}'.format(d))
        processes.append(p)
        os.chdir('..')

for p in processes:
    p.wait()

output = open("result.csv", "w")
outputForImport = open("resultForImport.csv", "w")
output.write("FullName,ID,correct,all,percent\n")
outputForImport.write("Username,,End-of-Line Indicator\n")

# collect result
for d in os.listdir():
    if os.path.isdir(d):
        os.chdir(d)
        parts = d.split(' - ')
        id = parts[1].split()[0].strip()
        fullName = parts[1].replace(id, '').strip()
        print('collecting result for {}'.format(id))
        res = subprocess.run(['tail', '-n', '3', 'log'], stdout=subprocess.PIPE, universal_newlines=True)
        result = [x for x in res.stdout.split('\n') if x]
        if result[1] == 'OK':
            output.write("{},{},".format(fullName, id))
            outputForImport.write("#{},".format(id))
            num = int(result[0].split()[1])
            output.write('{},{},{}\n'.format(num, num, 100))
            outputForImport.write('100,#\n')
        elif 'FAILED' in result[1]:
            output.write("{},{},".format(fullName, id))
            outputForImport.write("#{},".format(id))
            num = int(result[0].split()[1])
            failed = 0
            failures = re.search('failures=\d+', result[1])
            errors = re.search('errors=\d+', result[1])
            if failures:
                failed += int(failures.group().split('=')[-1])
            if errors:
                failed += int(errors.group().split('=')[-1])
            output.write('{},{},{}\n'.format(num - failed, num, (num - failed) / num * 100))
            outputForImport.write('{},#\n'.format((num - failed) / num * 100))
        else:
            print('Error {}'.format(id))
            # output.write('-1,-1,0\n')
            # outputForImport.write('0,#\n')
        os.chdir('..')

output.close()

# get JSON for browser script
df = pandas.read_csv("result.csv", index_col='FullName', dtype={'correct': 'Int32', 'all': 'Int32'})
df.to_json('result.json', orient='index', indent=4)
