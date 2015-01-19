
def lowerCaseString(entityName):
    nameLen = len(entityName)
    if nameLen > 0:
        return entityName[0].lower() + entityName[1:nameLen]
    else:
        return entityName
