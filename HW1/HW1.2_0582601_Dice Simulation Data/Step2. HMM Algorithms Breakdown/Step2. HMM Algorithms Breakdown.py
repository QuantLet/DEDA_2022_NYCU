#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 10:48:04 2020

@author: jane_hsieh
"""
import numpy as np
import pandas as pd
#============================================== 0. Input ==============================================
# Observation O_t
Obs = pd.read_csv('Sample_Obs.csv', index_col = 0).values.reshape(-1,).tolist()
Obs = Obs[:100]

#Parameters
Obs_state = {str(i+1): i for i in range(6)} #name: index
Hid_state = {'F': 0, 'L': 1}                #name: index
pF = [1/6 for i in range(6)]
pL=[0.1, 0.1, 0.1, 0.1, 0.1, 0.5]

## HMM-related parameters
Pi = np.array([0.5, 0.5])   # initial probs of hidden states {0, 1}  [0: fair dice; 1: Loaded dice]; p(S_0=1) = 1-pi_0
P = np.array([[0.95, 0.05], [0.05, 0.95]]) #Transition matrix T = [p_{i,j}] = [p(Sj|Si)]
E = np.array([pF,pL]) #Emission matrix E = [q_i^y] = [p(O=y|S=i)]



#============================================== 1. Alpha ==============================================

def Build_Alpha(Obs, Pi, P, E):
    '''
    Use Forward Algorithm to compute Alpha (dim=TxK)
    Alpha = [alpha_1, ..., alpha_T]^T, alpha_t = [alpha_t^0, ..., alpha_t^{K-1}]^T
    Issue: if T too large, Alpha_t --> 0 as t--> T
    '''
    T = len(Obs)
    K = len(Pi)
    Alpha = np.zeros([T,K]) 
    
    #Initial:
    index_E = Obs_state[str(Obs[0])]
    Alpha[0] = Pi * E[:, index_E]
    
    #Iterate:
    for t in range(1,T):
        index_E = Obs_state[str(Obs[t])]
        Alpha[t] = np.dot(Alpha[t-1], P) * E[:, index_E]
        
    return Alpha


Alpha = Build_Alpha(Obs, Pi, P, E)

Evaluation = Alpha[-1].sum()

#============================================== 2. Beta ==============================================
def Build_Beta(Obs, Pi, P, E):
    '''
    Use Backward Algorithm to compute Beta (dim=TxK)
    Beta = [beta_1, ..., beta_T]^T, beta_t = [beta_t^0, ..., beta_t^{K-1}]^T
    '''
    T = len(Obs)
    K = len(Pi)
    Beta = np.zeros([T,K]) 
    
    #Initial:
    Beta[T-1] = np.ones(K)
    
    #Iterate:
    for t in range(T-2,-1,-1):
        index_E = Obs_state[str(Obs[t+1])]
        Beta[t] = np.dot(Beta[t+1] * E[:, index_E], P.T)
    
    return Beta
    
Beta = Build_Beta(Obs, Pi, P, E)

#Termination:
# Decoding1 matrix is p(S_t=k|{O_t}_{t=1}^T)
Decoding1 = Alpha * Beta
Decoding1 = Decoding1 / Decoding1.sum(axis =1)[:, np.newaxis]

Seq_Decoding1 = Decoding1.argmax(axis = 1)

#============================================== 3. Viterbi & Traceback ==================================================
def Build_Viterbi(Obs, Pi, P, E):
    '''
    Use Viterbi Algorithm to compute V (dim=TxK)
    V = [V_1, ..., V_T]^T, V_t = [V_t^0, ..., V_t^{K-1}]^T
    '''
    T = len(Obs)
    K = len(Pi)
    V = np.zeros([T,K]) 
    
    #Initial:
    index_E = Obs_state[str(Obs[0])]
    V[0] = Pi * E[:, index_E]
    
    #Iterate:
    for t in range(1,T):
        index_E = Obs_state[str(Obs[t])]
        V[t] =   (V[t-1].reshape(-1,1) * P).max(axis=0)  * E[:, index_E]
        
    return V

V = Build_Viterbi(Obs, Pi, P, E)

def Viterbi_Traceback(V):
    '''
    find most likely assignment of state sequence (i.e., Seq_Decoding2)
    '''
    T, K = V.shape
    Seq_Decoding2 = np.zeros(T)
    
    #Termination:
    Seq_Decoding2[T-1] = V[T-1].argmax()
    
    #Iterate:
    for t in range(T-1,0,-1):
        index_P = int(Seq_Decoding2[t] )
        Seq_Decoding2[t-1] = (V[t-1] * P[:, index_P]).argmax()
        
    return Seq_Decoding2


Seq_Decoding2 = Viterbi_Traceback(V)




    