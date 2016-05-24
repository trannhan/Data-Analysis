from pandas import read_csv
import csv
import numpy as np
import matplotlib.pyplot as plt


infolder = 'answers'
outfolder = 'answers'
file = open(outfolder + '/YearlyHistogram.out', 'w')
csvwriter = csv.writer(file, delimiter='\t', lineterminator='\n')

# read and process data  
datafile = infolder + '/YearlyAverages.out'
df = read_csv(datafile, sep='\t', header=None)
df.columns = ['station', 'year', 'max_temp', 'min_temp', 'precipitation']

grouped_year = df.groupby(by='year', sort=True)
max_groups = grouped_year.aggregate(np.max)

#write results
for year, grouped_year in grouped_year:
    max_data = ((df['year'] == year) \
                & (np.isclose(df['max_temp'], 
                                max_groups.ix[year, 'max_temp'])))
    max_max_temp = df.ix[max_data, 'station'].count()
    max_data = ((df['year'] == year) \
                & (np.isclose(df['min_temp'], 
                                max_groups.ix[year, 'min_temp'])))
    max_min_temp = df.ix[max_data, 'station'].count()
    max_data = ((df['year'] == year) \
                & (np.isclose(df['precipitation'], 
                                max_groups.ix[year, 'precipitation'])))
    max_sum_preci = df.ix[max_data, 'station'].count()
    csvwriter.writerow([str(year), str(max_max_temp), str(max_min_temp), 
                        str(max_sum_preci)])                    

file.close()  

#plot histogram
df = read_csv(outfolder + '/YearlyHistogram.out', sep='\t', header=None)
df.columns = ['year', 'max_temp_freq', 'min_temp_freq', 'precipitation_freq']
fig, ax = plt.subplots()
df['year'].hist(by=df['year'], ax=ax)
fig.savefig(outfolder + '/YearHistogram.png')