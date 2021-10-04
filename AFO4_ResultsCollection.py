# output_folder='SimulationOutput_AFO_FLrelationship0'
# Results_parameter=['time', '/jointset/subtalar_r/subtalar_angle_r/value', '/jointset/subtalar_r/subtalar_angle_r/speed']
def Simulationresultscollection(output_folder, Results_parameter, DL_results):
    import numpy as np
    import math
    import os
    # The folder path of pthon script
    path_script = os.path.realpath(__file__)                                                                                              # The full path for the python scrip folder: python script
    path_simulation=os.path.dirname(os.path.dirname(path_script))                                                       # The path of the folder including the python script: python simulation
    # The joining of the folders python simulation, drop landing (DL) and output folders
    #DL_results_directory=os.path.join(path_simulation, 'Drop landing', output_folder)
    DL_results_directory=os.path.join(path_simulation, output_folder)
    #DL_results="default_states_degrees.mot"

    #directory=os.path.join(path, results_directory)
    if not os.path.isdir(DL_results_directory):
        print("No specified directory found, please create one!")
        os.makedirs(DL_results_directory)
        print(DL_results_directory)
        AFO_POI=np.array([])
    results_file_initial=os.path.join(DL_results_directory, DL_results)
    print(results_file_initial)
    if not os.path.exists(results_file_initial):
        print("No specified file found, please check! ")
        AFO_POI=np.array([])
    else:
        npos=[]
        AFO_POI=[]
        with open (results_file_initial,"r",encoding="utf-8") as f:
            lines=f.readlines()
        with open (os.path.join(DL_results_directory,'Results_file_final.txt'),"w",encoding="utf-8") as f_w:
            for line in lines:
                linestr=line.strip()
                if len(linestr)==0:
                    continue
                if linestr.startswith('time'):
                    strlist=linestr.split('\t')
                    for i in range(len(Results_parameter)):
                        npos.append(strlist.index(Results_parameter[i]))
                        f_w.writelines([strlist[npos[i]],"  "])
                    f_w.writelines("\n")
                elif linestr[0].isdigit():
                    strlist=linestr.split('\t')
                    for j in range(len(npos)):
                        f_w.writelines(strlist[npos[j]])
                        AFO_POI.append(float(strlist[npos[j]]))
                    f_w.writelines("\n")
        AFO_POI=np.array(AFO_POI).reshape(-1,len(Results_parameter))
    return AFO_POI

#------------------------------------------------------------------------------------------------------------------------------------------
# Export the MBD simulation results into excel file
# Input: # File_excel_folder: The folder for the MBD results that include the excel file, default='MBD Results'
              # File_excel: the name of the results excel, default='MBD Results'
              # Sheet_name: the name of the sheet, e.g. Sheet_name='SimulationOutput_AFO_FLrelationship0'
              # Results_parameter: the results of interest that will be stored to the excel file, defualt=['time', '/jointset/subtalar_r/subtalar_angle_r/value', '/jointset/subtalar_r/subtalar_angle_r/speed']
              # data: the matrix of data that will be stored into the excel file
def DLResultstoExcel(File_excel_folder, File_excel, Sheet_name, Results_parameter, data):
    import os
    import numpy as np
    import xlwt, xlrd
    from xlutils.copy import copy as xl_copy
    import openpyxl
    # The folder path of pthon script
    path_script = os.path.realpath(__file__)                                                                                              # The full path for the python scrip folder: python script
    path_simulation=os.path.dirname(os.path.dirname(path_script))                                                       # The path of the folder including the python script: python simulation
    # The joining of the folders python simulation, drop landing (DL) and output folders
    DL_results_directory=os.path.join(path_simulation, File_excel_folder)
    if not os.path.isdir(DL_results_directory):
        print("No specified directory found, please create one!")
        os.makedirs(DL_results_directory)
    DL_results_file=os.path.join(DL_results_directory, File_excel)

    if not os.path.exists(DL_results_file):
        f=xlwt.Workbook()
        sheet_name=f.add_sheet('%s' %(Sheet_name), cell_overwrite_ok=True)
    else:
        rb=xlrd.open_workbook(DL_results_file, formatting_info=True)
        f=xl_copy(rb)
        sheet_name=f.add_sheet('%s' %(Sheet_name))

    [h, l]=data.shape
    for i in range(h+1):
        if i==0:
            for j in range(len(Results_parameter)):
                sheet_name.write(i,j,Results_parameter[j])
        else:
            for j in range (l):
                sheet_name.write(i,j,data[i-1,j])
    f.save(DL_results_file)

#------------------------------------------------------------------------------------------------------------------------------------------
# Export the MBD simulation results from the excel file .xls, and pick up important value such as maximum value
# Inputs: # File_folder: the folder that include the results excel file, default='MBD Results'
               # File_excel: the name of the results excel, default='DoE Results.xls'
               # Results_collect_parameters: the results of interest that will be collected from the results excel, default=['time', '/jointset/subtalar_r/subtalar_angle_r/value']
# Output: # Matrix_RoI_max: the matrix that includes the import value of simulation results, as an input for DoE
def DoEResultsfromExcel (File_folder, File_excel, Results_collect_parameters):
    import pandas as pd
    import os
    import numpy as np
    # The folder path of pthon script
    path_script = os.path.realpath(__file__)                                                                                              # The full path for the python scrip folder: python script
    path_simulation=os.path.dirname(os.path.dirname(path_script))                                                       # The path of the folder including the python script: python simulation
    # The joining of the folders python simulation, drop landing (DL) and output folders
    DL_results_directory=os.path.join(path_simulation, 'Drop landing', File_folder)
    if not os.path.isdir(DL_results_directory):
        print("No specified directory found, please check!")
        exit()
    DL_results_file=os.path.join(DL_results_directory, File_excel)
    if not os.path.exists(DL_results_file):
        print('No specific file found, plrease check!')
        exit()
    data=pd.read_excel(DL_results_file, None)
    Matrix_RoI_max=[]
    Matrix_RoI=[]
    for sh_name in data.keys():
        sh_data=pd.DataFrame(pd.read_excel(DL_results_file, sh_name))
        RoI_data=np.array(sh_data[Results_collect_parameters])
        Matrix_RoI.append(RoI_data)
        Matrix_RoI_max.append(RoI_data.max())
    return Matrix_RoI_max

def ReadExcel(Excel_folder, Excel_file, Sheet_name):
    import os
    import pandas as pd
    # The folder path of pthon script
    path_script = os.path.realpath(__file__)                                                                                              # The full path for the python scrip folder: python script
    path_simulation=os.path.dirname(os.path.dirname(path_script))                                                       # The path of the folder including the python script: python simulation
    # The joining of the folders python simulation, drop landing (DL) and output folders
    Excel_file=os.path.join(path_simulation, Excel_folder, Excel_file)
    data=pd.read_excel(Excel_file, sheet_name=Sheet_name)
    return data
