
from preamble import *
import matplotlib.backends.backend_pdf

def plt_various_masks_yearly_subplots(xparam='Ts10',yparam='NCH4_S1',cparam='WTa',
    scaled=True,fit='lin',thres_lev=0,years=[11131,11132], leg=1,tempTh=10,
    pdf=matplotlib.backends.backend_pdf.PdfPages("output.pdf"),
    name_fig='out',fig_type='svg',col_map='BrBG',inc_call=1113,
    save_or_show='save'):
    
    num_plots=len(years)
    cols = math.floor(np.sqrt(num_plots))
    rows = math.ceil(num_plots/cols)
    if cols<rows:
        f1,f2=11.7,9
    else:
        f1,f2=9,11.7
    #fig, ax = plt.subplots(ncols=cols,nrows=rows,  sharex=True, sharey=True, figsize=(f1,f2))
    fig, ax = plt.subplots(ncols=cols,nrows=rows,  sharex=True, sharey=True, figsize=(7*rows,7*cols))
    xparam_y = xparam if type(xparam)==list else [xparam]
    yparam_y = yparam if type(yparam)==list else [yparam]
    cparam_y = cparam if type(cparam)==list else [cparam]
    
    if inc_call==None:
        inc_call = inclusive_yr_call(*tuple(years))
    xparam_y.append(inc_call)
    yparam_y.append(inc_call)
    cparam_y.append(inc_call)
    Xx,Yy,Cc = v(*ftup(xparam_y),mask=None), v(*ftup(yparam_y),mask=None),v(*ftup(cparam_y),mask=None)
    if type(cparam)==list:
        if cparam[2]=='PoI':
            maxD,minD=160,0
        elif cparam[2]=='PoIA':
            maxD,minD = 170,-170#max(Cc),min(Cc)
    elif type(cparam)==str:
        if cparam=='WTa':
            maxx = max(abs(max(Cc)), abs(min(Cc)))
            maxD, minD = maxx,-maxx
        else:
            maxD, minD = max(Cc),min(Cc)
        
    norm = matplotlib.colors.Normalize(vmin=minD, vmax=maxD, clip=True)
    mapper = cm.ScalarMappable(norm=norm, cmap=plt.cm.get_cmap(col_map))
    mapper.set_array([])
    miny,maxy = min(Yy),max(Yy)
    minx,maxx = min(Xx),max(Xx)
    #colors=['r','chocolate','r','r']
    colors = ['blue','lightcoral','darkslateblue','chocolate']
    tits = ['warm, wet','warm, dry','cool, wet','cool, dry']
    fitt = ['exp','exp','lin','lin']
    maskers = [[['c',tempTh],['a',thres_lev]],
        [['c',tempTh],['i',thres_lev]],
        [['h',tempTh],['a',thres_lev]],
        [['h',tempTh],['i',thres_lev]]]
    #maskers = [[
    #colors = ['blue','lightcoral','darkslateblue','chocolate']
    #tits = ['warm, wet','warm, dry','cool, wet','cool, dry']
    #fitt = ['exp','lin']#'exp','lin','lin']
    #maskers = [['a',thres_lev],
        #['i',thres_lev]]
    ct = 1
    for year in years:
        plt.subplot(cols,rows,ct)
        xparam_y[-1], yparam_y[-1],cparam_y[-1] = year,year,year
            
        ColorV,nnc,nnuc,nnmc = vnu(*ftup(cparam_y),mask=None)
        print(max(ColorV),min(ColorV))
        
        x,nnx,nnu,nnm = vnu(*ftup(xparam_y),mask=None)
        y,nny,nnuy,nnm = vnu(*ftup(yparam_y),mask=None)
        
        #print(max(ColorV))
        
        bill = [mapper.to_rgba(val) for val in ColorV]
        plt.scatter(x,y,s=30,c=bill,cmap=mapper,edgecolor=bill,vmin=minD,vmax=maxD)
        
        pp=0
        for mm in maskers:
            show_line=False
            x,nnx,nnu,nnm = vnu(*ftup(xparam_y),mask=mm)
            y,nny,nnuy,nnm = vnu(*ftup(yparam_y),mask=mm)
            #plt.scatter(x,y,c=colors[pp],marker='o',edgecolor=colors[pp],alpha=0.5)
            #try:
                #x,nx,ux,mn = vnu('Xs',xparam,yparam,fitt[pp],year,mask=mm)
                #y,ny,uy,mn = vnu('Ysexp',xparam,yparam,fitt[pp],year,mask=mm)
                #mn = 'no mask' if mn=='' else mn
                #plt.plot(x,y,colors[pp],label=mn,lw=0.5)
            #except:
                #None
            pp+=1
        plt.title(yname(year))
        plt.colorbar(mapper,label=nnc+nnuc)
        if leg==1:
            plt.legend(loc=1,ncol=1, fancybox=True,prop={'size':10})
        plt.tight_layout()
        if scaled:
            plt.xlim(xmin=minx,xmax=maxx)
            plt.ylim(ymin=miny,ymax=maxy)
            nam_add = 'scaled_'
        else:
            #plt.ylim(ymin=min(ybound),ymax=max(ybound))
            nam_add = ''
        ct += 1
    fig.text(0.5, 0.04,nnx+nnu, ha='center',fontdict=font)
    fig.text(0.04, 0.5, nny+nnu, va='center', rotation='vertical',fontdict=font)
    plt.suptitle('Water table influence on methane emissions, depending on if peatland is inundated or aerated',
        fontsize=16,fontdict=font)
    plt.tight_layout()
    plt.subplots_adjust(top=0.9,bottom=.1,left=.13)
    #--
    if save_or_show=='show':
        plt.show()
    elif save_or_show=='hold':
        None
    else:
        if fig_type=='pdf pages':
            pdf.savefig(fig)
        else:
            plt.savefig(gn(name_fig,sub_dirc='CH4_states',f='.'+fig_type),format=fig_type)

