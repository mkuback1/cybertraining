# -*- coding: utf-8 -*-
"""
@author: mkubacki

For use with RF_model.py

input: original RUCdata pandas dataframe (output from read_data_RF.py)

output: RUCdata pandas dataframe with fixed height grid

This function converts the pandas dataframe with varying height levels into
a pandas dataframe with a fixed height grid comprised of the average heights
at each of the 37 levels.  Feature values are interpolated
over the fixed height grid.

Input dataframe (from readRUCsounding)

                   event         temperature    dewpoint  ...  pressure  height 
    0   weakly\ntornadic  [t01 t02 ... t037]       [...]          [...]   [...]
    1   weakly\ntornadic  [t11 t12 ... t137]       [...]          [...]   [...]
    2        nontornadic               [...]       [...]          [...]   [...]
    3        nontornadic               [...]       [...]          [...]   [...]
    4        nontornadic               [...]       [...]          [...]   [...]
    
The function interpolates the RUCsoundings at various height levels to a
fixed vertical grid above ground level.

Output dataframe is

          temp1 temp2 ... temp37 ...  p1  ... p37               event          
    0       t01   t02 ...   t037 ...  p01 ... p037    weakly\ntornadic
    1       t11   t12 ...   t137 ...  p11 ... p137    weakly\ntornadic
    2       t21   t22 ...   t237 ...  p21 ... p237         nontornadic
    3       t31   t32 ...   t337 ...  p31 ... p337         nontornadic
    4       t41   t42 ...   t437 ...  p41 ... p437         nontornadic
    
where the feature entries (e.g. t01, t02) are the interpolated values from the
original feature vector entries [t01,t02,...].
"""


import numpy as np
import pandas as pd

def interpolate_avg_height(RUCdata):
    file_loc = "/umbc/xfs1/cybertrn/cybertraining2020/team8/research/RandomForest/DataInfo/avg_heights.txt"
    avg_height = np.loadtxt(file_loc)
    zlength_features = 6*len(avg_height)
    features = RUCdata.columns[1:7]
    ## initialize 2D array for interpolated RUC soundings
    RUCdata_interp = np.empty([RUCdata.shape[0],zlength_features])

    ## loop through each sounding variable in each file for interpolation 
    for i in range(RUCdata.shape[0]): # loop over storms
        # Height measurements for storm i
        height = np.trim_zeros(RUCdata.at[i,'height'],trim='b')
        # Interpolate for each feature
        k = 0
        for m in features:
            interp_array = np.trim_zeros(RUCdata.at[i,m])
            RUCdata_interp[i,k:k+len(avg_height)]=np.interp(avg_height,height,interp_array)
            k+=len(avg_height)

    # create feature index
    interp_features = []
    for m in features:
        add_int = 0
        for i in range(len(avg_height)):
            add_int+=1
            feature_name = m + ' ' + str(add_int)
            interp_features.append(feature_name)

    RUCdata_interp = pd.DataFrame(data=RUCdata_interp,columns=interp_features)
    RUCdata_interp['event']=RUCdata['event']

    return RUCdata_interp
