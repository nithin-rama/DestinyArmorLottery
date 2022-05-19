import requests

# dictionary to hold extra headers
HEADERS = {"X-API-Key":'93bbdc4a2531442d92fa17c21917a9b8'}

#shorten URLS into variables
baseURL = "https://www.bungie.net/platform/Destiny2/Manifest/"
entity = ["DestinyInventoryItemDefinition/", "DestinyPlugSetDefinition/"]

class plugSet:    
    def __init__(self, plugSetHash):
        self.plugSetHash = plugSetHash


    # get json object of plugSet with given plugSetHash
    def getPlugSet(self):
        r = requests.get(baseURL + entity[1] + str(self.plugSetHash), headers=HEADERS)
        plugSet = r.json()

        return plugSet

    # get list of possible stats of a given plugSet
    def getPlugSetStats(self):
        plugSet = self.getPlugSet()

        statList = []

        for p in range(len(plugSet['Response']['reusablePlugItems'])):
            plugItemHash = plugSet['Response']['reusablePlugItems'][p]['plugItemHash']

            #pull plug with given hash
            r = requests.get(baseURL + entity[0] + str(plugItemHash), headers=HEADERS)
            plugItem = r.json()

            #loop through stats and add values to 
            stat = []
            for d in range(3):
                stat.append(plugItem['Response']['investmentStats'][d]['value'])
            statList.append(stat)
        
        return statList

class inventoryItem:
    def __init__(self, itemNum):
        self.itemNum = itemNum

    # get json object of item with given itemNum
    def getItem(self):

        # pull item from api 
        r = requests.get(baseURL + entity[0] + str(self.itemNum), headers=HEADERS)
        inventoryItem = r.json()

        return inventoryItem

    # display name and item num of item with given itemNum
    def displayItemDetails(self):

        inventoryItem = self.getItem()
        name = inventoryItem['Response']['displayProperties']['name']

        # print name, num
        print("Item name: " + name + " (" + str(self.itemNum) + ")")

    # get list of 4 plug sets hashes of item with given itemNum
    def getItemPlugSets(self):

        inventoryItem = self.getItem()

        #loop through socket entries 6-9 and add plug set hashes to socketEntry[]
        socketEntry = []

        for e in range(4):
            if inventoryItem['Response']['sockets']['socketEntries'][e+6]['plugSources'] == 0:
                socketEntry.append(str(inventoryItem['Response']['sockets']['socketEntries'][e+6]['randomizedPlugSetHash']))
            else:
                socketEntry.append("X")

        return socketEntry

    def displayItemStats(self):

        inventoryItem = self.getItem()

        #loop through socket entries 6-9 and add plug set hashes to socketEntry[]
        socketEntry = []

        for e in range(4):
            socketEntry.append(str(inventoryItem['Response']['sockets']['socketEntries'][e+6]['randomizedPlugSetHash']))

            #pull plug set with given hash
            r = requests.get(baseURL + entity[1] + socketEntry[e], headers=HEADERS)
            plugSet = r.json()

            #loop through plug set (up to 63 each) and add plug hash to plug[]
            plug = []

            for p in range(len(plugSet['Response']['reusablePlugItems'])):
                plug.append(plugSet['Response']['reusablePlugItems'][p]['plugItemHash'])

                #pull plug with given hash
                r = requests.get(baseURL + entity[0] + str(plug[p]), headers=HEADERS)
                plugItem = r.json()

                #loop through stats and add values to 
                stat = []
                for d in range(3):
                    stat.append(plugItem['Response']['investmentStats'][d]['value'])

                if e < 2:
                    print("%2d: %2d | %2d | %2d | %2d | %2d | %2d (total = %d)" % (p, stat[0], stat[1], stat[2], 0, 0, 0, stat[0]+stat[1]+stat[2]))
                else:
                    print("%2d: %2d | %2d | %2d | %2d | %2d | %2d (total = %d)" % (p, 0, 0, 0, stat[0], stat[1], stat[2], stat[0]+stat[1]+stat[2]))

