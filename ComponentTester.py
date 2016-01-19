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

    def setComponent(self, componentName, componentType):
        self.taskBuilder.addComponent(componentName, componentType)
        self.taskBuilder.save()

    def addGenerator(self, generatorType):
        self.taskBuilder.addComponent('Generator', generatorType)
        self.taskBuilder.save()

    def addSink(self, sinkType, sinkInput = 'in_data'):
        self.taskBuilder.addComponent('Sink', sinkType)
        self.taskBuilder.save()

    def addDataStream(self, sourceName, sourcePort, sinkName, sinkPort):
        self.taskBuilder.addDataStream(sourceName + '.' + sourcePort, sinkName + '.' + sinkPort)
        self.taskBuilder.save()
