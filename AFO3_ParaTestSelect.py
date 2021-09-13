#------------------------------------------------------------------------------------------------------------------------------------------
# Automatically change the AFO materials properties in input file for batch Simulation
# Input:  FL_side_var_amplification: the variables of amplification for the side AFO materials, baseline value times the variables
#            FL_side_var_shift: the variables of shift for the side AFO materials, baseline value add negative variables means shift to left
#            FL_front_var_amplification: the variables of amplification for the front AFO materials, baseline value times the variables
#            FL_front_var_shift: the variables of shift for the front AFO materials, baseline value add negative variables means shift to left
# Output: the new input file that has changed based on the variables
def AFOmaterialVariables(FL_var_amplification, FL_var_shift, Designparameters_str):
    if 'AFO_FLrelationship' in Designparameters_str:
        # Extract AFO_FLrelationship from the input file
        AFO_FLrelationship=ParaTestValue('AFO Design', 'AFO input.txt', Designparameters_str)       # FL relationship for side AFO
        # Get new AFO FL relationship after the modification based on variables
        # New FL relationship for AFO
        AFO_FLrelationship[0]=AFO_FLrelationship[0]+FL_var_shift
        AFO_FLrelationship[1]=AFO_FLrelationship[1]*FL_var_amplification
        # Put the new AFO FL relationship to the new input file
        #ParaValeModification('AFO Design', 'AFO input_default.txt', 'AFO input.txt', Designparameters_str, AFO_FLrelationship)
        ParaValeModification('AFO Design', 'AFO input.txt', 'AFO input.txt', Designparameters_str, AFO_FLrelationship)
        return AFO_FLrelationship
    if 'AFO_stripe_orientations' in Designparameters_str:
        AFO_stripe_orientations=ParaTestValue('AFO Design', 'AFO input.txt', Designparameters_str)       # Stripe orientations for side AFO
        AFO_stripe_orientations=AFO_stripe_orientations+FL_var_amplification
        # Put the new AFO FL relationship to the new input file
        #ParaValeModification('AFO Design', 'AFO input_default.txt', 'AFO input.txt', Designparameters_str, AFO_stripe_orientations)
        ParaValeModification('AFO Design', 'AFO input.txt', 'AFO input.txt', Designparameters_str, AFO_stripe_orientations)

    # Extract AFO_FLrelationship from the input file
    #AFO_FLrelationship_side=ParaTestValue('AFO Design', 'AFO input.txt', 'AFO_FLrelationship_side')       # FL relationship for side AFO
    #AFO_FLrelationship_front=ParaTestValue('AFO Design', 'AFO input.txt', 'AFO_FLrelationship_front')    # FL relationship for front AFO

    """
    # Get new AFO FL relationship after the modification based on variables
    # New FL relationship for side AFO
    AFO_FLrelationship_side[1]=AFO_FLrelationship_side[1]*FL_side_var_amplification
    AFO_FLrelationship_side[0]=AFO_FLrelationship_side[0]+FL_side_var_shift
    # New FL relationship for front AFO
    AFO_FLrelationship_front[1]=AFO_FLrelationship_front[1]*FL_front_var_amplification
    AFO_FLrelationship_front[0]=AFO_FLrelationship_front[0]+FL_front_var_shift
    """
    # Get new AFO FL relationship after the modification based on variables
    # New FL relationship for the new AFO

    # Put the new AFO FL relationship to the new input file
    #ParaValeModification('AFO Design', 'AFO input_default.txt', 'AFO input.txt', 'AFO_FLrelationship_side', AFO_FLrelationship_side)
    #ParaValeModification('AFO Design', 'AFO input.txt', 'AFO input.txt', 'AFO_FLrelationship_front', AFO_FLrelationship_front)
    # ParaValeModification('AFO Design', 'AFO input_default.txt', 'AFO input.txt', FL_var_str, AFO_FLrelationship)
    #
#------------------------------------------------------------------------------------------------------------------------------------------
# Choose a design parameter as parameter test from the design parameter .txt file
# Input:    Input_directory: the folder that include the AFO input design DesignParameters: 'AFO Design'
             #  Input_file: the text file including the design parameters of AFO: AFO input_default.txt
             # DesignParameter_str: the string of the chosen design parameter for parameter test
