#from definitions import *

#regular code directory setup:
import sys, os, os.path
cwd = os.getcwd()
main_dirc = cwd.split('code', 1)[0]
cwd_code = main_dirc + 'code'
sys.path.insert(0, cwd_code+'/prelims')
from save_funcs import *

sys.path.insert(0, cwd_code+'/inundation_aeration_analysis')
from preamble import *
#from 


#plt.plot(MgA(deviations_predictor),MgA(Yvar))
#X,Y,Yexp,devs = btf.deviations(MgA(deviations_predictor),MgA(Yvar),fit_func=btf.func_exp, mask=None)
#print(Yexp)
#plt.plot(X,Y,'bo')
#plt.plot(X,Yexp,'r')
#plt.show()



#WT,CH_devs,Ts = btf.series_cleanup(c,devs,b)
#plt.plot(c,devs,'bo')
#plt.show()


#def plot_basic(Xvar,Yvar,color='Ts10',deviations_predictor=None,dev_fit_type=btf.func_exp,
    #fit_type=btf.func_linear,deviations_applied_to='y',col_map='coolwarm',
    #pic_name=None, pic_folder_name=None,save_or_show='show'):
#variables0,naming0 = load_obj('new_parameters'),load_obj('new_naming')
def plot_basic(Xs,Ys,color,fit=btf.func_linear,mask=None,
    col_map='coolwarm',save_or_show='show',pic_name=None):
    
    X,Y,ColorV = Xs,Ys,color
    #X,Y,ColorV = np.ma.masked_array(Xs,mask=mask),np.ma.masked_array(Ys,mask=mask),np.ma.masked_array(color,mask=mask)
    dicf = btf.fit_2sets(X,Y,fit_func=fit,mask=mask)
    fun = dicf['function']
    Xd,Yd = btf.array_span(X,fun,dense=1,specify_points=20)
    maxD, minD = max(ColorV), min(ColorV)
    norm = matplotlib.colors.Normalize(vmin=minD, vmax=maxD, clip=True)
    mapper = cm.ScalarMappable(norm=norm, cmap=plt.cm.get_cmap(col_map))
    mapper.set_array([])
    minY,maxY = min(Y),max(Y)
    fig, ax = plt.subplots(ncols=1,nrows=1,  sharex=True, sharey=True, figsize=(9,9))
    plt.subplot(1,1,1)
    
    plt.plot(Xd,Yd,label=dicf['print function'])
    #plt.plot(X,Y,label='reg')
    bill = [mapper.to_rgba(val) for val in ColorV]
    plt.scatter(np.ma.masked_array(Xs,mask=mask),np.ma.masked_array(Ys,mask=mask),
        s=30,c=bill,cmap=mapper,
        edgecolor=bill,vmin=minD,vmax=maxD,label='all events')
    plt.legend(loc=4,ncol=1, fancybox=True,prop={'size':8})
    plt.colorbar(mapper,label='color variable')
    plt.grid()
    
    #dicF = btf.fit_2sets(X,Y,fit_func=fit_type)
    #fun, print_fun = dicF['function'],dicF['print function']
    #Xexp,Yexp = btf.array_span(X, fun,dense=1,specify_points=20)
    #plt.plot(Xexp,Yexp,'r',label=print_fun)
    #bill = [mapper.to_rgba(val) for val in ColorV]
    #plt.scatter(X,Y,s=30,c=bill,cmap=mapper,
        #edgecolor=bill,vmin=minD,vmax=maxD,label='all events')
    #plt.legend(loc=4,ncol=1, fancybox=True,prop={'size':8})
    #plt.colorbar(mapper,label=namer(color,ndc))
    #plt.grid()
    #fig.text(0.5, 0.04,list_to_name(Xvar,ndx), ha='center',fontdict=font)
    ##fig.text(0.04, 0.5, 'CH4 residuals (based on soil temp at -10 cm)', va='center', rotation='vertical',fontdict=font)
    #fig.text(0.04, 0.5, list_to_name(Yvar,ndy), va='center', rotation='vertical',fontdict=font)
    ##plt.suptitle('Sensitivity to water table at different threshold definitions of '+t_e+' events',fontsize=16,fontdict=font)
    #plt.suptitle(list_to_name(Xvar,ndx)+' vs. '+list_to_name(Yvar,ndy),fontsize=16,fontdict=font)
    plt.tight_layout()
    plt.subplots_adjust(top=0.9,bottom=.1,left=.13)
    #if pic_name==None:
        #if save_or_show=='save':
            
            #plt.savefig(gn(), bbox_inches='tight')
            #plt.close(fig)
        #else:
            #plt.show()
    #else:
        ##pnam = pic_namer(pic_name, pic_folder_name)
        #plt.savefig(gn(pic_name,pic_folder_name), bbox_inches='tight')

