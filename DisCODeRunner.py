import subprocess
import threading


class DisCODeProcess():
    def __init__(self, output):
        # threading.Thread.__init__(self)
        self.output = output
        self.process = None
        self.taskName = ""
        self.logFileName = ""
        self.defaultLogFileName = "output.log"
        self.killSignal = False

    def run(self):
        print("discode starting")
        command = ["discode"]
        if self.taskName != "":
            command = ["discode", "-T" + self.taskName]

        if self.logFileName == "":
            self.logFileName = self.defaultLogFileName

        logFile = open(self.logFileName, 'w')
        self.process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                        universal_newlines=True)
        while not self.killSignal:
            line = self.process.stdout.readline()
            # output.join(line)
            self.output += line
            logFile.write(line)

            # if self.killSignal:
            #     self.process.kill()

            if line == "" or "Server stopped." in line:
                break

            # if self.terminationStatement == "":
            #     continue

            # if self.terminationStatement in line:
            #     self.process.kill()

        self.process.kill()
        print("discode ended")


class DisCODeRunner:
    def __init__(self):
        self.process = None
        self.taskName = ""
        self.terminationStatement = ""
        self.killSignal = False
        self.output = ""

    def run(self):
        process = DisCODeProcess(self.output)
        process.taskName = self.taskName
        process.daemon = True
        process.run()
        # command = ["discode"]
        # if self.taskName != "":
        #     command = ["discode", "-T" + self.taskName]
        # self.process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        #                                 universal_newlines=True)
        # out, err = process.communicate()
        # output = process.stdout.readlines()

    def setTerminationFlag(self, terminationStatement):
        self.terminationStatement = terminationStatement

    def kill(self):
        self.killSignal = True

    def readOutput(self):
        return self.output
        # while True:
            # line = self.process.stdout.readline()
            # output.join(line)
            # output += line

            # if self.killSignal:
            #     self.process.kill()

            # if line == "" or "Server stopped." in line:
            #     break

            # if self.terminationStatement == "":
            #     continue

            # if self.terminationStatement in line:
            #     self.process.kill()

        # return out
        # return output.join(self.process.stdout.readlines())


if __name__ == '__main__':
    runner = DisCODeRunner()
    print(runner.run())
