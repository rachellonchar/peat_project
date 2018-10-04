#import data 
#read tex file

from save_funcs import *
cwd = os.getcwd()
data_dir = cwd[:-13]+'/data_files'
logger_dir = data_dir+'/jr_loggers'
well_files = {}
print(os.listdir(path=logger_dir))
#well_files.append({'all wells':
#text_file = open(cwd+'/MSP_precip_mm.txt', 'r') 
#i = 0 
#year,month,day,reading = [],[],[],[]
#for line in text_file:
    #string0 = line.split()
    #year.append(int(string0[0]))
    #month.append(int(string0[1]))
    #day.append(int(string0[2]))
    #reading.append(float(string0[3]))
    #i += 1
#text_file.close() 

#save_obj(year,'year')
#save_obj(month,'month')
#save_obj(day,'day')
#save_obj(reading,'reading')