def simplifiedPlugSets():
    for i in range(len(itemNums)):
        currentItem = inventoryItem(itemNums[i])
        name = currentItem.getItem()['Response']['displayProperties']['name']
        socketEntry = currentItem.getItemPlugSets()

        # print(name + " " + str(socketEntry))
        if socketEntry[0] == "520381962":
            socketEntry[0] = "5"
        if socketEntry[1] == "520381962":
            socketEntry[1] = "5"

        if socketEntry[0] == "1204797486":
            socketEntry[0] = "1"
        if socketEntry[1] == "1204797486":
            socketEntry[1] = "1"

        if socketEntry[2] == "4163334830":
            socketEntry[2] = "4"
        if socketEntry[3] == "4163334830":
            socketEntry[3] = "4"

        if socketEntry[2] == "2445569938":
            socketEntry[2] = "2"
        if socketEntry[3] == "2445569938":
            socketEntry[3] = "2" 
        print("%-30s (%10d): %s | %s | %s | %s " % (name, itemNums[i], socketEntry[0], socketEntry[1], socketEntry[2], socketEntry[3]))

# simplifiedPlugSets()

# filter 1 | ghost mod for mobility or discipline | mobility or discipline >= 5
def filterGhostMobDis(inputStats):
    print("Mob or Dis (ghost) filter applied")
    outputStats = []
    for i in range(len(inputStats)):
        if inputStats[i][0] >=5:
            outputStats.append(inputStats[i]) 

    return outputStats

# filter 2 | ghost mod for recovery or intellect | recovery or intellect >= 5
def filterGhostRecInt(inputStats):
    print("Rec or Int (ghost) filter applied")
    outputStats = []
    for i in range(len(inputStats)):
        if inputStats[i][1] >=5:
            outputStats.append(inputStats[i]) 

    return outputStats

# filter 3 | ghost mod for resilience or strength | resilience or strength >= 5
def filterGhostResStr(inputStats):
    print("Res or Str (ghost) filter applied")
    outputStats = []
    for i in range(len(inputStats)):
        if inputStats[i][2] >=5:
            outputStats.append(inputStats[i]) 

    return outputStats

# filter 4 | activity filter for mobility or discipline | mobility or discipline >= 10
def filterActivityMobDis(inputStats):
    print("Mob or Dis (activity) filter applied")
    outputStats = []
    for i in range(len(inputStats)):
        if inputStats[i][0] >=10:
            outputStats.append(inputStats[i]) 

    return outputStats

# filter 5 | activity filter for recovery or intellect | recovery or intellect >= 10
def filterActivityRecInt(inputStats):
    print("Rec or Int (activity) filter applied")
    outputStats = []
    for i in range(len(inputStats)):
        if inputStats[i][1] >=10:
            outputStats.append(inputStats[i]) 

    return outputStats

# filter 6 | activity filter for resilience or strength | resilience or strength >= 10
def filterActivityResStr(inputStats):
    print("Res or Str (activity) filter applied")
    outputStats = []
    for i in range(len(inputStats)):
        if inputStats[i][2] >=10:
            outputStats.append(inputStats[i]) 

    return outputStats

# filter 7 | high stat | total plug >=14 
def filterHighStat(inputStats):
    print("HighStat filter applied")
    outputStats = []
    for i in range(len(inputStats)):
        if inputStats[i][0] + inputStats[i][1] + inputStats[i][2] >=14:
            outputStats.append(inputStats[i]) 

    return outputStats

def cleanStats(inputStats):
    print("")
    for i in range(len(inputStats)):
        total = inputStats[i][0] + inputStats[i][1] + inputStats[i][2]
        print("%2d | %2d / %2d / %2d | total = %d" % (i, inputStats[i][0], inputStats[i][1], inputStats[i][2], total))

    return

#Moonfang-X7 Boots
# itemNum = 1781294872

# glove = inventoryItem(itemNum)

# glove.getItem()
# glove.displayItemDetails()
# glove.getItemPlugSets()
# glove.displayItemStats()

# plugSetHash = glove.getItemPlugSets()

# L1 = plugSet(plugSetHash)
# print(L1.getPlugSetStats())

