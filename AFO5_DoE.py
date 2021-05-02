# Perform MBD simulation for the DoE, the MBD model is based on the design parameters after the DoEFactorLevel.
# Input:  Level_A: the level for the force-length relationship for AFO in side (amplification): Level_A==1: high level, Level_A==0: low
            # Level_B: the level for the force-length relationship for AFO in side (shift)
            # Level_C: the level for the force-length relationship for AFO in front (amplification)
            # Level_D: the level for the force-length relationship for AFO in side (shift)
            # Operation: the operation of the MBD model, Operation='model': display the MBD model, Operation='simulation': run MBD simulation and save the results
            # ResultDirectory: the folder that saves the simulation results
# Output: Generate the simulation results files in the results folder.
def DoESimulation (Level_A, Level_B, Level_C, Level_D, Operation, ResultDirectory):
    import AFO0_Simulation
    DoEFactorLevel (Level_A, Level_B, Level_C, Level_D)
    AFO0_Simulation.Simulation('AFODroplanding', Operation, ResultDirectory)

#---------------------------------------------------------------------------------------------------------------------------------------------
# Definte the factor levels and then change the parameters of the factor in the input file AFO input_default.txt.
# Input:  Level_A: the level for the force-length relationship for AFO in side (amplification): Level_A==1: high level, Level_A==0: low
            # Level_B: the level for the force-length relationship for AFO in side (shift)
            # Level_C: the level for the force-length relationship for AFO in front (amplification)
            # Level_D: the level for the force-length relationship for AFO in side (shift)
# Output: Generate a new input file of the design parameters AFO input.txt. The file will be used in the MBD model
def DoEFactorLevel(Level_A, Level_B, Level_C, Level_D):
    import AFO3_ParaTestSelect
    # The level for the force-length relationship for AFO in side (amplification) (low: level=-1, high: level=1)
    AFO_FLrelationship_side=AFO3_ParaTestSelect.ParaTestValue('AFO Design', 'AFO input_default.txt', 'AFO_FLrelationship_side')
    AFO_FLrelationship_front=AFO3_ParaTestSelect.ParaTestValue('AFO Design', 'AFO input_default.txt', 'AFO_FLrelationship_front')
    if Level_A==0:                                                       # low level
        AFO_FLrelationship_side[1]=AFO_FLrelationship_side[1]*3
    elif Level_A==1:                                                      # high level
        AFO_FLrelationship_side[1]=AFO_FLrelationship_side[1]*60

    # The level for the force-length relationship for AFO in side (shift) (low: level=-1, high: level=1)
    if Level_B==0:                                                       # low level
        AFO_FLrelationship_side[0]=AFO_FLrelationship_side[0]
    elif Level_B==1:                                                      # high level
        AFO_FLrelationship_side[0]=AFO_FLrelationship_side[0]-0.4

    # The level for the force-length relationship for AFO in side (amplification) (low: level=-1, high: level=1)
    if Level_C==0:
        AFO_FLrelationship_front[1]=AFO_FLrelationship_front[1]*3
    elif Level_C==1:
        AFO_FLrelationship_front[1]=AFO_FLrelationship_front[1]*60

    # The level for the force-length relationship for AFO in front (shift) (low: level=-1, high: level=1)
    if Level_D==0:                                                       # low level
        AFO_FLrelationship_front[0]=AFO_FLrelationship_front[0]
    elif Level_D==1:                                                      # high level
        AFO_FLrelationship_front[0]=AFO_FLrelationship_front[0]-0.4

    AFO3_ParaTestSelect.ParaValeModification('AFO Design', 'AFO input_default.txt', 'AFO input.txt', 'AFO_FLrelationship_side', AFO_FLrelationship_side)
    AFO3_ParaTestSelect.ParaValeModification('AFO Design', 'AFO input.txt', 'AFO input.txt', 'AFO_FLrelationship_front', AFO_FLrelationship_front)

# Calculate the main effects and develop regression model
# Inputs: # input_labels: the lables for the design parameters factors
               # factors_value: the values for high and low levels of factors
               # Simulation_results: the simulation results to generate the design matrix
