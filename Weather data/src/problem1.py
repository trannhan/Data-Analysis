from pandas import read_csv
import glob
import csv
  

missing = -9999
infolder = 'wx_data'
outfolder = 'answers'
file = open(outfolder + '/MissingPrcpData.out', 'w')
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
    missed_data = (df['precipitation'] == missing) \
                & (df['max_temp'] != missing) \
                & (df['min_temp'] != missing)    
    csvwriter.writerow([datafile.split('\\')[1], 
                        str(df.ix[missed_data,'date'].count())])

file.close()  