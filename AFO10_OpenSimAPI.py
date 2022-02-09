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


# Set and update the path to the local OpenSim geometry directory
path='C:\OpenSim 4.1\Geometry'
opensim.ModelVisualizer.addDirToGeometrySearchPaths(path)
# Load the model
osimModel='D:\Drop landing\Fullbodymodel_droplanding_AFO.osim'
myModel=opensim.Model(osimModel)
state=myModel.initSystem()
# Load the .mot file generated by the simulation
motSto=opensim.Storage('D:\Drop landing\DL simulation results\\11.mot')
nmotSto=motSto.getSize()   # The number of the time instances
timeStep=motSto.getMinTimeStep() # Get the smallest time step
coords=myModel.getCoordinateSet()
ncoords=coords.getSize()    # Get the number of coordinates in the model, including coordinates of forceset, such as BackBushing et al.

# Update each model coordinate for each time frame
nmotSto_num=2    # The number of time instances selected
nmotSto_interval=int(nmotSto/nmotSto_num)   # The number of intervals for the time instances
print(nmotSto_interval)
for j in range (1,nmotSto_num):
    #for i in range (13, ncoords-11):        # update coordinate from knee to ankle
    for i in range (12, ncoords-11):
        coordvalue=opensim.ArrayDouble()
        currentcoord=coords.get(i).getName()
        currentcoord_fullname='/jointset/'+currentcoord.replace('_angle_', '_').replace('_rotation_', '_')+'/'+currentcoord+'/value'
        motSto.getDataColumn(currentcoord_fullname, coordvalue)
        #motSto.getDataColumn('/jointset/subtalar_r/subtalar_angle_r/value', coordvalue)
        #q=coordvalue.getitem((j-1)*nmotSto_interval)
        q=coordvalue.getitem(j*nmotSto_interval)
        #if 'Rotational'==str(currentcoord.getMotionType()):  # If the rotational angle is in degree, convert to radian
        #    q=deg2rad(q)
        myModel.updCoordinateSet().get(i).setValue(state, q)
    myModel.realizePosition(state)
myModel.printToXML("D:\Drop landing\Fullbodymodel_droplanding_AFO1.osim")

"""
    myModel.computeStateVariableDerivatives(state)
    # Access ligament in models forceset & get ligament length after safedoncast
    fset=myModel.getForceSet()
    strap1=opensim.Ligament.safeDownCast(fset.get("orthosis_2"))
    strap1_length=strap1.getLength(state)
    #strap1_tension=strap1.getTension(state)
    print(strap1_length)
    #print(strap1_tension)
    #print(strap1)
#myModel.printToXML("D:\Drop landing\Fullbodymodel_droplanding_AFO1.osim")
"""



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
path='C:\OpenSim 4.1\Geometry'
opensim.ModelVisualizer.addDirToGeometrySearchPaths(path)
osimModel='D:\Drop landing\Fullbodymodel_droplanding_AFO.osim'
myModel=opensim.Model(osimModel)
fset=myModel.getForceSet()
strap1=opensim.Ligament.safeDownCast(fset.get("orthosis_1"))
strap2=opensim.Ligament.safeDownCast(fset.get("orthosis_2"))
strap3=opensim.Ligament.safeDownCast(fset.get("orthosis_3"))
strap4=opensim.Ligament.safeDownCast(fset.get("orthosis_4"))
state=myModel.initSystem()
myModel.computeStateVariableDerivatives(state)
strap_length=[strap1.getLength(state), strap2.getLength(state), strap3.getLength(state), strap4.getLength(state)]
print(strap_length)
tension=[strap1.getTension(state), strap2.getTension(state), strap3.getTension(state), strap4.getTension(state)]
print(tension)
"""