deviations_predictor,Yvar = 'Tsoil_10cm','CH4'
a,b,c = MgA(deviations_predictor),MgA(Yvar),MgA('WT')
devs,mask_nan = btf.deviations(a,b,fit_type=btf.func_exp,mask=None)
ma = maskA(1)
mi = maskI(1)
mmi = btf.mult_masks(mi,mask_nan)
mm = btf.mult_masks(mask_nan,ma)

#dicf = btf.fit_2sets(X,Y,fit_func=fit,mask=mask)
#fun = dicf['function']
#Xd,Yd = btf.array_span(X,fun,dense=1,specify_points=20)

plot_basic(c,devs,color=b,mask=mm)
plot_basic(c,devs,color=b,mask=mmi)
plt.show()

def perm_fit_exp(Xl,Yl,name_fig='permanence_times',
    num_bars = 3,Cl='WT',col_map='BrBG',
    name_fig_dirc=None,save_or_show='show'):
    
    #threshold_array=np.linspace(mint,maxt,3)
    cols,rows = 2,4#int(len(years)/2)
    if cols<rows:
        f1,f2=15,8.3
    else:
        f1,f2=8.3,15
    fig, ax = plt.subplots(ncols=cols,nrows=rows,  sharex=True, sharey=True, figsize=(f1,f2))
    #PTs = ['permanence time in aerated state','permanence time in inundated state']
    #thN = 0
    #for thres in threshold_array:
        ##mask,dic,ndic = notation_fix([PTs[0],thres],ret_dics=1)
        #noholdA,holdDA,modfA,unitA = permA(thres)
        #nohold,holdDI,modfI,unit = permI(thres)
        #pA,pI = [],[]
    dicfAll = btf.fit_2sets(MgA(Xl),MgA(Yl),fit_func=btf.func_exp,mask=None)
    funAll = dicfAll['function']
    XdAl,YdAl = btf.array_span(MgA(Xl),funAll,dense=1,specify_points=20)
    nn=1
    for yr in years:
        plt.subplot(cols,rows,nn)
        ColorV = v[yr][Cl]
        maxi = max(abs(max(ColorV)), abs(min(ColorV)))
        maxD, minD = maxi,-1*maxi
        norm = matplotlib.colors.Normalize(vmin=minD, vmax=maxD, clip=True)
        mapper = cm.ScalarMappable(norm=norm, cmap=plt.cm.get_cmap(col_map))
        mapper.set_array([])
        #minY,maxY = min(Y),max(Y)
        #fig, ax = plt.subplots(ncols=1,nrows=1,  sharex=True, sharey=True, figsize=(9,9))
        #plt.subplot(1,1,1)
        dicf = btf.fit_2sets(v[yr][Xl],v[yr][Yl],fit_func=btf.func_exp,mask=None)
        fun = dicf['function']
        Xd,Yd = btf.array_span(v[yr][Xl],fun,dense=1,specify_points=20)
        plt.plot(Xd,Yd,'y',label=dicf['print function'])
        plt.plot(XdAl,YdAl,'r',label=dicfAll['print function'])
        #plt.plot(
        #plt.plot(X,Y,label='reg')
        bill = [mapper.to_rgba(val) for val in ColorV]
        plt.scatter(v[yr][Xl],v[yr][Yl],
            s=30,c=bill,cmap=mapper,
            edgecolor=bill,vmin=minD,vmax=maxD,label='all events')
        plt.legend(loc=2,ncol=1, fancybox=True,prop={'size':8})
        plt.colorbar(mapper,label='color variable')
        plt.grid()
        
        #plt.plot(v[yr][Xl],v[yr][Yl],'r.')
        plt.ylim(ymin=0,ymax=0.23)
        plt.xlim(xmin=0,xmax=20)
        plt.title(yr)
        nn+=1
            #if yr not in nohold:
                #pA = np.append(pA,holdDA[yr])
                #pI = np.append(pI,holdDI[yr])
        #thN+=1
        #locat = [thN,thN+len(threshold_array)]
        ##for pp in [0,1]:
        #PTs = [modfA,modfI]
        #pp=0
        #kplus = 0
        #print(thres)
        #for waiting_times in [pA,pI]:
            #perm,N = PTs[pp],locat[pp]
            #mean_time = sum(waiting_times) / len(waiting_times)
            #maxM,minM = max(waiting_times),min(waiting_times)
            #midM = math.floor((maxM-minM)/2)
            #plt.subplot(cols,rows,N)
            #n1,n2,n3 = plt.hist(waiting_times, num_bars, histtype='bar',  normed=True,label='histogram of \npermanence times')
            #maxF = round(max(n1),5)
            #loc, scale = expon.fit(waiting_times.astype(np.float64), floc=0)
            #x = np.linspace(expon.ppf(0.01,loc=loc,scale=scale),expon.ppf(0.99,loc=loc,scale=scale), 100)
            #exfit = expon(loc=loc, scale=scale)
            #ks = kstest(waiting_times,exfit.cdf)
            #if ks[1]>=0.001:
                #kplus+=1
                #k0 = ks
            #plt.plot(x, expon.pdf(x,loc=loc,scale=scale),'r-', lw=5, alpha=0.6, label='fitting pdf')
            #print_on = 'FIT PARAMETERS\nlocation paramter: '+str(loc)+'\nscale parameter: '+str(scale)
            #plt.annotate(print_on, xy=(midM,maxF*(2/3)), xycoords='data',color='darkred')
            #plt.annotate('mean permanence time:\n'+str(mean_time),xy=(midM,maxF/3), xycoords='data',color='darkblue')
            
            #plt.annotate(str(len(waiting_times))+' events tot., '+str(num_bars)+' bars', xy=(max(x)*1/9,maxF*1/9), xycoords='data',color='black')
            #plt.legend(loc=1,ncol=1, fancybox=True,prop={'size':10})
            #plt.title(perm+'\nthreshold='+str(thres))
            #plt.grid()
            #pp=1
        #if kplus==2:
            #print('\n',thres)
            #print(PTs[0])
            #print('D=',k0[0])
            #print('pvalue=',k0[1])
            #print(PTs[1])
            #print('D=',ks[0])
            #print('pvalue=',ks[1])
    #fig.text(0.5, 0.04,'permanence time (days)', ha='center',fontdict=font)
    #fig.text(0.04, 0.5, 'frequency', va='center', rotation='vertical',fontdict=font)
    #plt.suptitle('Permanence time distributions',fontsize=16,fontdict=font)
    #plt.tight_layout()
    #plt.subplots_adjust(top=0.9,bottom=.1,left=.13)
    if save_or_show=='show':
        plt.show()
    elif save_or_show=='hold':
        None
    else:
        #plt.savefig(gn(name_fig+'9.3_'+str(num_bars)+'bars',name_fig_dirc))
        plt.savefig(gn(name_fig))

#for nn in [3,4,5,7]:
    #perm_fit_exp(threshold_array=[9.3],num_bars=nn,save_or_show='save')
#perm_fit_exp('Tsoil_10cm','CH4',name_fig='all_years_CH4_Ts_no1113',save_or_show='save')#threshold_array=[9.3],num_bars=4,save_or_show='show')
 
