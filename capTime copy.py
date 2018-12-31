#!/usr/bin/python
# list all .DTA files in Jul folder
import os
import re
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


# define map here -- use key to look for certain list
timesMap = {}
coulsMap = {}

for path, subdirs, files in os.walk("."):
    hzToPoint = {}
    print("Path: ", path)
    for name in files:
        # print "First: ", name
        if name.endswith(".DTA") and name.startswith("CC"):
            # use regular expression to extract parameters in filename
            print(name)
            match = re.match("(.*?)_(\w+)_([-\d\.]+)_([\d\.]+).DTA", name)

            if match:
                print(match.groups())
                sample = match.group(2)
                voltage = match.group(3)
                numSample = match.group(4)
                # define key
                key = sample, voltage, numSample
                print(key)
                if key not in coulsMap:
                    coulsMap[key] = []
                    timesMap[key] = []
                    print(os.path.join(path, name))
                    filenames = os.path.join(path, name)
                    print(filenames)
                    # open the file
                    fid = open(filenames, "r")
                    # print fid.readlines()
                    # store data lines as a variable
                    rawLines = fid.readlines()
                    lineToRead = 999999999
                    for i in range(len(rawLines)):
                        line = rawLines[i]
                        if line.startswith("CURVE"):
                            lineToRead = i + 3
                        if i > lineToRead and i < 5558:
                            splitted = line.split()
                            timesMap[key].append(float(splitted[1]))
                            coulsMap[key].append(float(splitted[2]))
            else:
                print("Not matched!")

# key = sample, voltage, numSample
for key in timesMap.keys():
    if key[0] == 'metalW' and key[2] == '3':
        print(key)
        #label='y = %.2f x + %.2f' %(A, B)
        plt.plot(timesMap[key], coulsMap[key], linewidth=2.0, label='%s_%.1fV_%s' %(key[0],float(key[1]),key[2]))
        legend = plt.legend(loc='upper left', shadow=True)

plt.xlabel('Time (s)')
plt.ylabel('Charge (C)')
plt.show()