
##regular code directory setup:
#import sys, os, os.path
#cwd = os.getcwd()
#main_dirc = cwd.split('code', 1)[0]
#cwd_code = main_dirc + 'code'
#sys.path.insert(0, cwd_code+'/prelims')
#from save_funcs import *
##-------------------------------------------

#from water_table_functions import *
#from substrate_directory import *

from preamble import *
from inundation_aeration_period_definitions import *

def perm_max_events(maxt=0,mint=18):
    
    PTs = ['permanence time in aerated state','permanence time in inundated state']
    threshold_array = np.linspace(mint,maxt,20)
    maxS,maxT = 0,0
    for thres in threshold_array:
        mask,dic,ndic = notation_fix([PTs[0],thres],ret_dics=1)
        hold = [0,0]
        for pp in [0,1]:
            perm = PTs[pp]
            wdic = notation_fix(perm,dic=dic,naming_dic=ndic)
            waiting_times = np.array(wdic[thres])
            hold[pp] = len(waiting_times)
        if hold[pp]>=maxS:
            maxS,maxT=hold[pp],thres
    return maxS,maxT

#s,t = perm_max_events()
#print(s,t)
#s,t = perm_max_events(maxt=12,mint=17.5)
#print(s,t)
#s,t = perm_max_events(maxt=14,mint=15)
#print(s,t)
#s,t = perm_max_events(maxt=14,mint=14.4)
#print(s,t)

#plot function
from scipy.stats import expon, gamma
def perm_fit_exp(threshold_array=[9.3],name_fig='permanence_times',
    num_bars = 5,
    name_fig_dirc=None,save_or_show='show'):
    
    cols,rows = 2,len(threshold_array)
    if cols<rows:
        f1,f2=15,8.3
    else:
        f1,f2=8.3,15
    fig, ax = plt.subplots(ncols=cols,nrows=rows,  sharex=True, sharey=True, figsize=(f1,f2))
    PTs = ['permanence time in aerated state','permanence time in inundated state']
    thN = 0
    for thres in threshold_array:
        mask,dic,ndic = notation_fix([PTs[0],thres],ret_dics=1)
        thN+=1
        locat = [thN,thN+len(threshold_array)]
        for pp in [0,1]:
            perm,N = PTs[pp],locat[pp]
            wdic = notation_fix(perm,dic=dic,naming_dic=ndic)
            waiting_times = np.array(wdic[thres])
            #print(thres,perm,len(waiting_times))
            mean_time = sum(waiting_times) / len(waiting_times)
            maxM,minM = max(waiting_times),min(waiting_times)
            midM = math.floor((maxM-minM)/2)
            plt.subplot(cols,rows,N)
            n1,n2,n3 = plt.hist(waiting_times, num_bars, histtype='bar',  normed=True,label='histogram of \npermanence times')
            maxF = round(max(n1),5)
            loc, scale = expon.fit(waiting_times.astype(np.float64), floc=0)
            x = np.linspace(expon.ppf(0.01,loc=loc,scale=scale),expon.ppf(0.99,loc=loc,scale=scale), 100)
            plt.plot(x, expon.pdf(x,loc=loc,scale=scale),'r-', lw=5, alpha=0.6, label='fitting pdf')
            print_on = 'FIT PARAMETERS\nlocation paramter: '+str(loc)+'\nscale parameter: '+str(scale)
            plt.annotate(print_on, xy=(midM,maxF*(2/3)), xycoords='data',color='darkred')
            plt.annotate('mean permanence time:\n'+str(mean_time),xy=(midM,maxF/3), xycoords='data',color='darkblue')
            
            plt.annotate(str(len(waiting_times))+' events tot., '+str(num_bars)+' bars', xy=(max(x)*1/9,maxF*1/9), xycoords='data',color='black')
            plt.legend(loc=1,ncol=1, fancybox=True,prop={'size':10})
            plt.title(perm+'\nthreshold='+str(thres))
            plt.grid()
    fig.text(0.5, 0.04,'permanence time (days)', ha='center',fontdict=font)
    fig.text(0.04, 0.5, 'frequency', va='center', rotation='vertical',fontdict=font)
    plt.suptitle('Permanence time distributions',fontsize=16,fontdict=font)
    plt.tight_layout()
    plt.subplots_adjust(top=0.9,bottom=.1,left=.13)
    if save_or_show=='show':
        plt.show()
    elif save_or_show=='hold':
        None
    else:
        plt.savefig(gn(name_fig+'9.3_'+str(num_bars)+'bars',name_fig_dirc))

#for nn in [3,4,5,7]:
    #perm_fit_exp(threshold_array=[9.3],num_bars=nn,save_or_show='save')
perm_fit_exp(threshold_array=[9.3],num_bars=3,save_or_show='show')
    


