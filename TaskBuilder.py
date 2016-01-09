from xml.dom.minidom import getDOMImplementation


class TaskBuilder:
    def __init__(self):
        self.fileName = ''
        self.taskBody = ''
        self.document = None

    def writeToFile(self, string):
        file = open(self.fileName, 'w')
        file.write(string)

    def save(self):
        if self.fileName == '':
            fileName = 'test_tasks/test_task.xml'
        else:
            fileName = self.fileName
        file = open(fileName, 'w')
        file.write(self.getTaskBody())

    def createTemplate(self):
        self.document = self.createEmptyDocument()
        topLevelElement = self.getTopLevelElement()
        subtasksElement = self.addSubtasksElement(topLevelElement)
        self.addDataStreams(topLevelElement)
        self.addMainSubtask(subtasksElement)

    def getTopLevelElement(self):
        topLevelElement = self.document.documentElement
        return topLevelElement

    def createEmptyDocument(self):
        DOMimpl = getDOMImplementation()
        document = DOMimpl.createDocument(None, 'Task', None)
        return document

    def addDataStreams(self, topLevelElement):
        datastreamsElement = self.document.createElement('DataStreams')
        topLevelElement.appendChild(datastreamsElement)

    def addMainSubtask(self, subtasksElement):
        mainSubtaskElement = self.document.createElement('Subtask')
        mainSubtaskElement.setAttribute('name', 'Main')
        subtasksElement.appendChild(mainSubtaskElement)

    def addSubtasksElement(self, topLevelElement):
        subtasksElement = self.document.createElement('Subtasks')
        topLevelElement.appendChild(subtasksElement)
        return subtasksElement

    def addExecutor(self, name, period):
        executor = self.document.createElement('Executor')
        executor.setAttribute('name', name)
        executor.setAttribute('period', str(period))
        mainSubtask = self.document.getElementsByTagName('Subtask').item(0)
        mainSubtask.appendChild(executor)

    def addDefaultExecutor(self):
        self.addExecutor('Processing', 1)

    def getTaskBody(self):
        if self.document is not None:
            self.taskBody = self.document.firstChild.toprettyxml()
        return self.taskBody
