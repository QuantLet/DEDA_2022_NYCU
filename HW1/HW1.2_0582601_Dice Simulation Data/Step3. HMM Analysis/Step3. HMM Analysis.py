#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 29 11:27:17 2020

@author: jane_hsieh

Article:
    1. For package of HMM– hmmlearn please refers to its tutorial:
        https://hmmlearn.readthedocs.io/en/latest/tutorial.html
    2. More example, refer to <Hidden Markov Model>
        https://medium.com/@kangeugine/hidden-markov-model-7681c22f5b9
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#====================== 0. Input: Observation O_t, and true Hidden states (for comparison) ===================================

import Generate_Dice_Sample as GDice
#0.1.---------------- Set parameters for sampling & those of Hidden Markov Model(HMM) -------------------------------- 

## Sampling-related parameters
seed = 123 # integer or None (i.e., random)
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


#2.0.------------------------ Generate sequence of {O_t}, {S_t} from t=0,...,N-1 ------------------------
## To reproduce the experiment, seed is fixed; o.w. you can set seed = None for fully random gereration
Hid, Obs  = GDice.GenerateFLDice(N=N, p01=p01, p10=p10, pL=pL, pF=pF, Dice = Dice, pi_0=pi_0, seed=seed)

Hid = pd.DataFrame(Hid, columns=['Hid'])
Obs = pd.DataFrame(Obs, columns=['Obs'])

#Obs.to_csv('Sample_Obs.csv')
#Hid.to_csv('Sample_Hid.csv')

## Data Visualization --------------------------------------------------------------------------------------------
data = pd.concat([Hid, Obs],axis=1)


def plot_timeseries(axes, x, y, color, xlabel, ylabel, linestyle='-', marker='None'):  
    axes.plot(x, y, color=color, linestyle = linestyle, marker = marker, ms = 1.6)  
    axes.set_xlabel(xlabel)  
    axes.set_ylabel(ylabel, color=color)  
    axes.tick_params('y', colors=color)

n= 300
sample = data[:n]
del data

fig, ax = plt.subplots(figsize = (10,5))
plot_timeseries(ax, sample.index, sample['Obs'],'blue', 'index', 'Dice Observations', linestyle='None', marker='o')
ax2 = ax.twinx()
plot_timeseries(ax2, sample.index, sample['Hid'],'orange', 'index', 'Hidden States')
ax2.set_yticks([0,1])
ax.set_title('First {} cases of dice sequence'.format(n))
plt.show()

fig.savefig('First {} cases of dice sequence.png'.format(n), dpi = 300)




#======================================== 1. Model Training and Prediction ==================================================
from hmmlearn import hmm

##load model– MultinomialHMM which is Hidden Markov Model with multinomial (discrete) emissions
model = hmm.MultinomialHMM(n_components=2, algorithm='viterbi', n_iter=1000, tol=0.001)
'''
    n_components: #{hidden states}
'''

##Training and Prediction of Hidden states
model.fit(Obs)
Hid_pre = model.predict(Obs)
logprob = model.score(Obs) #log-probability of sequence Obs

'''
To prevent local maximum of EM algorithm, the model is trained for several times (it = 0,...,10), 
each time with random initial parameter values.
The finest model with the highest log-probability of sequence Obs is choosed and reported at last
'''
for it in range(10):
    model1 = hmm.MultinomialHMM(n_components=2, algorithm='viterbi', n_iter=1000, tol=0.001)
    model1.fit(Obs) 
    logprob1 = model1.score(Obs)
    print('[{}] compare logprob ={} vs. logprob1={}'.format(it, logprob, logprob1))
    if logprob1 > logprob:
        model = model1
        logprob = model.score(Obs)
        print('model updated')
    
Hid_pre = model.predict(Obs)
print('The possible highest log-probability found in all iteration is: {}'.format(logprob))





'''
## To make consistent of the symbols of Hid_pre with Hid, transform the symbols of Hid_pre as follows:
temp = list(map(lambda x: 0 if x==1 else 1, Hid_pre))
'''

##Monitoring convergence of EM algorithm
print(model.monitor_)
'''
ConvergenceMonitor(
    history=[-853.4456094067322, -853.4359720533312],
    iter=62,
    n_iter=1000,
    tol=0.01,
    verbose=False,
)
'''
##Does the algorithm converge?
print("Does the algorithm converge? \n",model.monitor_.converged) #True

# ---------------------------------------------------------------------------------------------------------------------------------------
# --------------------------- Problem 1. [Evaluation] Given a known model what is the likelihood of sequence Obs happening? ----------------------
import math
logprob = model.score(Obs)
print("The prob with seq. Obs given the fitted model is {}".format(math.exp(logprob)))

## Suppose new seq. X, compute its prob.
X = np.array([1,6,6,4]).reshape(-1, 1)
logprobX = model.score(X)
print("The prob with seq.–{} given the fitted model is {}".format(X.tolist(), math.exp(logprobX)))


# ---------------------------------------------------------------------------------------------------------------------------------------
# --------------------------- Problem 2. [Decoding] Given a known model and sequence Obs, what is the optimal hidden state sequence? ------------
logprob, Hid_pre = model.decode(Obs)
print("The prob with seq. Obs given the fitted model is {}".format(math.exp(logprob)))

## Suppose new seq. X, compute its prob.
logprobX, seq = model.decode(X)
print("The prob with seq.–{}  given the fitted model is {}".format(X.tolist(), math.exp(logprobX)))

temp = pd.concat([Hid, pd.DataFrame(Hid_pre, columns=['Hid_pre'])], axis = 1)


## Check prediction accuracy
'''
### confusion matrix
#Notice:  check if the labels from true hidden seq. (Hid) are consistent with those form predicted seq. (Hid_pre)
#If yes:
conf_mat = pd.crosstab(Hid.values.squeeze(), Hid_pre, 
                       rownames=['True'], 
                       colnames=['Predicted'], 
                       margins = True)
#o.w., as below:
Hid = Hid.squeeze().map(lambda x: 1 if x==0 else 0)  #Now 0=Loaded dice, 1=Fair dice
conf_mat = pd.crosstab(Hid, Hid_pre, 
                       rownames=['True'], 
                       colnames=['Predicted'], 
                       margins = True)

                     
print('Confusion matrix: \n', conf_mat)
### acc
from sklearn.metrics import accuracy_score
acc = accuracy_score(Hid, Hid_pre)
print('Accuracy: \n', acc)
'''


#????????????????????????????????????????????????????
#temp.plot(linestyle='None', markersize = 10.0)
#plt.show()


# ---------------------------------------------------------------------------------------------------------------------------------------
#---------------------------- Problem 3. [Learning] Given sequence Obs and number of hidden states, what is the optimal model which maximizes the probability of O?-------
#Initial state occupation distribution 
print("Estimated initial state occupation distribution: \n {} \n".format( model.startprob_))
#Matrix of transition probabilities between states. dim= (n_components, n_components)
print("Estimated matrix of transition probabilities between states: \n {} \n".format(model.transmat_ ))
#Probability of emitting a given symbol when in each state. dim= ((n_components, n_features))
print("Probability of emitting a given symbol when in each state \n {}".format(model.emissionprob_))





