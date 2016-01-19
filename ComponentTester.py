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
        self.componentOutput = 'out_data'

    def setComponent(self, componentName, componentType, componentInput = 'in_data', componentOutput = 'out_data'):
        self.componentName = componentName
        self.componentOutput = componentOutput
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

    def addSink(self, sinkType, sinkInput = 'in_data'):
        self.taskBuilder.addComponent('Sink', sinkType)
        self.taskBuilder.addDataStream(self.componentName + '.' + self.componentOutput, 'Sink.' + sinkInput)
        self.taskBuilder.save()