#pyrrhic, iron forerunner, GoA, tusked allegiance don't work

itemNums = [1767106452, 4076604385, 2381337281, 1649346047, 3316852407, 2515293448] # s16 hunter helms

# 1 == 2 and 4 == 5

# base 1
stats1 = [[1, 1, 11], [1, 11, 1], [11, 1, 1], [1, 1, 11], [1, 11, 1], [11, 1, 1], [1, 1, 12], [1, 12, 1], [12, 1, 1], [1, 1, 13], 
[1, 5, 8], [1, 8, 5], [1, 13, 1], [5, 1, 8], [5, 8, 1], [8, 1, 5], [8, 5, 1], [13, 1, 1], [1, 1, 14], [1, 5, 9], 
[1, 6, 8], [1, 8, 6], [1, 9, 5], [1, 14, 1], [5, 1, 9], [5, 9, 1], [6, 1, 8], [6, 8, 1], [8, 1, 6], [8, 6, 1], 
[9, 1, 5], [9, 5, 1], [14, 1, 1], [1, 1, 15], [1, 5, 11], [1, 6, 9], [1, 7, 8], [1, 8, 7], [1, 9, 6], [1, 11, 5], 
[1, 15, 1], [5, 1, 11], [5, 11, 1], [6, 1, 9], [6, 9, 1], [7, 1, 8], [7, 8, 1], [8, 1, 7], [8, 7, 1], [9, 1, 6], 
[9, 6, 1], [11, 1, 5], [11, 5, 1], [15, 1, 1]]

# base 4
stats4 = [[1, 1, 11], [1, 5, 5], [1, 11, 1], [5, 1, 5], [5, 5, 1], [11, 1, 1], [1, 1, 11], [1, 5, 6],[1, 6, 5], [1, 11, 1], 
[5, 1, 6], [5, 6, 1], [6, 1, 5], [6, 5, 1], [11, 1, 1], [1, 1, 12], [1, 5, 7], [1, 6, 6], [1, 7, 5], [1, 12, 1], 
[5, 1, 7], [5, 7, 1], [6, 1, 6], [6, 6, 1], [7, 1, 5], [7, 5, 1], [12, 1, 1], [1, 1, 12], [1, 5, 7], [1, 6, 6], 
[1, 7, 5], [1, 12, 1], [5, 1, 7], [5, 7, 1], [6, 1, 6], [6, 6, 1], [7, 1, 5], [7, 5, 1], [12, 1, 1], [1, 1, 13], 
[1, 5, 8],[1, 8, 5], [1, 13, 1], [5, 1, 8], [5, 8, 1], [8, 1, 5], [8, 5, 1], [13, 1, 1], [1, 1, 13], [1, 5, 8], 
[1, 8, 5], [1, 13, 1], [5, 1, 8], [5, 8, 1], [8, 1, 5], [8, 5, 1], [13, 1, 1], [1, 1, 14], [1, 14, 1], [14, 1, 1], 
[1, 1, 15], [1, 15, 1], [15, 1, 1]]

# 1 mob/dis ghost mod
ghostmobdis4 = [[5, 1, 5], [5, 5, 1], [11, 1, 1], [5, 1, 6], [5, 6, 1], [6, 1, 5], [6, 5, 1], [11, 1, 1], [5
, 1, 7], [5, 7, 1], [6, 1, 6], [6, 6, 1], [7, 1, 5], [7, 5, 1], [12, 1, 1], [5, 1, 7], [5, 7,
 1], [6, 1, 6], [6, 6, 1], [7, 1, 5], [7, 5, 1], [12, 1, 1], [5, 1, 8], [5, 8, 1], [8, 1, 5],
 [8, 5, 1], [13, 1, 1], [5, 1, 8], [5, 8, 1], [8, 1, 5], [8, 5, 1], [13, 1, 1], [14, 1, 1], [
15, 1, 1]]

