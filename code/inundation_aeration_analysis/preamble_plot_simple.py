
from preamble import *
import matplotlib.backends.backend_pdf

#def plt_various_masks(xparam='NTs10',yparam='NCH4_S1',fit='lin',thresholds=[0],
    #years=2009,leg=1,
    #pdf=matplotlib.backends.backend_pdf.PdfPages("output.pdf"),
    #name_fig='out',fig_type='svg',
    #save_or_show='show'):
    
    #xparam_y = xparam if type(xparam)==list else [xparam]
    #yparam_y = yparam if type(yparam)==list else [yparam]
    #xparam_y.append(years)
    #yparam_y.append(years)
    #colors = ['y','b','brown']
    #for thres_lev in thresholds:
        #pp=0
        #for mm in [None,['a',thres_lev],['i',thres_lev]]:
            #x,nnx,nnu,nnm = vnu(*ftup(xparam_y),mask=mm)
            #y,nny,nnuy,nnm = vnu(*ftup(yparam_y),mask=mm)
            #plt.scatter(x,y,c=colors[pp],marker='o',edgecolor=colors[pp],alpha=0.6)
            #xold=x
            #pp+=1
        #pp=0
        #for mm in [None,['a',thres_lev],['i',thres_lev]]:
            #x,nx,ux,mn = vnu('Xs',xparam,yparam,fit,years,mask=mm)
            #y,ny,uy,mn = vnu('Ysexp',xparam,yparam,fit,years,mask=mm)
            #mn = 'no mask' if mn=='' else mn
            #plt.plot(x,y,colors[pp],label=mn,lw=3)
            #pp+=1
    ##plt.xlabel(nnx+nnu)
    ##plt.ylabel(nny+nnu)
    ##plt.legend()
    ##plt.tight_layout()
    #fig.text(0.5, 0.04,nnx+nnu, ha='center',fontdict=font)
    #fig.text(0.04, 0.5, nny+nnu, va='center', rotation='vertical',fontdict=font)
    #plt.suptitle('Water table influence on methane emissions,\ndepending on if peatland is inundated or aerated',fontsize=16,fontdict=font)
    #if leg==1:
        #plt.legend(loc=1,ncol=1, fancybox=True,prop={'size':10})
    #plt.tight_layout()
    #plt.subplots_adjust(top=0.9,bottom=.1,left=.13)
    ##--
    #if save_or_show=='show':
        #plt.show()
    #elif save_or_show=='hold':
        #None
    #else:
        #if fig_type=='pdf pages':
            #pdf.savefig(fig)
        #else:
            #plt.savefig(gn(name_fig,sub_dirc='CH4_states',f='.'+fig_type),format=fig_type)

