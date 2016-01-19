from TaskBuilder import TaskBuilder


class ComponentTester:
    def __init__(self):
        self.taskBuilder = TaskBuilder()
        self.taskBuilder.createTemplate()
        self.taskBuilder.addDefaultExecutor()
        self.taskBuilder.save()
        self.componentSinkName = 'Component.in_data'

    def setComponent(self, componentName, componentType, componentInput = 'in_data'):
        self.taskBuilder.addComponent(componentName, componentType)
        self.taskBuilder.addDataStream('Generator.out_data', componentName + '.' + componentInput)
        self.taskBuilder.save()

    def addGenerator(self, generatorType, generatorOutput = 'out_data'):
        self.taskBuilder.addComponent('Generator', generatorType)
        if self.taskBuilder.hasSource('Generator.out_data'):
            self.taskBuilder.updateSource('Generator', generatorOutput)
        else:
            self.taskBuilder.addDataStream('Generator.' + generatorOutput, self.componentSinkName)
        self.taskBuilder.save()

    def setGeneratorOutputName(self, outputName):
        pass
