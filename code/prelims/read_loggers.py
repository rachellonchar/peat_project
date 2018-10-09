#import data 
#read tex file

from save_funcs import *
import re

cwd = os.getcwd()
data_dir = cwd[:-13]+'/data_files'
logger_dir = data_dir+'/jr_loggers'

mainD = cwd[:-13]+'/obj/' #for pickling
log_ct = 0 
read_types = ['Date','Time','ms','ch1','ch2']
for logr in os.listdir(path=logger_dir):
    logD = logger_dir+'/'+logr+'/'
    for file in os.listdir(logD):
        if file.endswith(".txt"):
            log_file_dater = file[len(logr)+1:-4]
            #comment to force txt file overwrite:
            #try:
                #logr_dic = load_obj(logr,parent_folder=mainD)
            #except:
                #print('no obj '+logr+'...creating obj now')
                #logr_dic = {}
                #for rts in read_types:
                    #logr_dic.update({rts:[]})
                #logr_dic.update({'data files already processed':[]})
            #uncomment to force rewrite:
            logr_dic = {}
            for rts in read_types:
                logr_dic.update({rts:[]})
            logr_dic.update({'data files already processed':[]})
            if log_file_dater in logr_dic['data files already processed']:
                print('...')
            else:
                print('Adding file '+log_file_dater+' to object '+logr)
                text_file = open(os.path.join(logD, file), 'r') 
                Date,Time,ms,ch1,ch2 = [],[],[],[],[]
                array_order = [Date,Time,ms,ch1,ch2]
                ct = 0
                for line in text_file:
                    ct+=1
                    if ct>=46:
                        sep = line.strip()
                        if sep=='</Log>':
                            None
                        else:
                            cnt = re.sub(r'<.+?>', '', sep)
                            cnt_type = re.search('</(.+?)>', sep)#.group(1)
                            if ct==46:
                                ref_None = type(cnt_type)
                            if type(cnt_type)!=ref_None:
                                res = cnt_type.group(1)
                                if res in read_types:
                                    if res=='Date' or res=='Time':
                                        #yr,m,day = int(cnt[:4]),int(cnt[5:7]),int(cnt[8:])
                                        #array_order[read_types.index(res)].append([day,m,yr])
                                        array_order[read_types.index(res)].append(cnt)
                                    #elif res=='Time':
                                        #hh,mm,ss = int(cnt[:2]),int(cnt[3:5]),int(cnt[6:])
                                        #mm_ss = mm + ss/60
                                        #hr_time = hh + mm_ss/60
                                        #array_order[read_types.index(res)].append(hr_time)
                                    else:
                                        array_order[read_types.index(res)].append(float(cnt))
                for rts in read_types:
                    merged = np.append(logr_dic[rts],array_order[read_types.index(rts)])
                    logr_dic.update({rts:merged})
                obj_files = np.append(logr_dic['data files already processed'],log_file_dater)
                logr_dic.update({'data files already processed':obj_files})
                save_obj(logr_dic,logr,parent_folder=mainD)
print('...well logger objects up to date')