def plt_various_masks_yearly_subplots(xparam='Ts10',yparam='NCH4_S1',cparam='WTa',
    scaled=True,fit='lin',thresholds=[0],years=[11131,11132], leg=1,tempTh=9,
    pdf=matplotlib.backends.backend_pdf.PdfPages("output.pdf"),
    name_fig='out',fig_type='svg',col_map='BrBG',
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
    
    inc_call = inclusive_yr_call(*tuple(years))
    xparam_y.append(inc_call)
    yparam_y.append(inc_call)
    cparam_y.append(inc_call)
    Xx,Yy,Cc = v(*ftup(xparam_y),mask=None), v(*ftup(yparam_y),mask=None),v(*ftup(cparam_y),mask=None)
    maxx = max(abs(max(Cc)), abs(min(Cc)))
    maxD, minD = maxx,-maxx
    norm = matplotlib.colors.Normalize(vmin=minD, vmax=maxD, clip=True)
    mapper = cm.ScalarMappable(norm=norm, cmap=plt.cm.get_cmap(col_map))
    mapper.set_array([])
    miny,maxy = min(Yy),max(Yy)
    minx,maxx = min(Xx),max(Xx)
    #colors=['r','chocolate','r','r']
    colors = ['blue','lightcoral','darkslateblue','chocolate']
    tits = ['warm, wet','warm, dry','cool, wet','cool, dry']
    fitt = ['exp','exp','lin','lin']
    ct = 1
    for year in years:
        plt.subplot(cols,rows,ct)
        xparam_y[-1], yparam_y[-1],cparam_y[-1] = year,year,year
            
        ColorV,nnc,nnuc,nnmc = vnu(*ftup(cparam_y),mask=None)
        
        x,nnx,nnu,nnm = vnu(*ftup(xparam_y),mask=None)
        y,nny,nnuy,nnm = vnu(*ftup(yparam_y),mask=None)
        #bill = [mapper.to_rgba(val) for val in ColorV]
        #plt.scatter(x,y,s=30,c=bill,cmap=mapper,edgecolor=bill,vmin=minD,vmax=maxD)
        for thres_lev in thresholds:
            pp=0
            for mm in [[['c',tempTh],['a',thres_lev]],[['c',tempTh],['i',thres_lev]],[['h',tempTh],['a',thres_lev]],[['h',tempTh],['i',thres_lev]]]:
                x,nnx,nnu,nnm = vnu(*ftup(xparam_y),mask=mm)
                y,nny,nnuy,nnm = vnu(*ftup(yparam_y),mask=mm)
                plt.scatter(x,y,c=colors[pp],marker='o',edgecolor=colors[pp],alpha=0.5)
                pp+=1
            pp=0
            for mm in [[['c',tempTh],['a',thres_lev]],[['c',tempTh],['i',thres_lev]],[['h',tempTh],['a',thres_lev]],[['h',tempTh],['i',thres_lev]]]:
                try:
                    x,nx,ux,mn = vnu('Xs',xparam,yparam,fitt[pp],year,mask=mm)
                    y,ny,uy,mn = vnu('Ysexp',xparam,yparam,fitt[pp],year,mask=mm)
                    mn = 'no mask' if mn=='' else mn
                    plt.plot(x,y,colors[pp],label=tits[pp],lw=2)
                except:
                    None
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

def plt_overlap(*yparams,xparam='TotDays',
    years=[4409170,441518,441113],#[1113,11130], leg=1,
    pdf=matplotlib.backends.backend_pdf.PdfPages("output.pdf"),
    name_fig='out',fig_type='svg',leg=1,
    save_or_show='save'):
    
    cols,rows = len(yparams),1
    fig, ax = plt.subplots(ncols=cols,nrows=rows,  sharex=True, sharey=True, figsize=(17,9))
    yct = 1
    for yparam in yparams:
        xparam_y = xparam if type(xparam)==list else [xparam]
        yparam_y = yparam if type(yparam)==list else [yparam]
        #inc_call = inclusive_yr_call(*tuple(years))
        xparam_y.append(0)
        yparam_y.append(0)
        colors = ['y','b','r']
        marks = ['.','.','.']
        alphs = [1,.6,.3]
        ct = 1
        titlex=''
        plt.subplot(cols,rows,yct)
        for year in years:
            xparam_y[-1], yparam_y[-1] = year,year
            x,nnx,nnu,nnm = vnu(*ftup(xparam_y),mask=None)
            y,nny,nnuy,nnm = vnu(*ftup(yparam_y),mask=None)
            plt.plot(x,y,colors[ct-1]+marks[ct-1],alpha=alphs[ct-1],label=yname(year))
            plt.title(nny)
            plt.ylabel(nnuy)
            if leg==1 and yparam==yparams[-1]:
                plt.legend(loc=4,ncol=3, fancybox=True,prop={'size':9})
            plt.tight_layout()
            titlex += nnx
            ct += 1
        yct += 1
    fig.text(0.5, 0.04,nnx+' '+nnu, ha='center',fontdict=font)
    #fig.text(0.04, 0.5, nnuy, va='center', rotation='vertical',fontdict=font)
    plt.suptitle('Time series',fontsize=16,fontdict=font)
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

yy1 = [44091701113,441518,11130,1113]
yy2 = [2009,2010,2012]#,2014,20150,20170]
yy3 = [2014,20150,20170]
yy4 = [2015,2016,2017,2018]
yys = [yy1,yy2,yy3,yy4]

pdf = matplotlib.backends.backend_pdf.PdfPages("bulk_4statesD_linear_when_cool.pdf")
plt_overlap('Ts10','WTa','CH4_S1',
    pdf=pdf,fig_type='pdf pages')
for yy in yys:
    plt_various_masks_yearly_subplots(xparam='NTs10',yparam='CH4_S1',fit='exp',years=yy,#save_or_show='show')
        pdf=pdf,scaled=True,fig_type='pdf pages')
for yy in yys:
    plt_various_masks_yearly_subplots(xparam='WTa',yparam=['dev CH4_S1','NTs10'],
        fit='lin',scaled=True,
        years=yy, name_fig=str(yy[-1]),pdf=pdf,fig_type='pdf pages')
#for yy in yys:
    #plt_various_masks_yearly_subplots(xparam='WTa',yparam=['dev CH4_S1','NTs10'],
        #fit='quad',scaled=True,
        #years=yy, name_fig=str(yy[-1]),pdf=pdf,fig_type='pdf pages')
pdf.close()


    
    




