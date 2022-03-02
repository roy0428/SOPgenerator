import pdb
from pandas import read_csv
import pandas as pd
import numpy as np
import argparse as args
import json
import re

def get_elements(data):

    data = open(data, 'r', encoding='utf-8')
    data = json.load(data)
    type = []
    for i in data["shapes"]:
        type.append(i['label'])
    
    count_intersection = 0
    count_spacing = 0
    for i in range(len(type)):
        if type[i] == 'intersection':
            count_intersection += 1
        elif type[i] == 'spacing':
            count_spacing += 1

    label_type = [] 
    if count_intersection != 0:
        label_type.append('intersection')
    if count_spacing != 0:
        label_type.append('spacing')

    return label_type, count_intersection, count_spacing

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
a = [[] for _ in range(len(filename_png))]
b = [[] for _ in range(len(filename_png))]
c = [[] for _ in range(len(filename_png))]

label_type = []
count_intersection = []
count_spacing = []
appenders = range(3)
arrLists = [label_type, count_intersection, count_spacing]
lst_no = []

for k in range(len(filename_png)):
    for i in range(len(filename_json_1)):    
        if filename_json_1[i,0] == filename_png[k,0]:
            index[k+1].append(1)
            appenders = get_elements(re.sub(r"[^a-zA-Z0-9/_.-]","",str('labeled/2019-U_girder/'+filename_png[k-1]+'.json')))
            for x, lst in zip(appenders, arrLists):
                lst.append(x)
            lst_no.append(k+1)
    for i in range(len(filename_json_2)):    
        if filename_json_2[i,0] == filename_png[k,0]:
            index[k+1].append(1)
            appenders = get_elements(re.sub(r"[^a-zA-Z0-9/_.-]","",str('labeled/20210407-U_girder/'+filename_png[k]+'.json')))
            for x, lst in zip(appenders, arrLists):
                lst.append(x)
            lst_no.append(k+1)
    for i in range(len(filename_json_3)):    
        if filename_json_3[i,0] == filename_png[k,0]:
            index[k+1].append(1)
            appenders = get_elements(re.sub(r"[^a-zA-Z0-9/_.-]","",str('labeled/20210407-wall/'+filename_png[k-1]+'.json')))
            for x, lst in zip(appenders, arrLists):
                lst.append(x)
            lst_no.append(k+1)
    for i in range(len(filename_json_4)):    
        if filename_json_4[i,0] == filename_png[k,0]:
            index[k+1].append(1)
            appenders = get_elements(re.sub(r"[^a-zA-Z0-9/_.-]","",str('labeled/20210416-MRT_Station/'+filename_png[k-1]+'.json')))
            for x, lst in zip(appenders, arrLists):
                lst.append(x)
            lst_no.append(k+1)
                
#print(arrLists)
#print(lst_no)
lst_label_type = [[] for _ in range(len(filename_png))]
lst_count_intersection = [[] for _ in range(len(filename_png))]
lst_count_spacing = [[] for _ in range(len(filename_png))]
for i in range(len(filename_png)):
    for j in range(len(lst_no)):
        if i == lst_no[j]:
            lst_label_type[i].append(arrLists[0][j])
            lst_count_intersection[i].append(arrLists[1][j])
            lst_count_spacing[i].append(arrLists[2][j])

#df.columns = ['labeling', 'label_type', 'count_intersection', 'count_spacing']
df = pd.DataFrame({'labeling': index, 'label_type': lst_label_type, 'count_intersection': lst_count_intersection, 'count_spacing': lst_count_spacing})
df.to_csv(args.suffix_sample_path) #'labeled_or_not.csv'

df2 = pd.read_csv(args.sample_path)
df2[['labeling']] = df[['labeling']]
df2[['label_type']] = df[['label_type']]
df2[['count_intersection']] = df[['count_intersection']]
df2[['count_spacing']] = df[['count_spacing']]

#df2.to_csv('labeled_or_not.csv', index=None)
df2.to_csv(args.sample_path, index=None)