#yy1 = [44091701113,441518,11130,1113]
#yy2 = [2009,2010,2012]#,2014,20150,20170]
#yy3 = [2014,20150,20170]
#yy4 = [2015,2016,2017,2018]

yy1 = [1113,2009,2010]
yy2 = [2012,2014,2015]
yy3 = [2016,2017,2018]
yys = [yy1,yy2,yy3]#,yy4]

pdf = matplotlib.backends.backend_pdf.PdfPages("bulk_PoIA.pdf")
#plt_overlap('Ts10','WTa','CH4_S1',
    #pdf=pdf,fig_type='pdf pages')
    
#ft = 'svg'

#plt_various_masks_yearly_subplots(xparam='DoY',yparam='WTa',fit='exp',years=[2010,2015,2016],#save_or_show='hold')
    #col_map='PuOr',cparam=['threshold=',0,'PoIA'],
    #pdf=pdf,scaled=True,fig_type=ft,name_fig='156time_series_WTPoIA')   
#plt_various_masks_yearly_subplots(xparam='NTs10',yparam='CH4_S1',years=[2010,2015,2016],#save_or_show='hold')
    #col_map='PuOr',cparam=['threshold=',0,'PoIA'],
    #pdf=pdf,scaled=True,fig_type=ft,name_fig='156PoIA_TCH')   
    
    
#plt_various_masks_yearly_subplots(xparam='NTs10',yparam='CH4_S1',years=[2010,2015,2016],#save_or_show='hold')
    #col_map='Blues',cparam=['threshold=',0,'PoI'],
    #pdf=pdf,scaled=True,fig_type=ft,name_fig='156PoI') 
#plt_various_masks_yearly_subplots(xparam='NTs10',yparam='CH4_S1',years=[2010,2015,2016],#save_or_show='hold')
    ##col_map='Blues',cparam=['threshold=',0,'PoI'],
    #pdf=pdf,scaled=True,fig_type=ft,name_fig='156WT') 
#plt_various_masks_yearly_subplots(xparam='WTa',yparam=['dev CH4_S1','NTs10'],years=[2010,2015,2016],#save_or_show='hold')
    #col_map='BrBG',cparam=['threshold=',0,'PoIA'],
    #pdf=pdf,scaled=True,fig_type=ft,name_fig='156PoIA') 

for yy in yys:
    #plt_various_masks_yearly_subplots(xparam='NTs10',yparam='CH4_S1',fit='exp',years=yy,#save_or_show='hold')
        #pdf=pdf,scaled=True,fig_type='pdf pages')
