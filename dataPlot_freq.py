#!/usr/local/bin/python3
import os
import re
import matplotlib.pyplot as plt
from matplotlib import pylab
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
            match = re.match("(.*?)_(\w+)_([-\d\.]+)_([-\d\.]+)V_([\d\.]+)Hz_([\d\.]+).DTA", name)
            
            if match:
                print(match.groups())
                sample = match.group(2)
                voltage = float(match.group(3))
                voltageTo = float(match.group(4))
                appliedFreq = float(match.group(5))
                # define key
                key = sample, voltage, voltageTo, appliedFreq
                if key not in timesMap:
                    timesMap[key] = []
                    coulsMap[key] = []
                print(sample, voltage, voltageTo, appliedFreq)
                
                print(os.path.join(path, name))
                filenames = os.path.join(path, name)
                print(filenames)
                # open the file
                fid = open(filenames, "r", encoding='ISO-8859-1')
                # print fid.readlines()
                # store data lines as a variable
                rawLines = fid.readlines()
                lineToRead = 999999999
                for i in range(len(rawLines)):
                    line = rawLines[i]
                    if line.startswith("CURVE"):
                        lineToRead = i + 3
                    if i > lineToRead:
                        splitted = line.split()
                        timesMap[key].append(float(splitted[1]))
                        coulsMap[key].append(float(splitted[2]))
            else:
                print("Not matched!")

# key = sample, voltage, voltageTo, appliedFreq
#plt.subplot(331)
for key in timesMap.keys():
    if key[0] == 'metalW' and key[1] == 0.2 and key[2] == 0.4 and key[3] == 1:
	    print(key)
        #label='y = %.2f x + %.2f' %(A, B)
	    plt.plot((timesMap[key], coulsMap[key]), linewidth=2.0, label='%s_%.1f V_%.1f V_%.1f Hz' %(key[0],key[1],key[2], key[3]))

legend = plt.legend(loc='lower left',shadow=True)


plt.xlim((0, 4))
#plt.ylim((-0.00006, 0.00005))
plt.xlabel('Time (s)')
plt.ylabel('Charge (C)')
plt.show()