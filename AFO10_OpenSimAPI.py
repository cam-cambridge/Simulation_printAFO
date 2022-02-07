import AFO0_Simulation
import AFO1_DesignParameter
import os
import AFO2_MBDModel
import AFO3_ParaTestSelect
import numpy as np
import AFO4_ResultsCollection
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import math
import AFO_Simulation_Optimization
import opensim

"""
# Display the MSK model based on the provided solution (design variables)
solution = [[30, 101, 259, 326], [-40, 0, 0, 50], [20.34, 21.20, 13.18, 18.9], [30, 100, 100, 30]]
AFO_Simulation_Optimization.Main_model_demo (solution, 0)
"""

# Load the model
osimModel='D:\Drop landing\Fullbodymodel_droplanding_AFO.osim'
myModel=opensim.Model(osimModel)
state=myModel.initSystem()
# Load the .mot file generated by the simulation
motSto=opensim.Storage('D:\Drop landing\DL simulation results\\11.mot')
nmotSto=motSto.getSize()
timeStep=motSto.getMinTimeStep()
coords=myModel.getCoordinateSet()
ncoords=coords.getSize()

# Update each model coordinate for each frame
for j in range (1, nmotSto):
    for i in range (4, ncoords-13):
        coordvalue=opensim.ArrayDouble()
        currentcoord=coords.get(i)
        motSto.getDataColumn(currentcoord.getName(), coordvalue)
        q=coordvalue.getitem(j-1)
        #if strcmp('Rotational', char(currentcoord, getMotionType())):
        if 'Rotational'==str(currentcoord.getMotionType()):
            q=deg2rad(q)
        myModel.updCoordinateSet().get(i).setValue(state, q)
    myModel.realizePosition(state)
    # Access ligament in models forceset & get ligament length after safedoncast
    fset=myModel.getForceSet().get("orthosis_1")
    strap1=opensim.Ligament.safeDownCast(fset)
    #strap1=opensim.Ligament.safeDownCast(fset.get("orthosis_1"))
    strap1_length=strap1.getLength(state)
    strap1_FL=strap1.get_force_length_curve(state)
    print(strap1_FL)

#myModel.printToXML("D:\Drop landing\Fullbodymodel_droplanding_AFO1.osim")

"""
osimModel='D:\Drop landing\Fullbodymodel_droplanding_AFO.osim'
myModel=opensim.Model(osimModel)
reporter=opensim.ConsoleReporter()
reporter.set_report_time_interval (0.05)
fset=myModel.getForceSet()
strap1=opensim.Ligament.safeDownCast(fset.get("orthosis_1"))
reporter.addToReport(strap1.getLength())
"""

"""
osimModel='D:\Drop landing\Fullbodymodel_droplanding_AFO.osim'
myModel=opensim.Model(osimModel)
fset=myModel.getForceSet()
strap1=opensim.Ligament.safeDownCast(fset.get("orthosis_1"))
strap2=opensim.Ligament.safeDownCast(fset.get("orthosis_2"))
strap3=opensim.Ligament.safeDownCast(fset.get("orthosis_3"))
strap4=opensim.Ligament.safeDownCast(fset.get("orthosis_4"))

state=myModel.initSystem()
strap_length=[strap1.getLength(state), strap2.getLength(state), strap3.getLength(state), strap4.getLength(state)]
print(strap_length)
"""

"""
>>> myModel=getCurrentModel()
>>> fset=myModel.getForceSet()
>>> lig=modeling.Ligament.safeDownCast(fset.get("orthosis_1"))
>>> state=myModel.initSystem()
>>> length=lig.getLength(state)
>>> length
0.12603247926090794
>>>
"""
