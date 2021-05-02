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
        ParaTestValue=np.around(ParaTestValue, decimals=3)                                                                  # Make the decimals of the matrix element to 3 digits
        ParaTestValue_new1=ParaTestValue_new2=[]
        for i in range (len(ParaTestValue[0])):
            ParaTestValue_new1=np.append(ParaTestValue_new1, ParaTestValue[0][i])
            ParaTestValue_new2=np.append(ParaTestValue_new2, ParaTestValue[1][i])
        list1=ParaTestValue_new1.tolist()
        list2=ParaTestValue_new2.tolist()
        ParaTestValue_new='['+str(str(list1)+','+str(list2))+']'
    elif type(ParaTestValue) is np.ndarray:
        ParaTestValue=np.around(ParaTestValue, decimals=3)                                                                   # Make the decimals of the matrix element to 3 digits
        ParaTestValue_new=str([ParaTestValue[0], ParaTestValue[1], ParaTestValue[2]])
    elif type(ParaTestValue) is float or type(ParaTestValue) is int:
        ParaTestValue_new=str(ParaTestValue)
    str_line=DesignParameter_str+'='+ParaTestValue_new
    lines=''
    with open(txtFile_Input_fullpath, 'r+') as f:
        for line in f.readlines():
            if (line.find(DesignParameter_str)==0):
                line=str_line+'\n'
            lines +=line
    with open(txtFile_output_fullpath, 'r+') as f:
        f.writelines(lines)
