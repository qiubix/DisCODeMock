import subprocess
from threading import Thread, Condition

import signal

output = []
condition = Condition()
log = ""


class DisCODeProcess(Thread):
    def __init__(self, taskName):
        super().__init__()
        self.taskName = taskName
        self.killSignal = False
        self.process = None

    def run(self):
        global output
        # print("discode starting")
        command = ['discode']
        if self.taskName != '':
            command = ['discode', '-T' + self.taskName]
        # print(command)
        self.process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   universal_newlines=True)
        while True:
            if self.killSignal:
                self.process.send_signal(signal.SIGINT)
            line = self.process.stdout.readline()
            condition.acquire()
            output.append(line)
            condition.notify()
            condition.release()
            # print("DisCODe: ", line)

            if line == '' or 'Server stopped.' in line:
                break

        self.process.send_signal(signal.SIGINT)
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
        self.discodeProcess = None

    def run(self):
        self.discodeProcess = DisCODeProcess(self.taskName)
        self.discodeProcess.daemon = True
        self.discodeProcess.start()

    def runMonitor(self):
        self.monitor = OutputMonitor()
        self.monitor.daemon = True
        self.monitor.start()

    def readOutput(self):
        # global log
        lines = self.process.stdout.readlines()
        log = ''.join(lines)
        return log

    def runDisCODe(self):
        command = ['discode']
        if self.taskName != '':
            command = ['discode', '-T' + self.taskName]
        # print(command)
        self.process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                        universal_newlines=True)

        if self.terminationStatement != '':
            while True:
                line = self.process.stdout.readline()
                if self.terminationStatement in line:
                    self.process.send_signal(signal.SIGINT)
                    break

    def kill(self):
        self.process.send_signal(signal.SIGINT)
        # self.discodeProcess.killSignal = True


if __name__ == '__main__':
    runner = DisCODeRunner()
    runner.runDisCODe()
    # runner.run()
    # runner.readOutput()
    # print(runner.run())
    print(runner.readOutput())
