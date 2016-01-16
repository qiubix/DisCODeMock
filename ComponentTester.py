from TaskBuilder import TaskBuilder


class ComponentTester:
    def __init__(self):
        self.taskBuilder = TaskBuilder()
        self.taskBuilder.createTemplate()
        self.taskBuilder.addDefaultExecutor()
        self.taskBuilder.save()

    def setComponent(self, componentName, componentType, componentInput = 'in_data'):
        self.taskBuilder.addComponent(componentName, componentType)
        self.taskBuilder.addDataStream('Generator.out_data', componentName + '.' + componentInput)
        self.taskBuilder.save()

    def addGenerator(self, generatorType):
        self.taskBuilder.addComponent('Generator', generatorType)
        self.taskBuilder.save()

    def setGeneratorOutputName(self, outputName):
        pass
