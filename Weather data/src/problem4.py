from pandas import read_csv
import csv


infolder = 'answers'
outfolder = 'answers'
file = open(outfolder + '/Correlations.out', 'w')
csvwriter = csv.writer(file, delimiter='\t', lineterminator='\n')

# read and process data  
datafile = infolder + '/YearlyAverages.out'
df = read_csv(datafile, sep='\t', header=None)
df.columns = ['station', 'year', 'max_temp', 'min_temp', 'precipitation']
df.sort_values('year', inplace = True)

datafile = 'yld_data/US_corn_grain_yield.txt'
df1 = read_csv(datafile, sep='\t', header=None)
df1.columns = ['year', 'grain_yield']
df1.sort_values('year', inplace = True)

#write results
grouped_station = df.groupby(by='station', sort=True)
for group, grouped_station in grouped_station:
    max_temp_cor = grouped_station.max_temp.corr(df1.grain_yield)
    min_temp_cor = grouped_station.min_temp.corr(df1.grain_yield)
    sum_preci_cor = grouped_station.precipitation.corr(df1.grain_yield)
    csvwriter.writerow([group, str(max_temp_cor), str(min_temp_cor), 
                        str(sum_preci_cor)])

file.close() 