#!/usr/bin/python
# list all .DTA files in Jul folder
import os
import re
import csv


# define map here -- use key to look for certain list
pHMap = {}

for path, subdirs, files in os.walk("."):
    print("Path: ", path)
    for name in files:
        # print "First: ", name
        if name.endswith(".txt"):
            # use regular expression to extract parameters in filename
            print(name)
            match = re.match("([^\d\W]+)([\d\.]+).txt", name)

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
                    readLine = rawLines[-1]
                    splitted = readLine.split()
                    pHMap[key].append(splitted[2])

            else:
                print("Not matched!")

# key = sample, voltage, numSample
t = []
with open('pt.csv', 'a') as f:
    for key in pHMap.keys():
        if key[0] == 'Pt':
            t.append((float(key[1]),float(pHMap[key][0])))
    a = csv.writer(f, delimiter='\t')
    a.writerows(t)

        