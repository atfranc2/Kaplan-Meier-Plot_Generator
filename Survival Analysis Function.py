#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np 
import scipy.stats as stats
import matplotlib.pyplot as plt


# In[12]:


### This function will perform a grouped or single survival probability analysis 
    # The function takes as input: 
        # df = Table containing all nessesary survival data 
        # target = the binary varaible indicating if failure occured or not
        # time = column with the time of failure or cencorship 
        # cencored = numberical indicator that censorship of an observation has occured, 
        # Group = columns containing group id's to break survival fuctions down by

def survival_prob( df, target = 'survive', time = 'hour', cencored = 1, group = None, non_fail_id = 0 ):
    
    if group == None:
    
        df = df[[target, time]]
        
        #Number of observaions that are in the risk set (i.e. rk)
        risk_set = len( df )
        
        #Get the points in times where failure and censorship occur
        fail_times = df[ time ].unique()
        
        # This will create a list of failure times in the range of failre times in the dataset
        # This is required so that no times are skipped over
        fail_times = [i for i in range( 0, max(fail_times)+1 )]

        s_hat = 1

        surv_probs = [1]
        
        #Create a list to store the conditional failure probabilities        
        conditional_fail_prob = [0]

        for i in range(1, len(fail_times)):

            #Get only rows at the current failure time
            event_set = df[df[time] == fail_times[i]]

            #Get the number of events at the current failure time (i.e. dk )
            events = len( event_set )

            #Get the number of non-censored events at the failure time
            known_fails = len( event_set[ event_set[target] != cencored ] )

            #Calculate the surival probability at the current failure time
            s_hat = surv_probs[i-1] * (1 - ( known_fails / risk_set ))
            
            #Append the current value of the survival probability to the list
            surv_probs.append(s_hat)
            
            #Append the current conditional failure probability to the list
            conditional_fail_prob.append( known_fails / risk_set )
            
            #Remove events that have just occured from the risk set
            risk_set = risk_set - events
        
        #Plot the survival curve
        plt.plot(surv_probs)
        plt.xlim(0,50)
        plt.ylim(0,1.1)
        plt.xlabel('Tenure (Hours)')
        plt.ylabel('Survival Probability')
        plt.title('Survival Probability Over the Duration of the Storm')
        plt.grid()
        plt.show()
        
        #Plot the conditional failure probability
        plt.plot(conditional_fail_prob)
        plt.xlim(0,50)
        plt.ylim(0, max(conditional_fail_prob) * 1.02)
        plt.xlabel('Tenure (Hours)')
        plt.ylabel('Conditional Failure Probability')
        plt.title('Hazard Probability Over the Duration of the Storm')
        plt.grid()
        plt.show()
        
        return s_hat
            
    else:
        
        df = df[[ target, time, group ]]
        
        groups = df[ group ].unique()
        
        groups = groups[ groups != non_fail_id ]
        
        s_hat_group = []
        
        #Create a list to store the conditional failure probabilities        
        conditional_fail_prob_group = []
        
        #Create list that will store information needed in the test for differences between survival curves
        risk_numbers_list = []
        event_numbers_list = []
        
        for group_id in groups: 
            
            # Aggregate the observations from a group into a single dataframe
            group_df = df[ ( df[ group ] == group_id ) ]
            
            #Number of observaions that are in the risk set (i.e. rk)
            risk_set = len( group_df )

            #Get the points in times where failure and censorship occur
            fail_times = group_df[ time ].unique()

            # This will create a list of failure times in the range of failre times in the dataset
            # This is required so that no times are skipped over
            fail_times = [i for i in range( 0, max( fail_times )+1 )]

            s_hat = 1

            surv_probs = [ 1 ]
            
            conditional_fail_prob = [ ]
            
            risk_numbers = [ ]
            
            event_numbers = [ ]

            for i in range(1, len(fail_times)):

                #Get only rows at the current failure time
                event_set = group_df[ group_df[ time ] == fail_times[ i ] ]

                #Get the number of events at the current failure time (i.e. dk )
                events = len( event_set )

                #Get the number of non-censored events at the failure time
                known_fails = len( event_set[ event_set[ target ] != cencored ] )

                #Calculate the surival probability at the current failure time
                s_hat = surv_probs[ i-1 ] * (1 - ( known_fails / risk_set ))

                #Append the current value of the survival probability to the list
                surv_probs.append( s_hat )

                #Append the current conditional failure probability to the list
                conditional_fail_prob.append( known_fails / risk_set )
                
                risk_numbers.append( risk_set )
                
                event_numbers.append( events )
                
                #Remove events that have just occured from the risk set
                risk_set = risk_set - events
                
            s_hat_group.append( surv_probs )
            
            conditional_fail_prob_group.append( conditional_fail_prob )
            
            risk_numbers_list.append( risk_numbers )
            
            event_numbers_list.append( event_numbers )
        
        #Plot the survival curve
        for l in s_hat_group:
            plt.plot(l)
            
        plt.legend( groups )
        plt.xlim(0,50)
        plt.ylim(0,1.1)
        plt.xlabel('Tenure (Hours)')
        plt.ylabel('Survival Probability')
        plt.title('Survival Probability Over the Duration of the Storm')
        plt.grid()
        plt.show()
        
        #Plot the conditional probability of failure
        for l in conditional_fail_prob_group:
            plt.plot(l)
            
        plt.legend( groups )
        plt.xlim(0,50)
        #plt.ylim(0,1.1)
        plt.xlabel('Tenure (Hours)')
        plt.ylabel('Survival Probability')
        plt.title('Conditional Failure Probability Over the Duration of the Storm')
        plt.grid()
        plt.show()
        
        
    
        return [ risk_numbers_list, event_numbers_list ]

ss = survival_prob(data, group = 'reason', non_fail_id = 0)

#ss = survival_prob(data)


