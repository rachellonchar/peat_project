#regular code directory setup:
#import sys, os, os.path
#cwd = os.getcwd()
#sys.path.insert(0, cwd+'/prelims')
#from save_funcs import *

#regular code directory setup:
import sys, os, os.path
cwd = os.getcwd()
cwd_code = cwd[:-8]
sys.path.insert(0, cwd_code+'/prelims')
from save_funcs import *
font = {'family': 'serif',
        'color':  'darkred',
        'weight': 'normal',
        'size': 16,
        }

#from read_loggers import *
#from definitions import *
#cwd = os.getcwd()
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
plt.savefig(gn('ch1 and ch2',redirect=cwd_code[:-5]), bbox_inches='tight')
#plt.show()
#fig, ax = plt.subplots(figsize=(11.7,8.3))
#ii=0
#for kfs in [kf42, kf43, kf45]:
    #new,newp = [],[]
    #for idx in range(0,len(kfs['Date'])):
        #cnt = kfs['Date'][idx]
        #yr,m,day = int(cnt[:4]),int(cnt[5:7]),int(cnt[8:])
        #new.append([yr,m,day])
        #newp.append(m*30 + day + kfs['Time'][idx]/24)
    #plt.plot(newp,kfs['ch2'],'.',label=names[ii])
    #ii += 1
#plt.show()
    #plt.plot(newp,



# Fixing random state for reproducibility
#np.random.seed(19680801)


## tick every 5th easter
#rule = rrulewrapper(YEARLY, byeaster=1, interval=5)
#loc = RRuleLocator(rule)
#formatter = DateFormatter('%m/%d/%y')
#date1 = datetime.date(1952, 1, 1)
#date2 = datetime.date(2004, 4, 12)
#delta = datetime.timedelta(days=100)

#dates = drange(date1, date2, delta)
#s = np.random.rand(len(dates))  # make up some random y values


#fig, ax = plt.subplots()
#plt.plot_date(dates, s)
#ax.xaxis.set_major_locator(loc)
#ax.xaxis.set_major_formatter(formatter)
#ax.xaxis.set_tick_params(rotation=30, labelsize=10)
        
        
    
    ##print(yr,m,day)



#def per(Xvar,threshold):
    #if Xvar=='period of aeration':
        #Xvar = ['period of aeration',threshold]
    #elif Xvar=='period of inundation':
        #Xvar = ['period of inundation',threshold]
    #return Xvar

