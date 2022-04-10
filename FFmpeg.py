import os
from os import system

class FFmpeg:

    progress = 0
    total = 0

    commandString = '{} -ss {} -to {} {} -i {} {} {}'
    
    program = None
    inputFile = None
    inputParam = None
    outputFolder = None
    outputParam = None
    timeStampsFile = None
    print = None
    DEBUG = False

    stamps = []

    def debug(self, string):
        if self.DEBUG:
            if(callable(self.print)): self.print(f'DEBUG: {str(string)}')

    def output(self, string):
        if(callable(self.print)): self.print(f'-----: {str(string)}')
    
    def error(self, string):
        if(callable(self.print)): self.print(f'ERROR: {str(string)}, see terminal for detailed info')

    def getStamps(self, fileName):
        progressive = 1
        ret = []
        lines = open(fileName, 'r').readlines()
        for line in lines:
            tmp = ['', '', '', -1]
            line_d = line.replace('\n','').split(' ')
            if(len(line_d) < 2):
                self.error(f'({line}) impossible to find timestamp')
                exit(1)
            if(len(line_d) > 2):
                tmp[2] = " ".join(line_d[2:])
            tmp[0] = line_d[0]
            tmp[1] = line_d[1]
            tmp[3] = progressive
            progressive += 1
            ret.append(tmp)
        self.debug(f'Found stamps: \n{ret}')
        return ret

    def __init__(self, inputFile, inputParam, outputFolder, outputParam, timeStampsFile, DEBUG, print = None):
        from sys import platform
        if platform == "linux" or platform == "linux2" or platform == "darwin":
            self.program = "ffmpeg"
        elif platform == "win32":
            self.program = ".\\bin\\ffmpeg.exe"
            import os.path
            if not os.path.isfile(program):
                self.error("Could not find binary ffmpeg.exe, please download it and move it inside bin folder")
                exit(1)

        self.inputFile = inputFile
        self.inputParam = inputParam
        self.outputFolder = outputFolder
        self.outputParam = outputParam
        self.timeStampsFile = timeStampsFile
        self.print = print
        self.DEBUG = DEBUG
        self.stamps = self.getStamps(timeStampsFile)
    
    def cut(self, stamp):
        beginStamp, endStamp, comment, ID = stamp
        self.debug(f'clip ({ID}): {beginStamp}-{endStamp} "{comment}"')
        outputPath = '/'.join(
            [self.outputFolder,
            f'clipped_{beginStamp.replace(":", "-")}_{endStamp.replace(":", "-")}_{comment.replace(" ", "_")}.mp4'])
        self.debug(f'clip ({ID}): output path: "{outputPath}"')
        command = self.commandString.format(f'{self.program}', beginStamp, endStamp, f'{self.inputParam}', f'"{self.inputFile}"', f'{self.outputParam}', f'"{outputPath}"')
        self.debug(f'"running command: {command}')
        self.debug(command)
        response = os.system(command)
        if response != 0:
            self.error(f'clip ({ID}): error converting ({stamp})')
        else:
            self.output(f'clip ({ID}): {beginStamp}-{endStamp} "{comment}" converted')

