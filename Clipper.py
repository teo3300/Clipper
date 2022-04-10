#!/bin/python3

DEBUG = True
defaultOutputParam = '-c copy'
defaultInputParam = ""

import tkinter, tkinter.filedialog
from tkinter import *

import threading
import os
import sys

from FFmpeg import FFmpeg


def resource_path(relative_path):    
    if(hasattr(sys, '_MEIPASS')):
        base_path = getattr(sys, '_MEIPASS')
    else:
        base_path = os.path.abspath('.')
    return os.path.join(base_path, relative_path)


class MainWindow(Tk):

    outputFolder = None
    inputFile = None
    timeStampsFile = None

    #region Controls
    browseInput = None
    browseOutput = None
    browseTimeStamps = None

    startButton = None
    logTextArea = None
    #endregion

    def __init__(self):
        super(MainWindow, self).__init__()
        self.title('Clipper')
        self.geometry('480x360')
        self.update()
        self.minsize(self.winfo_width(), self.winfo_height())

        #datafile = '.resources\\icon.ico'

        # Input Panel
        gridpadding = 2
        parent = Frame(self, padx=10, pady=6)
        parent.pack(fill='x')
        parent.grid_columnconfigure(1, weight=1)

        # InputFile
        temp = Label(parent, text='Input file:')
        temp.grid(row=0, column=0, sticky='w', padx=gridpadding)

        self.inputFile = StringVar(self)
        self.inputFileEntry = Entry(parent, textvariable=self.inputFile)
        self.inputFileEntry.grid(row=0,column=1,sticky='we',padx=gridpadding)

        self.browseInput = Button(parent, text='Select input file', command = self.browseInput_Click)
        self.browseInput.grid(row=0,column=2,sticky='e',padx=gridpadding)

        # Output Folder
        temp = Label(parent,text='Output Folder:')
        temp.grid(row=1,column=0,sticky='w',padx=gridpadding)

        self.outputFolder = StringVar(self)
        self.outputFolderEntry = Entry(parent, textvariable=self.outputFolder)
        self.outputFolderEntry.grid(row=1,column=1,sticky='we',padx=gridpadding)

        self.browseOutput = Button(parent, text='Select output folder', command = self.browseOutput_Click)
        self.browseOutput.grid(row=1,column=2,sticky='e',padx=gridpadding)

        # Timestamps
        temp = Label(parent, text='Timestamps:')
        temp.grid(row=2, column=0, sticky='w', padx=gridpadding)

        self.timeStampsFile = StringVar(self)
        self.timeStampsFileEntry = Entry(parent, textvariable=self.timeStampsFile)
        self.timeStampsFileEntry.grid(row=2,column=1,sticky='we',padx=gridpadding, columnspan=2)
        
        self.browseTimeStamps = Button(parent, text='Select timestamps file', command = self.browseTimeStamps_Click)
        self.browseTimeStamps.grid(row=2,column=2,sticky='e',padx=gridpadding)

        # Additional input parameters
        temp = Label(parent, text='Input parameters:')
        temp.grid(row=3, column=0, sticky='w', padx=gridpadding)

        self.inputParam = StringVar(self, defaultInputParam)
        self.inputParam = Entry(parent, textvariable=self.inputParam)
        self.inputParam.grid(row=3,column=1,sticky='we',padx=gridpadding, columnspan=2)

        # Additional output parameters
        temp = Label(parent, text='Output parameters:')
        temp.grid(row=4, column=0, sticky='w', padx=gridpadding)

        self.outputParam = StringVar(self, defaultOutputParam)
        self.outputParam = Entry(parent, textvariable=self.outputParam)
        self.outputParam.grid(row=4,column=1,sticky='we',padx=gridpadding, columnspan=2)

        # Start Button
        self.startButton = Button(parent)
        self.startButton.configure(text='Start conversion',command = self.startButton_Click)
        self.startButton.grid(row=5, column = 0,sticky='w',padx=gridpadding)

        self.logTextArea = Text(self)
        self.logTextArea.pack(expand=YES, fill=BOTH)

        self.mainloop()

    def browseInput_Click(self):
        file = tkinter.filedialog.askopenfile(parent=self, title='Choose Input file')
        if file:
            self.inputFile.set(file.name)
        pass

    def browseOutput_Click(self):
        directory = tkinter.filedialog.askdirectory(parent=self,title='Choose Output folder')
        if directory != '':
            self.outputFolder.set(directory)
        pass

    def browseTimeStamps_Click(self):
        file = tkinter.filedialog.askopenfile(parent=self,title='Choose timeStamp file')
        if file:
            self.timeStampsFile.set(file.name)
        pass

    def startButton_Click(self):
        ffmpeg = FFmpeg(self.inputFile.get(), self.inputParam.get(), self.outputFolder.get(), self.outputParam.get(), self.timeStampsFile.get(), DEBUG, self.output)
        for stamp in ffmpeg.stamps:
            threading.Thread(target = ffmpeg.cut(stamp)).start()
        pass

    def output(self, string):
        self.logTextArea.insert(END, string+'\n')
        self.logTextArea.see(END)
        pass

if __name__ == '__main__':
    MainWindow()