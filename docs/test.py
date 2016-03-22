import subprocess
import time
import signal


#command = ['discode', '-TCvBasic:SequenceViewer']
command = ['discode', '-TSequenceViewer.xml', '-L0']
# print(command)
process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        universal_newlines=True)

time.sleep(10)
process.send_signal(signal.SIGINT)
print(process.stdout.readlines())
