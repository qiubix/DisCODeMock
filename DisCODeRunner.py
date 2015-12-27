import os
import subprocess


class DisCODeRunner:
    def __init__(self):
        pass

    def run(self):
        # process = subprocess.Popen(['discode'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # out, err = process.communicate()
        process = os.popen('discode', "r")
        firstLine = process.readline()
        return firstLine
