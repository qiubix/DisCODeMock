import subprocess


class DisCODeRunner:
    def __init__(self):
        self.taskName = ""
        self.terminationStatement = ""

    def run(self):
        command = ["discode"]
        if self.taskName != "":
            command = ["discode", "-T " + self.taskName]
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        out, err = process.communicate()
        # for line in process.stdout.readlines():
        #     if line == exitStatement
        return out

    def setTask(self, taskName):
        self.taskName = taskName

    def setTerminationFlag(self, terminationStatement):
        self.terminationStatement = terminationStatement


if __name__ == '__main__':
    runner = DisCODeRunner()
    print(runner.run())
