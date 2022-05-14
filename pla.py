import numpy as np
import pandas as pd
import csv
import sys
import copy
# from plot_db import visualize_scatter



def train(weights, data): 

    input = weights[0] * int(data[0]) + weights[1] * int(data[1]) + weights[2]
    if int(data[2]) * input <= 0:
        data = update(weights, data)

    data = [weights[0], weights[1], weights[2]]    
    return data
             

def update(weights, data):     
    weights[0] = weights[0] + int(data[2]) * int(data[0])
    weights[1] = weights[1] + int(data[2]) * int(data[1])
    weights[2] = weights[2] + int(data[2])
    


def main():
    
    if len(sys.argv) != 3:
       print("Usage: python3 problem1_3.py [input_file] [output_file]")
       return

    csvFile = pd.read_csv(sys.argv[1], header=None)
    datas = np.array(csvFile)

    out_file = open(sys.argv[2],'wt')
    outs = csv.writer(out_file)

   
    weights = [0 , 0, 0] 
    temp = [-1, -1, -1]
    output = []
    # head = ["weight 1", "weight 2", "b"]
    # outs.writerow(head)

    unconvergence = True
   

    while (unconvergence):
          temp = weights
         
          for data in datas:
            temprow = train(weights, data)
            output.append(temprow)
            weights = temprow

          if  weights == temp:
              unconvergence = False
          # visualize_scatter(df=csvFile, feat1=0, feat2=1, labels=2, weights=temprow, title="perceptron")
          outs.writerow(temprow)


    
    out_file.close()

    # visualize_scatter(df=csvFile, feat1=0, feat2=1, labels=2, weights=, title="perceptron")


if __name__ == '__main__':
   main()