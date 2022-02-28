import pdb
from pandas import read_csv
import pandas as pd
import numpy as np
import argparse as args

parser = args.ArgumentParser()
parser.add_argument('png_path', type=str, help='path to png_file')
parser.add_argument('sample_path', type=str, help='path to sample_file')
parser.add_argument('suffix_sample_path', type=str, help='path to suffix_sample_file')
args = parser.parse_args()

#to_refer
filename_json_1 = '2019-U_girder.csv'
filename_json_2 = '20210407-U_girder.csv'
filename_json_3 = '20210407-wall.csv'
filename_json_4 = '20210416-MRT_Station.csv'

#to_check
filename_png = args.png_path

filename_json_1 = read_csv(filename_json_1)
filename_json_2 = read_csv(filename_json_2)
filename_json_3 = read_csv(filename_json_3)
filename_json_4 = read_csv(filename_json_4)
filename_png = read_csv(filename_png)

filename_json_1 = filename_json_1.values
filename_json_2 = filename_json_2.values
filename_json_3 = filename_json_3.values
filename_json_4 = filename_json_4.values
filename_png = filename_png.values

for i in range(len(filename_json_1)):
    filename_json_1[i,0] = filename_json_1[i,0].replace(".json","")
for i in range(len(filename_json_2)):
    filename_json_2[i,0] = filename_json_2[i,0].replace(".json","")
for i in range(len(filename_json_3)):
    filename_json_3[i,0] = filename_json_3[i,0].replace(".json","")
for i in range(len(filename_json_4)):
    filename_json_4[i,0] = filename_json_4[i,0].replace(".json","")

for i in range(len(filename_png)):
    filename_png[i,0] = filename_png[i,0].replace(".png","")

'''
for i in range(len(filename_json_1)):
    if len(filename_json_1[i,0]) == 20:
        filename_json_1[i,0] = filename_json_1[i,0][:16] + '0' + filename_json_1[i,0][16:]
for i in range(len(filename_json_2)):
    if len(filename_json_2[i,0]) == 20:
        filename_json_2[i,0] = filename_json_2[i,0][:16] + '0' + filename_json_2[i,0][16:]
for i in range(len(filename_json_1)):
    if len(filename_json_3[i,0]) == 20:
        filename_json_3[i,0] = filename_json_3[i,0][:16] + '0' + filename_json_3[i,0][16:]
for i in range(len(filename_json_4)):
    if len(filename_json_4[i,0]) == 20:
        filename_json_4[i,0] = filename_json_4[i,0][:16] + '0' + filename_json_4[i,0][16:]
'''    
data = pd.read_csv(args.sample_path)
#print(data)
index = [[] for _ in range(len(filename_png))]
for k in range(len(filename_png)):
    for i in range(len(filename_json_1)):    
        if filename_json_1[i,0] == filename_png[k,0]:
            index[k+1].append(1)
    for i in range(len(filename_json_2)):    
        if filename_json_2[i,0] == filename_png[k,0]:
            index[k+1].append(1)
    for i in range(len(filename_json_3)):    
        if filename_json_3[i,0] == filename_png[k,0]:
            index[k+1].append(1)
    for i in range(len(filename_json_4)):    
        if filename_json_4[i,0] == filename_png[k,0]:
            index[k+1].append(1)

df = pd.DataFrame(index)
df.to_csv(args.suffix_sample_path) #'labeled_or_not.csv'

#add header
df1 = pd.read_csv(args.suffix_sample_path, names=['labeling'])
df1.to_csv(args.suffix_sample_path)
#print(df1)
df2 = pd.read_csv(args.sample_path)
#print(df2)
df2[['labeling']] = df1[['labeling']]
df2[['label_type']] = 'spacing'
#df2.to_csv('labeled_or_not.csv', index=None)
df2.to_csv(args.sample_path, index=None)