#def slope_at_thresholds(thresholds_array=[0,5,7,8,10],Xvar='period of aeration',Yvar='CH4_S1',color='NTs10',col_map='coolwarm',
    #deviations_predictor='NTs10',dev_fit_type=btf.func_exp,mask_events='inundated',show_masked_pts=0,
    #pic_name=None, pic_folder_name=None,save_or_show='show',cwd=cwd,deviations_applied_to='y'):
        
    #if Xvar=='period of aeration' or Yvar=='period of aeration':
        #mask_events = 'inundated'
    #if Xvar=='period of inundation' or Yvar=='period of inundation':
        #mask_events = 'aerated'
    ##thresholds_array = np.append(max(v['WT'])+1,thresholds_array) if mask_events=='inundated' else np.append(min(v['WT'])-1,thresholds_array)
    #t_e = 'aerated' if mask_events=='inundated' else 'inundated'
    #num_plots=len(thresholds_array)
    #cols = math.floor(np.sqrt(num_plots))
    #rows = math.ceil(num_plots/cols)
    #if cols<rows:
        #f1,f2=11.7,8.3
    #else:
        #f1,f2=8.3,11.7
    #if type(deviations_predictor) != type(None):
        #if deviations_applied_to=='y':
            #Y = deviations_from_fit(deviations_predictor, Yvar, fit_type=dev_fit_type,mask=None)
        #else:
            #Y = notation_fix(Yvar)
        #if deviations_applied_to=='x':
            #X = deviations_from_fit(deviations_predictor, Xvar, fit_type=dev_fit_type,mask=None)
            #Xvar = 'dev'
        #else:
            #None
        #if deviations_applied_to=='c':
            #ColorV = deviations_from_fit(deviations_predictor, color, fit_type=dev_fit_type,mask=None)
        #else:
            #ColorV = notation_fix(color)
    #else:
        #Y,ColorV = notation_fix(Yvar),notation_fix(color)
    #maxD, minD = max(ColorV), min(ColorV)
    #norm = matplotlib.colors.Normalize(vmin=minD, vmax=maxD, clip=True)
    #mapper = cm.ScalarMappable(norm=norm, cmap=plt.cm.get_cmap(col_map))
    #mapper.set_array([])
    #minY,maxY = min(Y),max(Y)
    #fig, ax = plt.subplots(ncols=cols,nrows=rows,  sharex=True, sharey=True, figsize=(f1,f2))
    #ct = 1
    #for threshold in thresholds_array:
        #plt.subplot(cols,rows,ct)
        #if mask_events=='inundated' or mask_events=='aerated':
            #mask,dic,ndic = notation_fix(['mask','mask '+mask_events+' events',threshold],ret_dics=1)
        #else:
            #mask = [0 for idx in range(0,len(Y))] #masks nothing
            #dic,ndic = v,n
        #def nf(string): return notation_fix(string,dic=dic,naming_dic=ndic)
        ##Xvar,Yvar,color = per(Xvar,threshold),per(Yvar,threshold),per(color,threshold)
        #Xvar = per(Xvar,threshold)
        #if Xvar != 'dev':
            #X = nf(Xvar)
        #fun, print_fun = btf.lin_fit(X,Y,mask=mask,type_return='function and print')
        #Xexp,Yexp = btf.array_span(X, fun,dense=1,specify_points=20)
        #if show_masked_pts==1:
            #plt.scatter(X,Y,c='white',edgecolor='darkgrey')
        
        #Xmsk = np.ma.masked_array(X,mask=mask)
        #Ymsk = np.ma.masked_array(Y,mask=mask)
        #plt.plot(Xexp,Yexp,'r',label=print_fun)
        #col_msk = np.ma.masked_array(ColorV,mask=mask)
        #bill = [mapper.to_rgba(val) for val in col_msk.compressed()]
        #plt.scatter(Xmsk.compressed(),Ymsk.compressed(),s=30,c=bill,cmap=mapper,
            #edgecolor=bill,vmin=minD,vmax=maxD,label='all '+t_e+' events')
        #plt.legend(loc=2,ncol=1, fancybox=True,prop={'size':10})
        ##if ct>1:
        #plt.title('threshold='+str(threshold))
        #if type(Xvar)==str and (Xvar=='WT' or Xvar=='NWT'):
            #plt.vlines(threshold,minY,maxY)
        ##else:
            ##plt.title('no masking')
        #plt.ylim(ymin=minY,ymax=maxY)
        #if type(Xvar)==list:
            #if Xvar[0]=='period of aeration':
                #plt.xlim(xmin=0,xmax=41)
        #else:
            #plt.xlim(xmin=min(Xexp),xmax=max(Xexp))
        #plt.colorbar(mapper,label='soil temp')
        #plt.grid()
        #ct+=1
    #fig.text(0.5, 0.04,list_to_name(Xvar,base=1)+' of '+t_e+' events', ha='center',fontdict=font)
    #fig.text(0.04, 0.5, 'CH4 residuals (based on soil temp at -10 cm)', va='center', rotation='vertical',fontdict=font)
    #plt.suptitle('Sensitivity to water table at different threshold definitions of '+t_e+' events',fontsize=16,fontdict=font)
    #plt.tight_layout()
    #plt.subplots_adjust(top=0.9,bottom=.1,left=.13)
    #if pic_name==None:
        #if save_or_show=='save':
            
            #plt.savefig(gn(), bbox_inches='tight')
            #plt.close(fig)
        #else:
            #plt.show()
    #else:
        #pnam = pic_namer(pic_name, pic_folder_name)
        #plt.savefig(gn(pic_name,pic_folder_name), bbox_inches='tight')
        
    
##slope_at_thresholds(Xvar='WT',save_or_show='save')
##slope_at_thresholds(Xvar='WT',mask_events='aerated',save_or_show='save')
##slope_at_thresholds(Xvar='period of inundation',save_or_show='save')
##slope_at_thresholds(Xvar='period of aeration',save_or_show='save')
#slope_at_thresholds(Xvar='period of inundation',Yvar='WT',color='NCH4_S1',deviations_applied_to='c',save_or_show='show',col_map='Blues')

##slope_at_thresholds(thresholds_array=[0,5,7,8,10],Xvar='period of aeration',Yvar='CH4_S1',color='NTs10',col_map='coolwarm',
    ##deviations_predictor='NTs10',dev_fit_type=btf.func_exp,mask_events='inundated',show_masked_pts=0,
    ##pic_name=None, pic_folder_name=None,save_or_show='show',cwd=cwd)