def StatiAna(inputs_labels, factors_value, Simulation_results):
    import pandas as pd
    import numpy as np
    from numpy.random import rand
    import itertools
    #-----------------------------------------------------------------------------------------------------------------------
    inputs_df = pd.DataFrame(factors_value,columns=['index','low','high'])
    inputs_df = inputs_df.set_index(['index'])
    inputs_df['label'] = inputs_df.index.map( lambda z : inputs_labels[z] )
    #-----------------------------------------------------------------------------------------------------------------------
    inputs_df['average']      = inputs_df.apply( lambda z : ( z['high'] + z['low'])/2 , axis=1)
    inputs_df['span']         = inputs_df.apply( lambda z : ( z['high'] - z['low'])/2 , axis=1)
    inputs_df['encoded_low']  = inputs_df.apply( lambda z : ( z['low']  - z['average'] )/( z['span'] ), axis=1)
    inputs_df['encoded_high'] = inputs_df.apply( lambda z : ( z['high'] - z['average'] )/( z['span'] ), axis=1)
    inputs_df = inputs_df.drop(['average','span'],axis=1)
    #------------------------------------------------------------------------------------------------------------------------
    encoded_inputs = list( itertools.product([-1,1],[-1,1],[-1,1],[-1,1]))
    results=encoded_inputs
    for i in range (len(encoded_inputs)):
        results[i]=np.append(results[i], Simulation_results[i])
        results[i]=tuple(results[i])
    results_df = pd.DataFrame(results,columns=['x1','x2','x3','x4','y'])
    # results_df['logy'] = results_df['y'].map( lambda z : z)
    print(results_df)
    #--------------------------------------------------------------------------
    real_experiment = results_df
    var_labels = []
    for var in ['x1','x2','x3','x4']:
        var_label = inputs_df.loc[var]['label']
        var_labels.append(var_label)
        real_experiment[var_label] = results_df.apply(
            lambda z : inputs_df.loc[var]['low'] if z[var]<0 else inputs_df.loc[var]['high'] ,
            axis=1)

    #--------------------------------------------------------------------------
    # Computing main effects
    # Compute the mean effect of the factor on the response,
    # conditioned on each variable
    labels = ['x1','x2','x3','x4']
    main_effects = {}
    SS_maineffects={}
    for key in labels:
        effects = results_df.groupby(key)['y'].mean()
        main_effects[key] = sum( [i*effects[i] for i in [-1,1]] )
        # The effects of factors: main_effects=(2/(n*pow(2,k)))*contrast
        # Sum of squres: SS=(1/(n*pow(2,k)))*contrast
        # So, sum of squares: SS=(n*pow(2,k)/4)*pow(main_effects,2)
        # In this case, SS=4*pow(main_effects,2), giving that n=1, k=4
        SS_maineffects[key]=4*(main_effects[key]**2)
    print('main_effects=')
    print(main_effects)

    # two-way interactions
    twoway_labels = list(itertools.combinations(labels, 2))
    twoway_effects = {}
    for key in twoway_labels:
        key1=list(key)
        effects = results_df.groupby(key1)['y'].mean()
        twoway_effects[key] = sum([ i*j*effects[i][j]/2 for i in [-1,1] for j in [-1,1] ])
        # This somewhat hairy one-liner takes the mean of a set of sum-differences
        #twoway_effects[key] = mean([  sum([ i*effects[i][j] for i in [-1,1] ]) for j in [-1,1]  ])
    print('twoway_effects=')
    print(twoway_effects)

    # three-way interactions
    threeway_labels = list(itertools.combinations(labels, 3))
    threeway_effects = {}
    for key in threeway_labels:
        key1=list(key)
        effects = results_df.groupby(key1)['y'].mean()
        threeway_effects[key] = sum([ i*j*k*effects[i][j][k]/4 for i in [-1,1] for j in [-1,1] for k in [-1,1] ])
    print('threeway_effects=')
    print(threeway_effects)

    # four-way interactions
    fourway_labels = list(itertools.combinations(labels, 4))
    fourway_effects = {}
    for key in fourway_labels:
        key1=list(key)
        effects = results_df.groupby(key1)['y'].mean()
        fourway_effects[key] = sum([ i*j*k*l*effects[i][j][k][l]/8 for i in [-1,1] for j in [-1,1] for k in [-1,1]for l in [-1,1]])
    print('fourway_effects=')
    print(fourway_effects)

    # Fitting a polynomial response surface
    s = "yhat = "
    s += "%0.3f "%(results_df['y'].mean())

    for mi, mk in enumerate(main_effects.keys()):
        if (main_effects[mk]<-1):
            s += "%0.3f %s "%( main_effects[mk]/2.0, mk)
        elif (main_effects[mk]>1):
            s += "+ %0.3f %s "%( main_effects[mk]/2.0, mk)
    for di, dk in enumerate(twoway_effects.keys()):
        if (twoway_effects[dk]<-1):
            s += "%0.3f %s "%( twoway_effects[dk]/2.0, dk)
        elif (twoway_effects[dk]>1):
            s += "+%0.3f %s "%( twoway_effects[dk]/2.0, dk)
    for ti,tk in enumerate(threeway_effects.keys()):
        if (threeway_effects[tk]<-1):
            s += "%0.3f %s "%( threeway_effects[tk]/2.0, tk)
        elif (threeway_effects[tk]>1):
            s += "+%0.3f %s "%( threeway_effects[tk]/2.0, tk)
    for fi, fk in enumerate(fourway_effects.keys()):
        if (fourway_effects[fk]<-1):
            s += "%0.3f %s"%( fourway_effects[fk]/2.0, fk)
        elif (fourway_effects[fk]>1):
            s += "+%0.3f %s"%( fourway_effects[fk]/2.0, fk)
    return s