#for yy in yys:

    #plt_various_masks_yearly_subplots(xparam='DoY',yparam='WTa',#cparam=['threshold=',0,'PoI'],
        #fit='exp',years=yy,#col_map='Blues',#save_or_show='hold')
        #col_map='PuOr',cparam=['threshold=',0,'PoIA'],
        #pdf=pdf,scaled=True,fig_type='pdf pages')
    #plt_various_masks_yearly_subplots(xparam='DoY',yparam='WTa',#cparam=['threshold=',0,'PoI'],
        #fit='exp',years=yy,#col_map='Blues',#save_or_show='hold')
        ##col_map='PuOr',cparam=['threshold=',0,'PoIA'],
        #pdf=pdf,scaled=True,fig_type='pdf pages')
    #plt_various_masks_yearly_subplots(xparam='DoY',yparam='WTa',#cparam=['threshold=',0,'PoI'],
        #fit='exp',years=yy,#col_map='Blues',#save_or_show='hold')
        #col_map='coolwarm',cparam='Ts10',
        #pdf=pdf,scaled=True,fig_type='pdf pages')
    plt_various_masks_yearly_subplots(xparam='NTs10',yparam='CH4_S1',#cparam=['threshold=',0,'PoI'],
        fit='exp',years=yy,#col_map='Blues',#save_or_show='hold')
        col_map='PuOr',cparam=['threshold=',0,'PoIA'],
        pdf=pdf,scaled=True,fig_type='pdf pages')
    plt_various_masks_yearly_subplots(xparam='NTs10',yparam='CH4_S1',#cparam=['threshold=',0,'PoI'],
        fit='exp',years=yy,#col_map='Blues',#save_or_show='hold')
        #col_map='PuOr',cparam=['threshold=',0,'PoIA'],
        pdf=pdf,scaled=True,fig_type='pdf pages')
    plt_various_masks_yearly_subplots(xparam='WTa',yparam=['dev CH4_S1','NTs10'],#cparam=['threshold=',0,'PoI'],
        fit='exp',years=yy,#col_map='Blues',#save_or_show='hold')
        col_map='PuOr',cparam=['threshold=',0,'PoIA'],
        pdf=pdf,scaled=True,fig_type='pdf pages')
    #plt_various_masks_yearly_subplots(xparam='WTa',yparam=['dev CH4_S1','NTs10'],#cparam=['threshold=',0,'PoI'],
        #fit='exp',years=yy,#col_map='Blues',#save_or_show='hold')
        ##col_map='PuOr',cparam=['threshold=',0,'PoIA'],
        #pdf=pdf,scaled=True,fig_type='pdf pages')
    plt_various_masks_yearly_subplots(xparam='WTa',yparam=['dev CH4_S1','NTs10'],#cparam=['threshold=',0,'PoI'],
        fit='exp',years=yy,#col_map='Blues',#save_or_show='hold')
        col_map='coolwarm',cparam='Ts10',
        pdf=pdf,scaled=True,fig_type='pdf pages')
#for yy in yys[1:]:
    #plt_various_masks_yearly_subplots(xparam='NTs10',yparam='CH4_S1',cparam=['threshold=',0,'PoA'],
        #fit='exp',years=yy,col_map='Oranges',#save_or_show='hold')
        #pdf=pdf,scaled=True,fig_type='pdf pages')
##for yy in yys:
    #plt_various_masks_yearly_subplots(xparam='WTa',yparam=['dev CH4_S1','NTs10'],
        #fit='lin',scaled=True,
        #years=yy, name_fig=str(yy[-1]),pdf=pdf,fig_type='pdf pages')
##for yy in yys:
    #plt_various_masks_yearly_subplots(xparam='WTa',yparam=['dev CH4_S1','NTs10'],
        #fit='lin',scaled=True,cparam=['threshold=',0,'PoI'],col_map='Blues',
        #years=yy, name_fig=str(yy[-1]),pdf=pdf,fig_type='pdf pages')
##for yy in yys:
    #plt_various_masks_yearly_subplots(xparam='WTa',yparam=['dev CH4_S1','NTs10'],
        #fit='lin',scaled=True,cparam=['threshold=',0,'PoA'],col_map='Oranges',
        #years=yy, name_fig=str(yy[-1]),pdf=pdf,fig_type='pdf pages')
##for yy in yys:
    ##plt_various_masks_yearly_subplots(xparam='WTa',yparam=['dev CH4_S1','NTs10'],
        ##fit='quad',scaled=True,
        ##years=yy, name_fig=str(yy[-1]),pdf=pdf,fig_type='pdf pages')
pdf.close()

#plt.show()


    
    




