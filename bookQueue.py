class BookQueue:
    def __init__(self):
        self.name = ''
        self.volume = 0
        self.queue = 1

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

