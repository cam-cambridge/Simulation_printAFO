# output_folder='SimulationOutput_AFO_FLrelationship0'
# Results_parameter=['time', '/jointset/subtalar_r/subtalar_angle_r/value', '/jointset/subtalar_r/subtalar_angle_r/speed']
def Simulationresultscollection(output_folder, Results_parameter, DL_results):
    import numpy as np
    import math
    import os
    import tkinter
    from tkinter import filedialog

    # The folder path of pthon script
    path_script = os.path.realpath(__file__)                                                                                              # The full path for the python scrip folder: Simulation_printAFO
    path_simulation=os.path.dirname(os.path.dirname(path_script))                                                       # The path of the folder including the python script:Simulation_printAFO_CAMG

    # The joining of the folders python simulation, drop landing (DL) and output folders
    #DL_results_directory=os.path.join(path_simulation, 'Drop landing', output_folder)
    # previous code
    # DL_results_directory=output_folder
    #DL_results="default_states_degrees.mot"
    DL_results_directory=os.path.join(path_simulation, output_folder)

    #directory=os.path.join(path, results_directory)
    if not os.path.isdir(DL_results_directory):
        print(DL_results_directory)
        print("No specified directory found, please create one!")
        os.makedirs(DL_results_directory)
        AFO_POI=np.array([])
    results_file_initial=os.path.join(DL_results_directory, DL_results)
    # print(results_file_initial)
    if not os.path.exists(results_file_initial):
        print(results_file_initial)
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
    #import xlsxwriter
    from xlutils.copy import copy as xl_copy
    import openpyxl
    # Previous code
    """
    # The folder path of pthon script
    path_script = os.path.realpath(__file__)                                                                                              # The full path for the python scrip folder: python script
    path_simulation=os.path.dirname(os.path.dirname(path_script))                                                       # The path of the folder including the python script: python simulation
    """
    # The joining of the folders python simulation, drop landing (DL) and output folders
    # DL_results_directory=os.path.join(path_simulation, File_excel_folder)
    DL_results_directory=File_excel_folder
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
def curvecomparison(data1, data2, Results_parameter_i, n):
    #------------------------------------------------------------------------------------------------------------------------------------------
    # Compare 2 cuves generated from the 2 datasets, and calculate the total and average differences between the two datasets
    # Input: data1: the points datasets for curve 1
    #            data2: the points datasets for curve 2
    #            Results_parameter_i: the i th parameters in the matrix - Results_parameter
    #            n:        the number of interpolation points in the curve
    import numpy as np
    import matplotlib.pyplot as plt
    from scipy import interpolate
    #------------------------------------------------------------------------------------------------------------------------------------------
    # Interpolation of data 1 and data 2
    f_data1=interpolate.interp1d(data1[:,0],data1[:,Results_parameter_i])
    f_data2=interpolate.interp1d(data2[:,0],data2[:,Results_parameter_i])
    # The new x and y values for the interpolation data for data 1 and data 2
    xnew_data1=np.arange(min(data1[:,0]), max(data1[:,0]), (max(data1[:,0])-min(data1[:,0]))/n)
    ynew_data1=f_data1(xnew_data1)
    xnew_data2=np.arange(min(data2[:,0]), max(data2[:,0]), (max(data2[:,0])-min(data2[:,0]))/n)
    ynew_data2=f_data2(xnew_data2)
    """
    # plot the orginal curve and interpolation curve
    plt.plot(data1[:,0],data1[:,Results_parameter_i],'-', xnew_data1, ynew_data1, 'o', data2[:,0],data2[:,Results_parameter_i],'-', xnew_data2, ynew_data2, 'o')
    plt.plot(data1[:,0],data1[:,Results_parameter_i],'*', data2[:,0],data2[:,Results_parameter_i],'*')
    plt.plot(xnew_data1, abs(ynew_data1-ynew_data2), '-')
    plt.show()
    """
    diff_total=np.sum(abs(ynew_data1-ynew_data2))
    diff_average=np.sum(abs(ynew_data1-ynew_data2))/n
    diff_max=max(abs(ynew_data1-ynew_data2))
    return diff_total, diff_average, diff_max
