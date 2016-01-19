from TaskBuilder import TaskBuilder


class ComponentTester:
    def __init__(self):
        self.taskBuilder = TaskBuilder()
        self.taskBuilder.createTemplate()
        self.taskBuilder.addDefaultExecutor()
        self.taskBuilder.save()
        self.componentSinkName = 'Component.in_data'
        self.generatorOutput = 'out_data'
        self.componentName = 'Component'

    def setComponent(self, componentName, componentType, componentInput = 'in_data'):
        self.componentName = componentName
        self.taskBuilder.addComponent(componentName, componentType)
        if self.taskBuilder.hasSource('Generator.' + self.generatorOutput):
            self.taskBuilder.updateSink('Component', componentName, componentInput)
        else:
            self.taskBuilder.addDataStream('Generator.' + self.generatorOutput, componentName + '.' + componentInput)
        self.taskBuilder.save()

    def addGenerator(self, generatorType, generatorOutput = 'out_data'):
        self.taskBuilder.addComponent('Generator', generatorType)
        self.generatorOutput = generatorOutput
        if self.taskBuilder.hasSource('Generator.out_data'):
            self.taskBuilder.updateSource('Generator', generatorOutput)
        else:
            self.taskBuilder.addDataStream('Generator.' + generatorOutput, self.componentSinkName)
        self.taskBuilder.save()

    def addSink(self, sinkType):
        self.taskBuilder.addComponent('Sink', sinkType)
        self.taskBuilder.addDataStream(self.componentName + '.out_data', 'Sink.in_data')
        self.taskBuilder.save()
