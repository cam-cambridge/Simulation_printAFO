# get the mass change distribution from the output file
def getRRAmassoutput(outfile):
    import re
    f = open(outfile,'r').read()
    pos_str_totalmasschange=f.find("Total mass change")
    pattern=re.compile('[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?')
    pattern_Totalmasschange=pattern.findall(f,pos_str_totalmasschange,pos_str_totalmasschange+40)
    Totalmasschange=list(map(float,pattern_Totalmasschange))[0]
    return Totalmasschange

# The mass change after RRA
def setBodyMassUsingRRAMassChange(osimModel,massChange):
    currTotalMass=getModelMass(osimModel)
    NewTotalMass=currTotalMass+massChange
    massScaleFactor=NewTotalMass/currTotalMass

    allBodies=osimModel.getBodySet()
    for i in range(0,allBodies.getSize()):
        currBodyMass=allBodies.get(i).getMass()
        newBodyMass=currBodyMass*massScaleFactor
        allBodies.get(i).setMass(newBodyMass)
    osimModel_rraMassModification=osimModel
    return osimModel_rraMassModification

def getModelMass(osimModel):
    totalMass=0
    allBodies=osimModel.getBodySet()
    for i in range(0,allBodies.getSize()):
        currBody=allBodies.get(i)
        totalMass=totalMass+currBody.getMass()
    return totalMass

def ScaleOptimalForceSubjectSpecific(osimModel_generic, osimModel_scaled, height_generic, height_scaled):
    mass_model_generic=getModelMass(osimModel_generic)
    mass_model_scaled=getModelMass(osimModel_scaled)

    Vtotal_generic = 47.05 * mass_model_generic * height_generic + 1289.6
    Vtotal_scaled = 47.05 * mass_model_scaled * height_scaled + 1289.6

    allMuscles_generic = osimModel_generic.getMuscles()
    allMuscles_scaled = osimModel_scaled.getMuscles()

    for i in range (0, allMuscles_generic.getSize()):
        currentMuscle_generic = allMuscles_generic.get(i)
        currentMuscle_scaled = allMuscles_scaled.get(i)
        lmo_generic = currentMuscle_generic.getOptimalFiberLength()
        lmo_scaled = currentMuscle_scaled.getOptimalFiberLength()
        forceScaleFactor = (Vtotal_scaled / Vtotal_generic) / (lmo_scaled / lmo_generic)

        currentMuscle_scaled.setMaxIsometricForce ( forceScaleFactor * currentMuscle_generic.getMaxIsometricForce( ) )
    osimModel_scaledForces = osimModel_scaled
    return osimModel_scaledForces

def setMaxContractionVelocityAllMuscles(osimModel, maxContractionVelocity):
    Muscles = osimModel.getMuscles()

    for i in range (0, Muscles.getSize()):
        currentMuscle = Muscles.get(i)
        currentMuscle.setMaxContractionVelocity(maxContractionVelocity)
    osimModel_vmax = osimModel
    return osimModel
