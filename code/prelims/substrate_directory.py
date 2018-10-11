import numpy as np
import matplotlib.pyplot as plt
import xlrd
import scipy.special
import scipy.integrate 
from scipy.integrate import quad
import math
import random
import xlwt
import xlrd

#DEFINITION OF SUBSTRATE TYPES
#The mean depth when days with 0 cm of inundation are NOT counted is:
mean_depth = 0.5595273264401741
#The mean interarrival time is:
mean_interarrival_time = 1.6935007385524372

#interception = 0 if lam_0 is given instead of lam
substrate_dict = {'laio_loamy_sand':{'alpha':2, 'lam':.3, 'interception':0, 'T_p':0.5, 'rd':30,
    'k1':3.7*10**(-3), 'k12':3.7*10**(-3), 'y_0':-200, 'psi_s':-1.73351756206248,
    'k_s':100, 'n':.42, 'm':(1/4.38)},#(0) loamy sand laio
                  'ex1_tamea':{'alpha':1.2, 'lam':.3, 'interception':0, 'T_p':0.4, 'rd':20,
    'k1':.007, 'k12':.007, 'y_0':-20, 'psi_s':-11,
    'k_s':31, 'n':.463, 'm':.22},#(1) ex 1 from tamea
                'tamea_everglades_NP46':{'alpha':.95, 'lam':.589, 'interception':0, 'T_p':0.48, 'rd':10,
    'k1':.001, 'k12':.006, 'y_0':0, 'psi_s':-10,
    'k_s':10, 'n':.5, 'm':.2},#(2) everaglades 2 in tamea
                'tamea_everglades_NP62':{'alpha':.97, 'lam':.607, 'interception':0, 'T_p':0.46, 'rd':10,
    'k1':.001, 'k12':.003, 'y_0':-20, 'psi_s':-10,
    'k_s':10, 'n':.5, 'm':.2},#(3) everglades 3 in tamea
                'S2_bog':{'alpha':mean_depth, 'lam':(1/mean_interarrival_time), 'interception':0, 'T_p':0.5, 'rd':10,
    'k1':.001, 'k12':.003, 'y_0':-20, 'psi_s':-10,
    'k_s':10, 'n':.5, 'm':.2}#(4) paramters from s2 bog
                  }
