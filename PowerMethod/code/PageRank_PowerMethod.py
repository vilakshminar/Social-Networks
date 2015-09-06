import csv
from collections import Counter
from collections import OrderedDict

srcDir = 'C:\\Stuffs\\Courses\\SocialNetworks\\FinalProject'
myName = 'Ashwin Giridharan'
inputFriendsGraph = '\\mutualfriends.csv'
alpha = 0.65
tolerance = 1.0/10000000000.0


nameToNumMap = {}
numToNameMap = {}

# method to read connection edges from csv file
def readFriendsData():
    numIndex = 0
    edgesList = []
    with open(srcDir + inputFriendsGraph) as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for line in reader:
            if line[0] not in nameToNumMap:
                nameToNumMap[line[0]] = numIndex
                numToNameMap[numIndex] = line[0]
                numIndex += 1
            if line[1] not in nameToNumMap:
                nameToNumMap[line[1]] = numIndex
                numToNameMap[numIndex] = line[1]
                numIndex += 1
            if [nameToNumMap[line[0]], nameToNumMap[line[1]]] not in edgesList:
                edgesList.append([nameToNumMap[line[0]], nameToNumMap[line[1]]])
    print('Total Friends',numIndex)
#     print('My Index',nameToNumMap['Muthurani MI Ashwin'])
    return edgesList,numIndex
 
# Method to rank connections based on Pagerank power method    
def findImpContactsUsingPowerMethod(edgesList, numIndex, alpha, tolerance):
    # Creating zeros array of NxN
    adjMatrix = numpy.zeros(shape=(numIndex,numIndex))
    
    # Populating the edges with 1
    for edge in edgesList:
        adjMatrix[edge[0]][edge[1]] = 1
        adjMatrix[edge[1]][edge[0]] = 1
        
    # Converting matrix to probability / stochastic matrix
    for i in xrange(0,numIndex):
        edgesCount = Counter(adjMatrix[i])[1.0]
        if edgesCount ==0:
            # Skipping handling of zero row as it will not be present
            print('No zero row should be present in Mutual friends data')
        adjMatrix[i] = adjMatrix[i] / edgesCount
#     print('Friend vector before dangle handle',adjMatrix[122])
    
    # Handling dangling nodes by giving them minimum probability
    minProbArray = numpy.ones(shape=(numIndex,numIndex))
    minProbArray = minProbArray / numIndex
    adjMatrix = (alpha * adjMatrix) + ((1-alpha)*minProbArray)
#     print('Friend vector after dangle handle',adjMatrix[122])

    # Power Method
    initialVector = numpy.ones(shape=(1,numIndex))
    initialVector = initialVector / numIndex
    
    stationaryVector = initialVector
    
    expToleranceArray = np.ones(shape=(1,numIndex), dtype=bool)
    
    for i in xrange(0,1000):
        prevStationaryVector = stationaryVector
        stationaryVector = numpy.dot(stationaryVector, adjMatrix)
        toleranceVector = stationaryVector - prevStationaryVector
        currToleranceArray = (toleranceVector < tolerance)
        # Break the loop if tolerance is met
        if numpy.array_equal(currToleranceArray,expToleranceArray):
            print('Tolerance in iteration ',i,'for alpha', alpha,' and tolerance ',tolerance)
            break
        
    contactsWeightMap = {}
    for i in xrange(0,numIndex):
        contactsWeightMap[numToNameMap[i]] = stationaryVector[0][i]
    return OrderedDict(sorted(contactsWeightMap.items(), key=lambda x: x[1], reverse=True))

# Method to rank connections using in-degree or number of mutual friends
def findImpContactsUsingDegree(edgesList, numIndex):
    friendsMutualDegreeMap = {}
    with open(srcDir + '\\mutualfriends.csv') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for line in reader:
            if line[0] != myName:
                if line[0] not in friendsMutualDegreeMap:
                    friendsMutualDegreeMap[line[0]] = 1
                else:
                    friendsMutualDegreeMap[line[0]] = friendsMutualDegreeMap[line[0]] + 1
            if line[1] != myName:
                if line[1] not in friendsMutualDegreeMap:
                    friendsMutualDegreeMap[line[1]] = 1
                else:
                    friendsMutualDegreeMap[line[1]] = friendsMutualDegreeMap[line[1]] + 1
    return OrderedDict(sorted(friendsMutualDegreeMap.items(), key=lambda x: x[1], reverse=True))           
      
# Output ranking comparison of Power Method and in-degree to result file    
def generateRankCompData(impContactsWeightMapPower, impContactsWeightMapDegree, alpha, tolerance):
    powerRankMap = {}
    degreeRankMap = {}
    rankCompList = []
    i = 1
    for key in impContactsWeightMapPower:
        if key != myName:
            powerRankMap[key] = i
            i += 1
    i = 1
    for key in impContactsWeightMapDegree:
        if key != myName:
            degreeRankMap[key] = i
            i += 1
#     print(powerRankMap)
#     print(degreeRankMap) 

    powerRankSortedMap = OrderedDict(sorted(powerRankMap.items(), key=lambda x: x[1]))
#     print(powerRankMap)
    
    rankCompList.append(['Name','PowerRank','DegreeRank','PowerScore','DegreeCount'])
    for key in powerRankSortedMap:
        rankCompList.append([key,powerRankMap[key],degreeRankMap[key],impContactsWeightMapPower[key],impContactsWeightMapDegree[key]])
    
    
    outFile = "rankComp"+str(int(alpha*100.0))+"_"+str(tolerance)+".csv"
    print(outFile)
    with open(srcDir + "\\"+outFile, "wb") as f:
        writer = csv.writer(f)
        writer.writerows(rankCompList)
        
    
                
        
    
def main():            
    edgesList, numIndex = readFriendsData()
    impContactsWeightMapPower = findImpContactsUsingPowerMethod(edgesList, numIndex, alpha, tolerance)
    impContactsWeightMapDegree = findImpContactsUsingDegree(edgesList, numIndex)
    print(len(impContactsWeightMapPower))
    print(len(impContactsWeightMapDegree))
    generateRankCompData(impContactsWeightMapPower, impContactsWeightMapDegree, alpha, tolerance)
    
