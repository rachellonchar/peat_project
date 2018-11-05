
#from preamble import *
##import matplotlib.backends.backend_pdf
#from preamble_plot_simple import *
import basic_fit_funcs as btf
import numpy as np



#plt_various_masks_yearly_subplots(xparam='DoY',yparam='WTa',#['dev CH4_S1','NTs10'],
    #years=[2015,20150,2017,20170],scaled=True,leg=0,save_or_show='hold')
#plt_various_masks_yearly_subplots(xparam='DoY',yparam='CH4_S1',#['dev CH4_S1','NTs10'],
    #years=[2015,20150,2017,20170],scaled=True,leg=0,save_or_show='hold')
#plt.show()

def merge1517(arg,dic):
    a1_15,a1_17 = dic[arg][2015],dic[arg][2017]
    a1 = np.append(a1_15,a1_17)
    a2_15,a2_17 = dic[arg][20150],dic[arg][20170]
    a2 = np.append(a2_15,a2_17)
    return a1,a2

def adj_to_newdat(dic,naming):
    args = naming['calls']
    #d1_15,d1_17 = dic['DoY'][2015],dic['DoY'][2017]
    #d1 = np.append(d1_15,d1_17)
    #d2_15,d2_17 = dic['DoY'][20150],dic['DoY'][20170]
    #d2 = np.append(d2_15,d2_17)
    #d1,d2 = v('DoY',441517),v('DoY',4415170)
    d1,d2 = merge1517('DoY',dic)
    indices,indices2 = [],[]
    for idx in range(0,len(d1)):
        for idx2 in range(0,len(d2)):
            if d1[idx]==d2[idx2]:
                if (idx not in indices) and (idx2 not in indices2):
                    indices.append(idx)
                    indices2.append(idx2)
    funD = {}
    for arg in args:
        if arg!='DoY' and arg!='TotDays':
            #a1_15,a1_17 = dic[arg][2015],dic[arg][2017]
            #a1 = np.append(a1_15,a1_17)
            #a2_15,a2_17 = dic[arg][20150],dic[arg][20170]
            #a2 = np.append(a2_15,a2_17)
            a1,a2 = merge1517(arg,dic)

            #a1,a2 = v(ar,441517),v(pp,4415170)
            adj_dic = btf.fit_2sets(a2[indices2],a1[indices])
            fun = adj_dic['function']
        else:
            def fun(ii): return ii
        funD.update({arg:fun})
    return funD,args

def adj_old(dic,naming):
    funD,args = adj_to_newdat(dic,naming)
    for arg in args:
        fun = funD[arg]
        for yr in [2009,2010,2011,2012,2013,2014,20150,20170]:
            a_old = dic[arg][yr]
            a_old_adj = [fun(aa) for aa in a_old]
            dic[arg].update({yr:a_old_adj})
    return dic,naming

#pp='WTa'
#a1,a2 = v(pp,441517),v(pp,4415170)
#adj_dic = btf.fit_2sets(a2[indices2],a1[indices])
#fun = adj_dic['function']


#plt.plot(d1[indices],a1[indices],'r.')
#a2new = [fun(dd) for dd in a2[indices2]]
#plt.plot(d2[indices2],a2new,'b.')
#plt.show()

#print(len(a1),len(a2))
        



    
    




