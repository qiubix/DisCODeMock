import subprocess


class DisCODeRunner:
    def __init__(self):
        pass

    def run(self):
        process = subprocess.Popen(['discode'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        out, err = process.communicate()
        return out

if __name__ == '__main__':
    runner = DisCODeRunner()
    print(runner.run())
