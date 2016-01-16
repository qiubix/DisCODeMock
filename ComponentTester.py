from TaskBuilder import TaskBuilder


class ComponentTester:
    def __init__(self):
        self.taskBuilder = TaskBuilder()

    def setComponent(self, componentName, componentType):
        self.taskBuilder.createTemplate()
        self.taskBuilder.addDefaultExecutor()
        self.taskBuilder.addComponent(componentName,componentType)
        self.taskBuilder.save()
