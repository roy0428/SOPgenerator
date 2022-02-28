import pandas as pd
import argparse as args
import os

parser = args.ArgumentParser()
parser.add_argument('csv_path', type=str, help='path to csv_file')
parser.add_argument('new_csv_path', type=str, help='path to new csv_file')
args = parser.parse_args()

df = pd.read_csv(args.csv_path, names=['file_ID', 'label_type', 'labeling', 'contributor', 'QC'])
df.to_csv(args.new_csv_path, index=False)