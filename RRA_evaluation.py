def rra_evaluation(path, RRA_directory, RRA_Residuals, RRA_pErr_file):
    import numpy as np
    import math
    import os

    rra_residualF=np.matrix(rra_residual_evaluation(path, RRA_directory, RRA_Residuals, 'F'))
    rra_residualM=np.matrix(rra_residual_evaluation(path, RRA_directory, RRA_Residuals, 'M'))
    Max_residualF=abs(rra_residualF.flat[abs(rra_residualF).argmax()])
    Max_residualM=abs(rra_residualM.flat[abs(rra_residualM).argmax()])
    RMS_residualF=float(np.sqrt(np.vdot(rra_residualF,rra_residualF)/rra_residualF.size))
    RMS_residualM=float(np.sqrt(np.vdot(rra_residualM,rra_residualM)/rra_residualM.size))
    print('Max Residual Force (N):', Max_residualF)
    print('RMS Residual Force (N):', RMS_residualF)
    print('Max Residual Moment (Nm):', Max_residualM)
    print('RMS Residual Moment (Nm):', RMS_residualM)

    RRA_pErr_data=rra_pErr(path, RRA_directory, RRA_pErr_file)
    RRA_pErr_T=RRA_pErr_data[:,1:4]
    RRA_pErr_R=RRA_pErr_data[:,4:len(RRA_pErr_data[:,0])]
    Max_pErr_T=abs(RRA_pErr_T.flat[abs(RRA_pErr_T).argmax()])
    Max_pErr_R=abs(RRA_pErr_R.flat[abs(RRA_pErr_R).argmax()])
    RMS_pErr_T=float(np.sqrt(np.vdot(RRA_pErr_T,RRA_pErr_T)/RRA_pErr_T.size))
    RMS_pErr_R=float(np.sqrt(np.vdot(RRA_pErr_R,RRA_pErr_R)/RRA_pErr_R.size))
    print('Max position error (trans, cm):', Max_pErr_T*100)
    print('RMS position error (trans, cm):', RMS_pErr_T*100)
    print('Max position error (rot, radian):', Max_pErr_R)
    print('Max position error (rot, radian):', RMS_pErr_R)

    Residual_results=[Max_residualF, RMS_residualF, Max_residualM, RMS_residualM]
    pErr_results=[Max_pErr_T*100, RMS_pErr_T*100, Max_pErr_R, RMS_pErr_R]
    return Residual_results, pErr_results

def rra_residual_evaluation(path, Results_directory, Results_file, evaluation_parameter):
    import numpy as np
    import os
    import re
    RRA_results_file=os.path.join(path, Results_directory, Results_file)
    dataset=[]
    with open(RRA_results_file,"r",encoding="utf-8") as f:
        lines=f.readlines()
        for line in lines:
            if line.find(evaluation_parameter)!=-1:
                line=" ".join(line.strip().split('\t'))
                line=float(re.findall(r"-?\d+\.?\d*",line)[0])
                dataset.append(line)
    return dataset

def rra_pErr(path, Results_directory, Results_file):
    import numpy as np
    import math
    import os
    import re
    RRA_results_file=os.path.join(path, Results_directory, Results_file)
    dataset_pErr=[]
    with open(RRA_results_file,"r",encoding="utf-8") as f:
        lines=f.readlines()
        temp=[]
        for line in lines:
            if line.strip()[0].isdigit():
                num=list(map(float,line.split()))
                temp.append(num)
    dataset_pErr=np.array(temp)
    return dataset_pErr
