import signal
import subprocess

from processes import DisCODeProcess, OutputMonitor


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

    def runDisCODe(self):
        self.discodeProcess = DisCODeProcess(self.taskName)
        self.discodeProcess.daemon = True
        self.discodeProcess.start()

    def runMonitor(self):
        self.monitor = OutputMonitor()
        self.monitor.daemon = True
        self.monitor.start()

    def readOutput(self):
        lines = self.process.stdout.readlines()
        log = ''.join(lines)
        return log

    def start(self):
        command = ['discode']
        if self.taskName != '':
            command = ['discode', '-T' + self.taskName]
        # print(command)
        self.process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                        universal_newlines=True)

        if self.terminationStatement != '':
            while True:
                line = self.process.stdout.readline()
                print(line)
                if self.terminationStatement in line:
                    self.process.send_signal(signal.SIGINT)
                    break

    def kill(self):
        print('sending kill signal...')
        self.process.send_signal(signal.SIGINT)


if __name__ == '__main__':
    runner = DisCODeRunner()
    runner.start()
    print(runner.readOutput())
