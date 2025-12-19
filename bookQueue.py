import math
class BookQueue:
    def __init__(self):
        self.name = ''
        self.volume = 0
        self.queue = 1
        self.volumeList = []

    def setVolume(self, volume):
        self.volume = volume
    
    def getVolume(self):
        temp = self.volume
        self.volume = 0
        return temp

    def setName(self, name):
        self.name = name
    
    def getName(self):
        return self.name

    def setLine(self, line):
        self.queue = line

    def getLine(self):
        temp = self.queue
        self.queue = 1
        return temp

    def getVolumeByBookId(self, bookId):
        for volume in self.volumeList:
            if volume.getId() == bookId:
                return volume
        volume = volumeForInsert(bookId)
        self.volumeList.append(volume)
        return volume

    def setContents(self, contentDict):
        volume = self.getVolumeByBookId(contentDict['bookId'])
        return volume.setContents(contentDict=contentDict), volume
            
    def getContents(self, bookId):
        for i in range(len(self.volumeList)):
            if self.volumeList[i].getId() == bookId:
                return self.volumeList.pop(i).getContents()
    
    
class volumeForInsert:
    def __init__(self, id):
        self.id = id
        self.contents = {
            "chunkIndex" : []
        }
    
    def getId(self):
        return self.id
    
    def checkSetContents(self):
        chunkList = self.contents['chunkIndex']
        totalChunk = self.contents['totalChunk']
        return math.floor((int(len(chunkList)) * 100) / totalChunk)
    
    def setContents(self, contentDict):
        for key in contentDict.keys():
            if key == "chunkIndex":
                self.contents["chunkIndex"].append(contentDict[key])
            else :
                self.contents[key] = contentDict[key]
        return self.checkSetContents()
    
    def getContents(self):
        temp = self.contents.copy()
        self.contents = {}
        return temp
    
    
