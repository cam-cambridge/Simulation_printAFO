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
