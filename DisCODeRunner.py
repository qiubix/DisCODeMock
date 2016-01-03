import subprocess
from threading import Thread, Condition

output = []
condition = Condition()
log = ""


class DisCODeProcess(Thread):
    def __init__(self, taskName):
        super().__init__()
        self.taskName = taskName

    def run(self):
        global output
        # print("discode starting")
        command = ['discode']
        if self.taskName != '':
            command = ['discode', '-T' + self.taskName]
        # print(command)
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   universal_newlines=True)
        while True:
            line = process.stdout.readline()
            condition.acquire()
            output.append(line)
            condition.notify()
            condition.release()
            # print("DisCODe: ", line)

            if line == '' or 'Server stopped.' in line:
                break

        process.kill()
        # print("discode ended")


class OutputMonitor(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        global output
        global log
        log = ''
        # print("Monitor started")
        while True:
            condition.acquire()
            if not output:
                # print("Monitor waiting for output")
                condition.wait()
            line = output.pop(0)
            log += line
            # print(log)
            # print("Monitor: ", line)
            condition.release()
            if line == "":
                break

        # print("Monitor ended")


class DisCODeRunner:
    def __init__(self):
        self.process = None
        self.monitor = None
        self.taskName = ''
        self.terminationStatement = ''
        self.killSignal = False
        self.output = ''
        self.log = ''

    def run(self):
        self.process = DisCODeProcess(self.taskName)
        self.process.daemon = True
        self.process.start()

    def runMonitor(self):
        self.monitor = OutputMonitor()
        self.monitor.daemon = True
        self.monitor.start()

    def readOutput(self):
        global log
        return log

    def runDisCODe(self):
        command = ['discode']
        if self.taskName != '':
            command = ['discode', '-T' + self.taskName]
        print(command)
        self.process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                        universal_newlines=True)


if __name__ == '__main__':
    runner = DisCODeRunner()
    runner.run()
    runner.readOutput()
    # print(runner.run())
