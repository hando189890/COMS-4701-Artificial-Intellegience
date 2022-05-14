
import numpy as np
import pandas as pd
import csv
import sys
import copy
# from plot_db import visualize_scatter
import statistics


def loaddata(datas):
    year = []
    weight = []
    height = []

    for data in datas:
       year.append(float(data[0]))
       weight.append(float(data[1]))
       height.append(float(data[2]))

    return year, weight, height


def normalization(data):

    mean = np.mean(data, axis = 0)
    stdev = np.std(data, axis = 0)
    data = (data - mean)/stdev
    return data



def gradientDescent(syear, sweight, sheight, coeff, times):

    b = [0,0,0]

    for i in range(0, times):
      sum =[0,0,0]
      for n in range(0, len(syear)):
            sum[0] = sum[0] + b[0] + b[1]*syear[n] + b[2]*sweight[n] - sheight[n]
            sum[1] = sum[1] + (b[0] + b[1]*syear[n] + b[2]*sweight[n] - sheight[n])*syear[n]
            sum[2] = sum[2] + (b[0] + b[1]*syear[n] + b[2]*sweight[n] - sheight[n])*sweight[n]

      for x in range(0, 3):
            b[x] = b[x] - coeff * sum[x]/len(syear)

    return b




def main():
    
    if len(sys.argv) != 3:
       print("Usage: python3 problem1_3.py [input_file] [output_file]")
       return

    csvFile = pd.read_csv(sys.argv[1], header=None)
    datas = np.array(csvFile)

    out_file = open(sys.argv[2],'wt')
    outs = csv.writer(out_file)



    year, weight, height = loaddata(datas)
    syear = normalization(year)
    sweight = normalization(weight)


    for coeff in [0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1, 5, 10]:
       oute =[]
       out = [coeff, 100]
       oute = gradientDescent(syear, sweight, height, coeff, 100)
       outs.writerow(out+oute)


    
    oute =[]
    out = [0.25, 50]
    oute = gradientDescent(syear, sweight, height, 0.25, 50)
    outs.writerow(out+oute)
    out_file.close()

if __name__ == '__main__':
   main()