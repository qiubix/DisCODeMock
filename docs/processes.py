import signal
import subprocess
from threading import Condition, Thread

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