def getRRAmassoutput(outfile):
    import re
    f = open(outfile,'r').read()
    pos_str_totalmasschange=f.find("Total mass change")
    pattern=re.compile('[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?')
    pattern_Totalmasschange=pattern.findall(f,pos_str_totalmasschange,pos_str_totalmasschange+40)
    Totalmasschange=list(map(float,pattern_Totalmasschange))[0]
    return Totalmasschange

def getModelMass(osimModel):
    totalMass=0
    allBodies=osimModel.getBodySet()
    for i in range(0,allBodies.getSize()):
        currBody=allBodies.get(i)
        totalMass=totalMass+currBody.getMass()
    return totalMass

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
