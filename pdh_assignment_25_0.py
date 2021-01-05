from os import walk
import pandas as pd
import numpy as np
import math


#define Euclid Distance
def euclid_dist(d1, d2):
    if len(d1) != len(d2):
        return None
    
    sum_diff = 0
    for i in range(0, len(d1), 1):
        sum_diff = sum_diff + (d1[i] - d2[i])**2
    return math.sqrt(sum_diff)

#load all data of companies into panda dataframe
#init columns with date and companycode
header = ['Company Code']
for i in range(0, 128, 1):
    header.append(i)
df_original_price = pd.DataFrame(columns=header)

#load data to the dataframe
fileout = open("stock_data_stat.txt", 'a')
for (dirpath, dirnames, filenames) in walk('./data/'):
    for f in filenames:
        temp = {}
        temp['Company Code'] = f.split('.')[0]
        
        #read line
        with open('./data/' + f) as file_content:
            prices = file_content.read().splitlines()
            #write to stats file
            if len(prices) != 256:
                fileout.write("ABNORMAL ==== ")
            fileout.write(f + " contains number of lines: ")
            fileout.write(str(len(prices)) + '\n')
            for j in range(0,128,1):
                temp[j] = prices[j]
            print(temp)
     
        df_original_price = df_original_price.append(temp, ignore_index = True)
fileout.close()

print('After loading all')
print(df_original_price.head(10))
print(df_original_price.describe())

