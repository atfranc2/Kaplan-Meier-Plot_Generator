# Kaplan-Meier-Plot_Generator
A code snippet for constructing a Kaplan-Meier Plot to support survival analyses

<h2> Example </h2>

Consider a dataset containing data regarding pump faiures during a hurricane. An example of the data is shown in Table 1. 

<b> Table 1: </b> Data used for constructing the Kaplan-Meier plot. The data table is 
stored in _survival_data_

survive |	hour	| reason
------------ | -------------| -------------
1 | 48| 	0
1 | 48| 	0
1 | 48| 	0
1 | 48| 	0
1 | 48| 	0

Now we can use the survival_prob( ... ) function in this repository to construct the plot

```

survival_prob( df = survival_data, target = 'survive', time = 'hour', cencored = 1, group = None, non_fail_id = 0 )
  ''' Will return plots of the survival probability and the conditional failure probability and 
      the data used to construct each '''

```

![Image of the surival and conditional failure probability plots]( https://github.com/atfranc2/Kaplan-Meier-Plot_Generator/blob/master/Survival_prob_plot.png )


