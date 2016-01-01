import subprocess


class DisCODeRunner:
    def __init__(self):
        self.taskName = ""

    def run(self):
        command = ["discode"]
        if self.taskName != "":
            command = ["discode", "-T " + self.taskName]
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        out, err = process.communicate()
        return out

    def setTask(self, taskName):
        self.taskName = taskName


if __name__ == '__main__':
    runner = DisCODeRunner()
    print(runner.run())
