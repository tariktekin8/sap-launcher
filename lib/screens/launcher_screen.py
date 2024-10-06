from tkinter import Tk, Frame, StringVar, Entry, Listbox, Button, filedialog

from .base_screen import BaseScreen

class LaunchScreen(BaseScreen):

    __screen: Tk
    __screenGeometry = '350x500'

    __filterVar: StringVar
    __listData: list
    __listBox: Listbox

    onFilterChange: callable
    onLaunch: callable

    def __init__(self, listData: list, onFilterChange, onLaunch):
        super().__init__(self.__screenGeometry)
        self.__listData = listData
        self.onFilterChange = onFilterChange
        self.onLaunch = onLaunch
        pass

    def show(self):

        self.__screen = super().getNewAppFrame()

        self.__screen.grid_rowconfigure(1, weight=1)
        self.__screen.grid_columnconfigure(0, weight=1)

        mainFrame = Frame(self.__screen, width=300, height=500)
        mainFrame.pack()

        top = Frame(mainFrame, width=300, height=20, pady=10)
        center = Frame(mainFrame, width=300, height=200, pady=10)
        bottom = Frame(mainFrame, width=300, height=30, pady=10)

        top.pack()
        center.pack()
        bottom.pack()

        self.__filterVar = StringVar(self.__screen)
        self.__filterVar.trace_add("write", self.__onFilterChange)

        Entry(top, width=40, textvariable=self.__filterVar).pack()

        self.__listBox = Listbox(center, width=40, height=20)
        self.__listBox.grid(column=0, row=0, sticky="ew")

        self.buildList(self.__listData)

        Button(bottom, text='Launch', command=self.__onLaunch,
               width=33, height=2).pack()

        self.__screen.mainloop()

    def close(self):
        self.__screen.destroy()

    def hide(self):
        self.__screen.iconify()

    def buildList(self, listData):
        self.__listBox.delete(0, 99999)
        for index, data in enumerate(listData):
            self.__listBox.insert(index, data)

    def updateList(self, listData: list):
        self.__listData = listData
        self.buildList(self.__listData)

    def __onFilterChange(self, s1, s2, s3):
        self.onFilterChange(self, self.__filterVar.get())
        pass

    def __onLaunch(self):
        currentSelections = self.__listBox.curselection()
        if not currentSelections:
            return
        
        self.onLaunch(self, currentSelections[0])