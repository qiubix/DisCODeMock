from discoderunner import DisCODeRunner, TaskBuilder


class ComponentTester:
    def __init__(self, taskName='test_task'):
        self.taskDirectory = 'data/test_tasks/'
        self.taskName = taskName + '.xml'
        taskPath = self.taskDirectory + self.taskName
        self.taskBuilder = TaskBuilder(taskPath)
        self.taskBuilder.createTemplate()
        self.taskBuilder.addDefaultExecutor()
        self.taskBuilder.save()
        self.componentSinkName = 'Component.in_data'
        self.generatorOutput = 'out_data'
        self.componentName = 'Component'
        self.componentOutput = 'out_data'
        self.runner = DisCODeRunner()

    def setComponent(self, componentName, componentType):
        self.taskBuilder.addComponent(componentName, componentType)
        self.taskBuilder.save()

    def addGenerator(self, generatorType, generatorName = 'Generator'):
        self.taskBuilder.addComponent(generatorName, generatorType)
        self.taskBuilder.save()

    def addSink(self, sinkType, sinkInput = 'in_data'):
        self.taskBuilder.addComponent('Sink', sinkType)
        self.taskBuilder.save()

    def addDataStream(self, sourceName, sourcePort, sinkName, sinkPort):
        self.taskBuilder.addDataStream(sourceName + '.' + sourcePort, sinkName + '.' + sinkPort)
        self.taskBuilder.save()

    def start(self, taskName=''):
        if taskName is '':
            self.runner.taskName = self.taskDirectory + self.taskName
        else:
            self.runner.taskName = taskName
        self.runner.start()

    def getOutput(self):
        return self.runner.readOutput()

    def stop(self):
        self.runner.kill()

    def addTerminationStatement(self, terminationStatement):
        self.runner.terminationStatements.append(terminationStatement)

    def resetTerminationStatements(self):
        self.runner.terminationStatements = []

    def setDebugMode(self, debugMode):
        self.runner.debugMode = debugMode

    def setLogLevel(self, logLevel):
        self.runner.logLevel = logLevel
