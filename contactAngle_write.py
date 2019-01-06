#!/usr/bin/python
# list all .DTA files in Jul folder
import os
import re
import csv


# define map here -- use key to look for certain list
pHMap = {}

for path, subdirs, files in os.walk("../ContactAngle"):
    print("Path: ", path)
    for name in files:
        # print "First: ", name
        if name.endswith(".txt"):
            # use regular expression to extract parameters in filename
            print(name)
            match = re.match("([a-zA-Z]+)_?([\d\.]+).txt", name)

            if match:
                print(match.groups())
                sample = match.group(1)
                pH = match.group(2)
                
                # define key
                key = sample, pH
                print(key)
                if key not in pHMap:
                    pHMap[key] = []
                    print(os.path.join(path, name))
                    filenames = os.path.join(path, name)
                    print(filenames)
                    # open the file
                    fid = open(filenames, "r")
                    # print fid.readlines()
                    # store data lines as a variable
                    rawLines = fid.readlines()
                    for i in range(1,5):
                        readLine = rawLines[-i]
                        splitted = readLine.split()
                        pHMap[key].append(splitted[2])
                    print(pHMap[key])

            else:
                print("Not matched!")

# key = sample, voltage, numSample

with open('../ContactAngle/Pt.csv', 'w') as f:
    for key in pHMap.keys():
        if key[0] == 'Pt':
            t = []
            t.append(float(key[1]))
            for i in range(4):
                t.append(float(pHMap[key][i]))
            print(t)
            a = csv.writer(f, delimiter='\t')
            a.writerow(t)
with open('../ContactAngle/fW.csv', 'w') as f:
    for key in pHMap.keys():
        if key[0] == 'fW':
            t = []
            t.append(float(key[1]))
            for i in range(4):
                t.append(float(pHMap[key][i]))
            print(t)
            a = csv.writer(f, delimiter='\t')
            a.writerow(t)
with open('../ContactAngle/mW.csv', 'w') as f:
    for key in pHMap.keys():
        if key[0] == 'mW':
            t = []
            t.append(float(key[1]))
            for i in range(4):
                t.append(float(pHMap[key][i]))
            print(t)
            a = csv.writer(f, delimiter='\t')
            a.writerow(t)