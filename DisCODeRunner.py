import subprocess
from threading import Thread, Condition

output = []
condition = Condition()
log = ""


class DisCODeProcess(Thread):
    def run(self):
        global output
        print("discode starting")
        command = ["discode"]
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   universal_newlines=True)
        while True:
            line = process.stdout.readline()
            condition.acquire()
            output.append(line)
            condition.notify()
            condition.release()
            print("DisCODe: ", line)

            if line == "" or "Server stopped." in line:
                break

        process.kill()
        print("discode ended")


class OutputMonitor(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        global output
        global log
        print("Monitor started")
        while True:
            condition.acquire()
            if not output:
                print("Monitor waiting for output")
                condition.wait()
            line = output.pop(0)
            log += line
            print(log)
            # print("Monitor: ", line)
            condition.release()


# class DisCODeProc:
#     def __init__(self, output):
#         threading.Thread.__init__(self)
        # self.output = output
        # self.process = None
        # self.taskName = ""
        # self.logFileName = ""
        # self.defaultLogFileName = "output.log"
        # self.killSignal = False

    # def run(self):
    #     print("discode starting")
    #     command = ["discode"]
    #     if self.taskName != "":
    #         command = ["discode", "-T" + self.taskName]

        # if self.logFileName == "":
        #     self.logFileName = self.defaultLogFileName

        # logFile = open(self.logFileName, 'w')
        # self.process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        #                                 universal_newlines=True)
        # while not self.killSignal:
        #     line = self.process.stdout.readline()
        #     output.join(line)
            # self.output += line
            # logFile.write(line)

            # if self.killSignal:
            #     self.process.kill()

            # if line == "" or "Server stopped." in line:
            #     break

                # if self.terminationStatement == "":
                #     continue

                # if self.terminationStatement in line:
                #     self.process.kill()

        # self.process.kill()
        # print("discode ended")


class DisCODeRunner:
    def __init__(self):
        self.process = None
        self.monitor = None
        self.taskName = ""
        self.terminationStatement = ""
        self.killSignal = False
        self.output = ""
        self.log = ""

    def run(self):
        # process = DisCODeProcess(self.output)
        # process.taskName = self.taskName
        # process.daemon = True
        # process.run()
        self.process = DisCODeProcess()
        self.process.daemon = True
        self.process.start()
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

    def runMonitor(self):
        self.monitor = OutputMonitor()
        self.monitor.daemon = True
        self.monitor.start()

    def readOutput(self):
        global log
        return log
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

    # def stop(self):
    #     self.process.


if __name__ == '__main__':
    runner = DisCODeRunner()
    runner.run()
    runner.readOutput()
    # print(runner.run())
