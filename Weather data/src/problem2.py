from pandas import read_csv, Series
import glob
from datetime import datetime
import numpy as np
import csv
  

missing = -9999
infolder = 'wx_data'
outfolder = 'answers'
file = open(outfolder + '/YearlyAverages.out', 'w')
csvwriter = csv.writer(file, delimiter='\t', lineterminator='\n')
filelist = []

# read filenames      
for datafile in glob.glob(infolder + "/*"):  
    filelist.append(datafile)

filelist.sort()

# read and process data 
for datafile in filelist:  
    df = read_csv(datafile, sep='\t', header=None)
    df.columns = ['date', 'max_temp', 'min_temp', 'precipitation']
    df.replace(missing, np.nan, inplace=True)
    
    year = []
    for i in df.index:
        dt = datetime.strptime(str(df['date'][i]), '%Y%m%d')
        year.append(dt.year)
    df['year'] = Series(year)
    
    grouped_year = df.groupby(by='year')    
    filename = datafile.split('\\')[1]
    avg_max_temp = round(grouped_year['max_temp'].mean(),2)
    avg_min_temp = round(grouped_year['min_temp'].mean(),2)
    sum_preci = round(grouped_year['precipitation'].sum(),2)
    for year, grouped_year in grouped_year:
        csvwriter.writerow([filename, str(year), str(avg_max_temp[year]), 
                            str(avg_min_temp[year]), str(sum_preci[year])])

file.close()  