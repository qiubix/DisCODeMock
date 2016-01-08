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
        DOMimpl = getDOMImplementation()
        document = DOMimpl.createDocument(None, 'Task', None)
        topLevelElement = document.documentElement

        subtasksElement = document.createElement('Subtasks')
        topLevelElement.appendChild(subtasksElement)
        mainSubtaskElement = document.createElement('Subtask')
        mainSubtaskElement.setAttribute('name', 'Main')
        subtasksElement.appendChild(mainSubtaskElement)

        datastreamsElement = document.createElement('DataStreams')
        topLevelElement.appendChild(datastreamsElement)

        self.taskBody = document.firstChild.toprettyxml()
        # self.taskBody = '<Task>\n<Subtasks>\n</Subtasks>\n<Datasets>\n</Datasets>\n</Task>'