def Excel3Dplot(sheet_name, xs_variable, ys_variable, zs_variable):
    import pandas as pd
    import tkinter
    from tkinter import filedialog
    from mpl_toolkits.mplot3d import Axes3D
    import matplotlib.pyplot as plt
    # Open and select the destinated file
    root =tkinter.Tk()                                                      # Open the dialog of the file
    root.withdraw()
    SelectionFile=filedialog.askopenfilename()                       # the path of the selected file
    data=pd.read_excel(SelectionFile, sheet_name=sheet_name)

    fig=plt.figure()
    ax=fig.add_subplot(111,projection='3d')
    for c, m, cm in [('b', '*', 'rainbow')]:
        xs=data[xs_variable].to_list()
        ys=data[ys_variable].to_list()
        zs=data[zs_variable].to_list()
        ax.scatter(xs,ys,zs,c=zs,marker=m, cmap=cm)

    ax.set_xlabel(xs_variable)
    ax.set_ylabel(ys_variable)
    ax.set_zlabel(zs_variable)
    plt.show()
def ExcelMatrixCollection(sheet_name, ParameterOfInterest1, ParameterOfInterest2, ParameterOfInterest3):
    import pandas as pd
    import tkinter
    from tkinter import filedialog
    from mpl_toolkits.mplot3d import Axes3D
    import matplotlib.pyplot as plt
    # Open and select the destinated file
    root =tkinter.Tk()                                                      # Open the dialog of the file
    root.withdraw()
    SelectionFile=filedialog.askopenfilename()                       # the path of the selected file
    data=pd.read_excel(SelectionFile, sheet_name=sheet_name)
    POI1=data[ParameterOfInterest1].to_list()
    POI2=data[ParameterOfInterest2].to_list()
    POI3=data[ParameterOfInterest3].to_list()
    POI=[POI1, POI2, POI3]
    return POI
def ExcelObjectiveFunction(sheet_name_activity1, sheet_name_activity2, sheet_name_activity3, merge_variables):
    import pandas as pd
    import tkinter
    from tkinter import filedialog
    import math
    # Open and select the destinated file
    root =tkinter.Tk()                                                      # Open the dialog of the file
    root.withdraw()
    SelectionFile=filedialog.askopenfilename()                       # the path of the selected file
    data_activity1=pd.read_excel(SelectionFile, sheet_name=sheet_name_activity1)
    root =tkinter.Tk()                                                      # Open the dialog of the file
    root.withdraw()
    SelectionFile=filedialog.askopenfilename()                       # the path of the selected file
    data_activity2=pd.read_excel(SelectionFile, sheet_name=sheet_name_activity2)
    root =tkinter.Tk()                                                      # Open the dialog of the file
    root.withdraw()
    SelectionFile=filedialog.askopenfilename()                       # the path of the selected file
    data_activity3=pd.read_excel(SelectionFile, sheet_name=sheet_name_activity3)

    data_synchonized_1=pd.merge(data_activity2, data_activity3,  how='left', on=[merge_variables])
    data_synchonized_1['Objective function1']=abs(data_synchonized_1['Gait_subtalar difference'])+abs(data_synchonized_1['Gait_ankle difference'])+abs(data_synchonized_1['Run_subtalar difference'])+abs(data_synchonized_1['Run_ankle difference'])

    data_synchonized_2=pd.merge(data_synchonized_1, data_activity1,  how='left', on=[merge_variables])
    data_synchonized_2['Objective function2']= data_synchonized_2['Objective function1']+math.exp(data_synchonized_2['DL_Max_subtalar']-37)

    root =tkinter.Tk()                                                      # Open the dialog of the file
    root.withdraw()
    SelectionFile=filedialog.askdirectory()
    data_synchonized_2.to_excel(filedialog.asksaveasfilename())
