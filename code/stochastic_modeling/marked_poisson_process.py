# seperates rainfall depths and rainfall waiting times

#regular code directory setup:
import sys, os, os.path
cwd = os.getcwd()
main_dirc = cwd.split('code', 1)[0]
cwd_code = main_dirc + 'code'
sys.path.insert(0, cwd_code+'/prelims')
from save_funcs import *
#-------------------------------------------

def time_series(rains,canopy_catch=0):
    readings = np.array([max(rain-canopy_catch,0) for rain in rains])
    #eliminating 'zero cm' depth events
    depths_array = []
    for depth in readings:
        if depth != 0:
            depths_array.append(depth)
    depths_array = np.array(depths_array)

    #interarrival times
    #setting all 'zero depth' flood events to 0 and all positive flood events to 1
    rain_on_off = np.ones_like(readings)
    for idx in range(0,len(readings)):
        reading = readings[idx]
        event=0 if reading==0 else 1
        rain_on_off[idx] = event
    #how many days in between rain events?
    arrival_times = []
    count = 1 #say that even when rains two consecutive days, you had to "wait" a day for the second rain event
    for value in rain_on_off:
        if value == 0:
            count += 1
        elif value == 1:
            count += 1
            arrival_times.append(count)
            count = 1
    arrival_times = np.array(arrival_times)
    return depths_array, arrival_times

#plot function
from scipy.stats import expon, gamma
def fit_exp(depths,waiting_times=None,var_name='',name_fig='exp',name_fig_dirc=None,save_or_show='show'):
    #The mean depth when days with 0 cm of inundation are NOT counted is:
    mean_depth = sum(depths) / len(depths)
    #mean_time = sum(waiting_times) / len(waiting_times)
    
    if type(waiting_times)==type(None):
        fig, ax = plt.subplots(ncols=1,nrows=1,  sharex=True, sharey=True, figsize=(9,9))
        plt.subplot(1,1,1)
    else:
        fig, ax = plt.subplots(ncols=1,nrows=2,  sharex=True, sharey=True, figsize=(17,9))
        plt.subplot(1,2,1)
    maxM,minM = max(depths),min(depths)
    midM = math.floor((maxM-minM)/2)
    #plt.hist(depths, 40, histtype='bar',  normed=True,label='histogram of actual rainfall depths')
    n1,n2,n3 = plt.hist(depths, 40, histtype='bar',  normed=True,label='histogram of measurements/simulations')
    maxF = round(max(n1),5)
    if type(waiting_times)==type(None):
        locc = 0
    else:
        locc = 1
    loc, scale = expon.fit(depths.astype(np.float64), floc=locc)
    x = np.linspace(expon.ppf(0.01,loc=loc,scale=scale),expon.ppf(0.99,loc=loc,scale=scale), 100)
    #print(max(expon.ppf(0.01,loc=loc,scale=scale)))
    plt.plot(x, expon.pdf(x,loc=loc,scale=scale),'r-', lw=5, alpha=0.6, label='fitted pdf')
    print_on = 'FIT PARAMETERS\nlocation paramter: '+str(loc)+'\nscale parameter: '+str(scale)
    plt.annotate(print_on, xy=(midM,maxF/2), xycoords='data',color='darkred')
    plt.annotate('actual mean event value:\n'+str(mean_depth),xy=(midM,maxF/3), xycoords='data',color='darkblue')
    plt.legend()
    #plt.xlabel('depth (mm)')
    plt.title(var_name+' values')
    plt.grid()
    if type(waiting_times)!=type(None):
        #if type(xtitles)!=list:
            #xtitles = [xtitles,'']
        #if ytitles!=list:
            #ytitles = ['ytitles','']
        maxM,minM = max(depths),min(depths)
        midM = math.floor((maxM-minM)/2)
        mean_time = sum(waiting_times) / len(waiting_times)
        plt.subplot(1,2,2)
        n1,n2,n3 = plt.hist(waiting_times, 150, histtype='bar',  normed=True,label='histogram of actual waiting times')
        maxF = round(max(n1),5)
        loc, scale = expon.fit(waiting_times.astype(np.float64), floc=1)
        x = np.linspace(expon.ppf(0.01,loc=loc,scale=scale),expon.ppf(0.99,loc=loc,scale=scale), 100)
        plt.plot(x, expon.pdf(x,loc=loc,scale=scale),'r-', lw=5, alpha=0.6, label='fitting pdf')
        print_on = 'FIT PARAMETERS\nlocation paramter: '+str(loc)+'\nscale parameter: '+str(scale)
        plt.annotate(print_on, xy=(midM,maxF/2), xycoords='data',color='darkred')
        #plt.annotate('actual mean waiting time between events (days):\n'+str(mean_time),xy=(10,.2), xycoords='data',color='darkblue')
        plt.annotate('actual mean waiting time between events:\n'+str(mean_time),xy=(midM,maxF/3), xycoords='data',color='darkblue')
        plt.legend()
        #plt.xlabel('time between rainfall events (days)')
        #plt.xlabel(xtitles[1])
        plt.title('Waiting time between events')
        #plt.title(xtitles[1])
        plt.grid()
    #fig.text(0.5, 0.04,'rainfall paramter', ha='center',fontdict=font)
    fig.text(0.5, 0.04,'event paramter', ha='center',fontdict=font)
    fig.text(0.04, 0.5, 'frequency', va='center', rotation='vertical',fontdict=font)
    plt.suptitle(var_name+' distributions',fontsize=16,fontdict=font)
    plt.tight_layout()
    plt.subplots_adjust(top=0.9,bottom=.1,left=.13)
    if save_or_show=='show':
        plt.show()
    elif save_or_show=='hold':
        None
    else:
        plt.savefig(gn(name_fig,name_fig_dirc))

#1
#depths_array,arrival_times = time_series()
#fit_exp(depths_array,arrival_times,name_fig='1')

##2
#depths_array,arrival_times = time_series(canopy_catch=.3)
#fit_exp(depths_array,arrival_times,name_fig='2')
