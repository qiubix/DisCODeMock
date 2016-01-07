class TaskBuilder:
    def __init__(self):
        self.fileName = ''

    def writeToFile(self, string):
        file = open(self.fileName, 'w')
        file.write(string)