# Output:  ParaTest_value: the value of the chosen design parameter for parameter test
def ParaTestValue(Input_directory, Input_file, DesignParameter_str):
    import os
    import re
    import numpy as np
    path_script = os.path.realpath(__file__)                                                                                              # The full path for the python scrip folder: python script
    path_simulation=os.path.dirname(os.path.dirname(path_script))                                                       # The path of the folder including the python script: python simulation
    txtFile_fullpath=os.path.join(path_simulation, Input_directory, Input_file)
    dataset=[]
    with open(txtFile_fullpath, "r", encoding="utf-8") as f:
        lines=f.readlines()
    index=0
    for line in lines:
        line=" ".join(line.strip().split('\t'))
        if DesignParameter_str in line:
            DesignParameter_str_Pos=index
        index+=1
        dataset.append(line)
    if '[[' in dataset[DesignParameter_str_Pos] or '],[' in dataset[DesignParameter_str_Pos]:                                                              # If the selected parameter is two matrix, then
        ParaTest_value=re.compile('-?\d+\.*\d*').findall(dataset[DesignParameter_str_Pos])
        ParaTest_value=np.array(ParaTest_value, dtype=np.float).reshape(2,-1)
    elif '[' in dataset[DesignParameter_str_Pos] or ']' in dataset[DesignParameter_str_Pos]:                                                                      # If the selected parameter is matrix, then
        ParaTest_value=re.compile('-?\d+\.*\d*').findall(dataset[DesignParameter_str_Pos])
        ParaTest_value=np.array(ParaTest_value, dtype=np.float)
    else:                                                                                                                        # If the selected parameter is a value, then
        ParaTest_value=float(re.findall(r"\d+\.?\d*",dataset[DesignParameter_str_Pos])[0])
    return ParaTest_value
    #
#------------------------------------------------------------------------------------------------------------------------------------------
# Change the chosen design parameter in the .txt file
# Input:    Input_directory: the folder that include the AFO input design DesignParameters: AFO Design
           #  Input_file: the text file including the design parameters of AFO: AFO input_default.txt
           # DesignParameter_str: the string of the chosen design parameter for parameter test
           # The changed design parameter
def ParaValeModification(Input_directory, Input_file, Output_file, DesignParameter_str, ParaTestValue):
    import os
    import numpy as np
    path_script = os.path.realpath(__file__)                                                                                              # The full path for the python scrip folder: python script
    path_simulation=os.path.dirname(os.path.dirname(path_script))                                                       # The path of the folder including the python script: python simulation
    txtFile_Input_fullpath=os.path.join(path_simulation, Input_directory, Input_file)                            # The path of file for the Input file: AFO input_default
    txtFile_output_fullpath=os.path.join(path_simulation, Input_directory, Output_file)                       # The path of file for the output file: AFO input
    if not os.path.exists(txtFile_output_fullpath):                                                                                     # Chech wheterh the txt file exists or not, if not, create one
        f=open(txtFile_output_fullpath, 'a')
        f.close
    if type(ParaTestValue) is np.ndarray and len(ParaTestValue)==2:
        ParaTestValue=np.around(ParaTestValue, decimals=4)                                                                  # Make the decimals of the matrix element to 3 digits
        ParaTestValue_new1=ParaTestValue_new2=[]
        for i in range (len(ParaTestValue[0])):
            ParaTestValue_new1=np.append(ParaTestValue_new1, ParaTestValue[0][i])
            ParaTestValue_new2=np.append(ParaTestValue_new2, ParaTestValue[1][i])
        list1=ParaTestValue_new1.tolist()
        list2=ParaTestValue_new2.tolist()
        ParaTestValue_new='['+str(str(list1)+','+str(list2))+']'
    elif type(ParaTestValue) is np.ndarray and len(ParaTestValue)==3:
        ParaTestValue=np.around(ParaTestValue, decimals=4)                                                                   # Make the decimals of the matrix element to 3 digits
        ParaTestValue_new=str([ParaTestValue[0], ParaTestValue[1], ParaTestValue[2]])
    elif type(ParaTestValue) is np.ndarray and len(ParaTestValue)==4:
        ParaTestValue=np.around(ParaTestValue, decimals=4)                                                                   # Make the decimals of the matrix element to 3 digits
        ParaTestValue_new=str([ParaTestValue[0], ParaTestValue[1], ParaTestValue[2], ParaTestValue[3]])
    elif type(ParaTestValue) is float or type(ParaTestValue) is int:
        ParaTestValue_new=str(ParaTestValue)
    str_line=DesignParameter_str+'='+ParaTestValue_new
    lines=''
    with open(txtFile_Input_fullpath, 'r+') as f:
        for line in f.readlines():
            if (line.find(DesignParameter_str)==0):
                line=str_line+'\n'
            lines+=line
    with open(txtFile_output_fullpath, 'r+') as f:
        f.truncate(0)
        f.writelines(lines)
    #
