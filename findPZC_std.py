# 5499  10  2.52074E-004  -1.99844E-001  2.71488E-005  0.00000E+000  -2.00000E-001  1.72460E-004  8  ...........
# 5500  10.002  2.52129E-004  -1.99974E-001  2.71688E-005  0.00000E+000  -2.00000E-001  4.72460E-004  8  ...........                
import os
import re
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import pylab
import matplotlib.patches as mpatches
# sci python
from scipy import stats

def aggregateInfos():
    coulsMap = {}
    for path, subdirs, files in os.walk("."):
        hzToPoint = {}
        print("Path: ", path)
        for name in files:
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
                    if key not in coulsMap:
                        coulsMap[key] = []

                    with open(os.path.join(path, name), "r") as fid:
                        lineToRead = 0
                        rawLines = fid.readlines()
                        for i in range(len(rawLines)):
                            line = rawLines[i]
                            if line.startswith("CURVE"):
                                lineToRead = i + 1
                            if i > lineToRead and lineToRead != 0:
                                splitted = line.split()
                                time = splitted[1]
                                if time == "10":
                                    coulsMap[key].append(float(splitted[2]))
                                    break
                else:
                    print("Not matched!")
    return coulsMap

def main():
    coulsMap = aggregateInfos()
    print(coulsMap)
    # key = sample, voltage, numSample
    posVolts = []
    posCouls = [[],[],[]]
    negVolts = []
    negCouls = [[],[],[]]

  #for key in coulsMap.keys():
    for (sample, voltage, numSample), couls in coulsMap.items(): # map key and value together
        
        if sample == 'Pt' and numSample == '1':
            if couls[0] > 0:
                posVolts.append(float(voltage))
                posCouls[0].append(float(couls[0]))
            else:
                negVolts.append(float(voltage))
                negCouls[0].append(-float(couls[0]))

        if sample == 'Pt' and numSample == '2':
            if couls[0] > 0:
                posCouls[1].append(float(couls[0]))
            else:
                negCouls[1].append(-float(couls[0]))
        if sample == 'Pt' and numSample == '3':
            if couls[0] > 0:
                posCouls[2].append(float(couls[0]))
            else:
                negCouls[2].append(-float(couls[0]))

    print(posCouls)
    print(negCouls)
    arrPosCoul = np.array([posCouls[0], posCouls[1], posCouls[2]])
    
    #arrPosCoul = arrPosCoul * 1000000
    print(arrPosCoul)
    arrNegCoul = np.array([negCouls[0], negCouls[1], negCouls[2]])
    print(arrNegCoul)

    #arrNegCoul = arrNegCoul * 1000000
    errPos = np.std(arrPosCoul, axis = 0)
    errNeg = np.std(arrNegCoul, axis = 0)
    meanPos = np.mean(arrPosCoul, axis = 0)
    meanNeg = np.mean(arrNegCoul, axis = 0)
    
    
    print(meanPos, meanNeg)

    
    # Generated linear fit for postive charge storage
    fig, ax = plt.subplots()
    slope1, intercept1, r_value1, p_value1, std_err = stats.linregress(posVolts, meanPos)
    line1 = [slope1*V + intercept1 for V in posVolts]
    #ax.plot(posVolts,meanPos,'o', posVolts, line1)
    ax.errorbar(posVolts, meanPos, yerr = errPos, fmt = 'o', fillstyle='none', ecolor='black',  mec='blue')
    plt.plot(posVolts, line1, color = 'red')
    # Generated linear fit for negative charge storage
    slope2, intercept2, r_value2, p_value2, std_err2 = stats.linregress(negVolts, meanNeg)
    line2 = [slope2*V + intercept2 for V in negVolts]
    ax.errorbar(negVolts, meanNeg, yerr = errNeg, fmt = 'o', fillstyle='none', ecolor='black',  mec='blue')
    plt.plot(negVolts, line2, color = 'red')
    #ax.plot(negVolts,meanNeg,'o', negVolts, line2)
    
    ax.set_xlabel('Voltage (V)')
    ax.set_ylabel(r'Charge($\mu$C)')
    plt.show()
    # py.plot_mpl(fig, filename='linear-Fit-with-postiveVoltage')
    # https://stackoverflow.com/questions/419163/what-does-if-name-main-do

    
if __name__ == "__main__":
    main()
