class TaskBuilder:
    def __init__(self):
        self.fileName = ''
        self.taskBody = '<Task>\n<Subtasks>\n</Subtasks>\n<Datasets>\n</Datasets>\n</Task>'

    def writeToFile(self, string):
        file = open(self.fileName, 'w')
        file.write(string)

    def save(self):
        if self.fileName == '':
            fileName = 'test_tasks/test_task.xml'
        else:
            fileName = self.fileName
        file = open(fileName, 'w')
        file.write(self.taskBody)
