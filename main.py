import pandas as pd
import numpy as np
from datetime import datetime


def vcf_maker(name, phone):
    vcf_lines = []
    vcf_lines.append('BEGIN:VCARD')
    vcf_lines.append('VERSION:4.0')
    vcf_lines.append('FN:%s' % name)
    vcf_lines.append('TEL:%s' % phone)
    vcf_lines.append('END:VCARD')
    vcf_string = '\n'.join(vcf_lines) + '\n'
    return vcf_string


def no_name_extracter(df):
    no_name_df = df[df['name'].isnull()]
    no_name_df.to_csv('no-names.csv')


def write_vcf(row, index_file, timestamp):
    csv_file = open(f'contacts{index_file}-{timestamp}.vcf', 'a')
    csv_file.write(vcf_maker(row['name'], row['tel']))
    csv_file.close()


df = pd.read_csv('names.csv', header=0) # read your file here depend on your format
df = df.drop_duplicates(subset='tel', keep="first") # drop duplicate numbers and keep first ones only

no_name_extracter(df)

index_file = 1
timestamp = datetime.now().strftime('%M%S')
df_cleaned = df[~df['name'].isnull()]

for index, row in df_cleaned.iterrows():
    # I got error on files more than 100 numbers so sliced numbers by 100 numbers in each file
    if not (index+1)%100:                               
        index_file += 1
        timestamp = datetime.now().strftime('%M%S%f')
    write_vcf(row, index_file, timestamp)
    