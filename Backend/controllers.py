
def rangos(dataBase, variable):
    if (variable == "Energy Consumed (kWh/yr)") or (variable == "% Run Time (M/M)"):
        return "NA"
    elif variable == "RC Temp Average A°F (M/M)" or (variable == "RC1 Temp °F") or (variable == "RC2 Temp A°F") or (variable == "RC3 Temp A°F"):
        min = 36
        max = 40
    elif variable == "FC Temp Average A°F (M/M)" or (variable == "FC1 Temp A°F") or (variable == "FC2 Temp A°F 2nd P") or (variable == "FC3 Temp A°F 2nd P"):
        min = 0
        max = 4
    elif variable == "% Below Rating Point":
        min = -3
        max = 3
    else:
        return "NA"
    return len(dataBase[(dataBase[variable] >= min) & (dataBase[variable] <= max)])


def famFilter(dataBase, Familia, variable):
    try:
        filter = dataBase[dataBase["Familia"] == Familia]
        filter = filter[[variable]]
        storeFamInfo = []
        storeFamInfo.append(len(filter))
        storeFamInfo.append(filter[variable].mean())
        storeFamInfo.append(filter[variable].mode().iloc[0])
        storeFamInfo.append(filter[variable].median())
        storeFamInfo.append(filter[variable].std())
        storeFamInfo.append(rangos(filter, variable))
        return {'count': storeFamInfo[0],
                'mean': storeFamInfo[1],
                'mode': storeFamInfo[2],
                'median': storeFamInfo[3],
                'std': storeFamInfo[4],
                'withinRange': storeFamInfo[5]}
    except:
        storeFamInfo = ['error']
        return storeFamInfo
