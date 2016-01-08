from xml.dom.minidom import getDOMImplementation


class TaskBuilder:
    def __init__(self):
        self.fileName = ''
        self.taskBody = ''

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

    def createTemplate(self):
        document = self.createEmptyDocument()
        topLevelElement = self.getTopLevelElement(document)
        subtasksElement = self.addSubtasksElement(document, topLevelElement)
        self.addDataStreams(document, topLevelElement)
        self.addMainSubtask(document, subtasksElement)

        self.taskBody = document.firstChild.toprettyxml()

    def getTopLevelElement(self, document):
        topLevelElement = document.documentElement
        return topLevelElement

    def createEmptyDocument(self):
        DOMimpl = getDOMImplementation()
        document = DOMimpl.createDocument(None, 'Task', None)
        return document

    def addDataStreams(self, document, topLevelElement):
        datastreamsElement = document.createElement('DataStreams')
        topLevelElement.appendChild(datastreamsElement)

    def addMainSubtask(self, document, subtasksElement):
        mainSubtaskElement = document.createElement('Subtask')
        mainSubtaskElement.setAttribute('name', 'Main')
        subtasksElement.appendChild(mainSubtaskElement)

    def addSubtasksElement(self, document, topLevelElement):
        subtasksElement = document.createElement('Subtasks')
        topLevelElement.appendChild(subtasksElement)
        return subtasksElement
