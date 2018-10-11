

#regular code directory setup:
import sys, os, os.path
cwd = os.getcwd()
main_dirc = cwd.split('code', 1)[0]
cwd_code = main_dirc + 'code'
sys.path.insert(0, cwd_code+'/prelims')
from save_funcs import *
#-------------------------------------------



from matplotlib.dates import (YEARLY, DateFormatter,
                              rrulewrapper, RRuleLocator, drange)
import datetime
mainD = cwd[:-13]+'/obj/' #for pickling
#def load_fix(objj): return load_obj(objj,mainD)

names,holder = ['KF42W','KF43W','KF45W'],[]
for n in names:
    holder.append(load_obj(n,mainD))


#fig, ax = plt.subplots(figsize=(11.7,8.3))
formatter = DateFormatter('%m/%d/%y')

cols,rows=1,2
fig, ax = plt.subplots(ncols=cols,nrows=rows,  sharex=True, sharey=True, figsize=(15,5))

ii=0
plt.subplot(cols,rows,1)
for kfs in holder:
    newp = []
    for idx in range(0,len(kfs['Date'])):
        cnt,tnt = kfs['Date'][idx],kfs['Time'][idx]
        yr,m,day = int(cnt[:4]),int(cnt[5:7]),int(cnt[8:])
        hh,mm,ss = int(tnt[:2]),int(tnt[3:5]),int(tnt[6:])
        di = datetime.datetime(yr, m, day,hh,mm,ss)
        newp.append(di)
    plt.plot_date(newp,kfs['ch1'],'.',label=names[ii])
    plt.title('channel 1')
    ii += 1
plt.legend(loc=2,ncol=1, fancybox=True,prop={'size':10})

ii=0
plt.subplot(cols,rows,2)
for kfs in holder:
    newp = []
    for idx in range(0,len(kfs['Date'])):
        cnt,tnt = kfs['Date'][idx],kfs['Time'][idx]
        yr,m,day = int(cnt[:4]),int(cnt[5:7]),int(cnt[8:])
        hh,mm,ss = int(tnt[:2]),int(tnt[3:5]),int(tnt[6:])
        di = datetime.datetime(yr, m, day,hh,mm,ss)
        newp.append(di)
    plt.plot_date(newp,kfs['ch2'],'.',label=names[ii])
    plt.title('channel 2')
    ii += 1
plt.legend(loc=2,ncol=1, fancybox=True,prop={'size':10})

fig.text(0.5, 0.04,'date and time', ha='center',fontdict=font)
fig.text(0.04, 0.5, 'channel  readings (m)', va='center', rotation='vertical',fontdict=font)
plt.suptitle('Jr Logger preliminary time series' ,fontsize=16,fontdict=font)
plt.tight_layout()
plt.subplots_adjust(top=0.9,bottom=.1,left=.13)
plt.grid()
plt.savefig(gn('ch1 and ch2'), bbox_inches='tight')