# 2 rec/int ghost mod
ghostrecint4 = [[1, 5, 5], [1, 11, 1], [5, 5, 1], [1, 5, 6], [1, 6, 5], [1, 11, 1], [5, 6, 1], [6, 5, 1], [1
, 5, 7], [1, 6, 6], [1, 7, 5], [1, 12, 1], [5, 7, 1], [6, 6, 1], [7, 5, 1], [1, 5, 7], [1, 6,
 6], [1, 7, 5], [1, 12, 1], [5, 7, 1], [6, 6, 1], [7, 5, 1], [1, 5, 8], [1, 8, 5], [1, 13, 1]
, [5, 8, 1], [8, 5, 1], [1, 5, 8], [1, 8, 5], [1, 13, 1], [5, 8, 1], [8, 5, 1], [1, 14, 1], [
1, 15, 1]]

# 3 res/str ghost mod
ghostresstr4 = [[1, 1, 11], [1, 5, 5], [5, 1, 5], [1, 1, 11], [1, 5, 6], [1, 6, 5], [5, 1, 6], [6, 1, 5], [1
, 1, 12], [1, 5, 7], [1, 6, 6], [1, 7, 5], [5, 1, 7], [6, 1, 6], [7, 1, 5], [1, 1, 12], [1, 5
, 7], [1, 6, 6], [1, 7, 5], [5, 1, 7], [6, 1, 6], [7, 1, 5], [1, 1, 13], [1, 5, 8], [1, 8, 5]
, [5, 1, 8], [8, 1, 5], [1, 1, 13], [1, 5, 8], [1, 8, 5], [5, 1, 8], [8, 1, 5], [1, 1, 14], [
1, 1, 15]]

# 4 high mob/dis activity
activitymobdis4 = [[11, 1, 1], [11, 1, 1], [12, 1, 1], [12, 1, 1], [13, 1, 1], [13, 1, 1], [14, 1, 1], [15, 1,
1]]

# 5 high rec/int activity
activityrecint4 = [[1, 11, 1], [1, 11, 1], [1, 12, 1], [1, 12, 1], [1, 13, 1], [1, 13, 1], [1, 14, 1], [1, 15,
1]]

# 6 high res/str activity
activityresstr4 = [[1, 1, 11], [1, 1, 11], [1, 1, 12], [1, 1, 12], [1, 1, 13], [1, 1, 13], [1, 1, 14], [1, 1, 1
5]]

# 7 high stat
high4 = [[1, 1, 12], [1, 12, 1], [12, 1, 1], [1, 1, 12], [1, 12, 1], [12, 1, 1], [1, 1, 13], [1, 5, 8
], [1, 8, 5], [1, 13, 1], [5, 1, 8], [5, 8, 1], [8, 1, 5], [8, 5, 1], [13, 1, 1], [1, 1, 13],
 [1, 5, 8], [1, 8, 5], [1, 13, 1], [5, 1, 8], [5, 8, 1], [8, 1, 5], [8, 5, 1], [13, 1, 1], [1
, 1, 14], [1, 14, 1], [14, 1, 1], [1, 1, 15], [1, 15, 1], [15, 1, 1]]

# 1 + 7 high mob/dis
highmobdis4 = [[12, 1, 1], [12, 1, 1], [5, 1, 8], [5, 8, 1], [8, 1, 5], [8, 5, 1], [13, 1, 1], [5, 1, 8], [
5, 8, 1], [8, 1, 5], [8, 5, 1], [13, 1, 1], [14, 1, 1], [15, 1, 1]]

# 2 + 7 high rec/int
highrecint4 = [[1, 12, 1], [1, 12, 1], [1, 5, 8], [1, 8, 5], [1, 13, 1], [5, 8, 1], [8, 5, 1], [1, 5, 8], [
1, 8, 5], [1, 13, 1], [5, 8, 1], [8, 5, 1], [1, 14, 1], [1, 15, 1]]

# 3 + 7 high res/str
highresstr4 = [[1, 1, 12], [1, 1, 12], [1, 1, 13], [1, 5, 8], [1, 8, 5], [5, 1, 8], [8, 1, 5], [1, 1, 13],
[1, 5, 8], [1, 8, 5], [5, 1, 8], [8, 1, 5], [1, 1, 14], [1, 1, 15]]