#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 22 10:54:50 2020

@author: Jane Hsieh (Hsing-Chuan, Hsieh)

@article:
    Generate random sample of dice (with Faif and Loaded dice used interchangeably)
"""
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

os.getcwd()



#0. ================================================ Functions ===============================================

def InitialState(pi_0=0.5):
    '''
    function to generate initial state S_0 out of {F,L} of the dice with prob-p(S_0=F) = p(F)=pi_0 (0:F; 1:L)
    Input: 
        pi_0: defaul= 0.5 which is the initial prob of hiddent state p(S_0 = 0)  [0: fair dice; 1: Loaded dice]
                (pi1 := p(S_0 = 1) = 1-pi_0)
    Output:
        S_0: initial generated hidden state
    ''' 
    S_0 = np.random.choice(2, 1, p=[pi_0, 1-pi_0])[0] #Default: replace=True
    return S_0
    

    
def EmitObs(S_t, Dice, pF, pL):
    '''
    function to generate observation O_t according to the mechanism of hidden state S_t --> Emit Observation
    Input:
        S_t: current hidden state
        Dice: face point of dice, e.g., [1,2,...,6]
        pF: distributions of Fair Dice, say, with point = [1,2,...,6]
        pL: distributions of Loaded Dice, say, with point = [1,2,...,6]
    '''
    if S_t == 0:
        #Fair dice state with prob = pF
        O_t = np.random.choice(Dice, 1, replace=True, p=pF)[0]
    if S_t == 1:
        #Loaded dice state with prob = pL
        O_t = np.random.choice(Dice, 1, replace=True, p=pL)[0]
    return O_t


def TransitState(S_t, p01, p10):
    '''
    function to generate the new hidden state S_t according to the mechanism of previous hidden state S_t
    Input:
        S_t: current hidden state
        p01: Transition prob from 0(F) to 1(L)); p00 =  1- p01
        p10: Transition prob from 1(L) to 0(F); p11 = 1-p10
    '''
    if S_t == 0:
        #Fair dice state with prob = pF
        S_new = np.random.choice(2, 1, replace=True, p=[1-p01, p01])[0]
    if S_t == 1:
        #Loaded dice state with prob = pL
        S_new = np.random.choice(2, 1, replace=True, p=[p10, 1-p10])[0]
    return S_new 
    


def GenerateFLDice(N, p01, p10, pL, pF=[1/6 for i in range(6)], Dice = [i+1 for i in range(6)], pi_0=0.5, seed=None):
    '''
    Generate random sample of dice (with predefined Fair(F) and Loaded(L) dice used interchangeably)
    
    Input:
        N: sample size
        seed: random seed– None or int
        Dice: face point of the dice; default = [1,2,...,6]
        pF, pL: distributions of Fair vs Loaded Dice (length of pF, pL must be the same with Dice)
        pi_0: initial probability of hidden state S_0 – p(S_0 = 0)  [0: fair dice; 1: Loaded dice]
        p01, p10: Transition prob of hidden state from 0(F) to 1(L)) & from 1(L) to 0(F), respectively
    Output:
        Sample_S: sequence of hidden states {S_t} from t=0,...,N-1
        Sample_O: sequence of observations {O_t} from t=0,...,N-1

    '''
    np.random.seed(seed) 
    Sample_S = []
    Sample_O = []
    
    t=0
    # Generate initial hidden state S_t & the Observed state O_t out of it
    S_t = InitialState(pi_0)
    O_t = EmitObs(S_t, Dice, pF, pL)
    
    Sample_S.append(S_t)
    Sample_O.append(O_t) 
    
    t += 1
    
    while t < N:        
        #Generate New S_t at next time (i.e., t+1) point according to previous mechanism of S_t; 
        #and O_t out of New S_t
        S_t = TransitState(S_t, p01, p10)
        O_t = EmitObs(S_t, Dice, pF, pL)
        
        Sample_S.append(S_t)
        Sample_O.append(O_t) 
        
        t += 1
        
    return Sample_S, Sample_O
        

#1. =============== Set parameters for sampling & those of Hidden Markov Model(HMM) =============================
## Sampling-related parameters
seed = 123
N = 5000  #sample size


## HMM-related parameters
pi_0 = 0.5 # initial prob of hiddent state p(S_0 = 0)  [0: fair dice; 1: Loaded dice]; p(S_0=1) = 1-pi_0
p01 = 0.05  # Transition prob from 0(F) to 1(L)); p00 =  1- p01
p10 = 0.05  # Transition prob from 1(L) to 0(F); p11 = 1-p10


### Emission probs: pF vs pL are distributions of Fair vs Loaded Dice  with point = [1,2,...,6], respectively
### Note: length of Dice, pF, pL must be the same
Dice = [i+1 for i in range(6)]
pF = [1/6 for i in range(6)]
pL=[0.1, 0.1, 0.1, 0.1, 0.1, 0.5]


#2. ============================= Generate sequence of {O_t}, {S_t} from t=0,...,N-1 ==================== 
## To reproduce the experiment, seed is fixed; o.w. you can set seed = None for fully random gereration
Sample_Hid, Sample_Obs  = GenerateFLDice(N=N, p01=p01, p10=p10, pL=pL, pF=pF, Dice = Dice, pi_0=pi_0, seed=seed)
#or equal to below:
#Sample_Hid, Sample_Obs = GenerateFLDice (N=N, p01=p01, p10=p10, pL=pL, seed=seed, pi_0 = pi_0)

Sample_Hid  = pd.Series(Sample_Hid, name = 'State')
Sample_Obs = pd.Series(Sample_Obs, name = 'Observation')

# Output data
Sample_Obs.to_csv('Sample_Obs.csv')
Sample_Hid.to_csv('Sample_Hid.csv')


## Data Visualization --------------------------------------------------------------------------------------------
data = pd.concat([Sample_Hid,Sample_Obs],axis=1)


def plot_timeseries(axes, x, y, color, xlabel, ylabel, linestyle='-', marker='None'):  
    axes.plot(x, y, color=color, linestyle = linestyle, marker = marker, ms = 2)  
    axes.set_xlabel(xlabel)  
    axes.set_ylabel(ylabel, color=color)  
    axes.tick_params('y', colors=color)

n= 200
sample = data[:n]

fig, ax = plt.subplots(figsize = (10,5))
plot_timeseries(ax, sample.index, sample['Observation'],'blue', 'index', 'Dice Observations', linestyle='None', marker='o')
ax2 = ax.twinx()
plot_timeseries(ax2, sample.index, sample['State'],'orange', 'index', 'Hidden States')
ax2.set_yticks([0,1])
ax.set_title('First {} cases of dice sequence'.format(n))
plt.show()

fig.savefig('First {} cases of dice sequence.png'.format(n), dpi = 300)










