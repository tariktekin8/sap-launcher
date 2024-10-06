from tkinter import Tk, StringVar, Label, Entry, Button, filedialog, DISABLED

from .base_screen import BaseScreen
import sys

sys.path.append('../providers')
from lib.providers.config_provider import Config

class ConfigScreen(BaseScreen):

    __screen: Tk
    __screenGeometry= '500x150'

    __config: Config

    __sapShortcutExePathVar: StringVar
    __keepassDbPathVar: StringVar

    onSave: callable
    
    def __init__(self, config, onSave):
        super().__init__(self.__screenGeometry)

        self.__config = config
        self.onSave = onSave
        pass

    def show(self):
        
        self.__screen = super().getNewAppFrame()

        self.__sapShortcutExePathVar = StringVar(self.__screen)
        self.__keepassDbPathVar = StringVar(self.__screen)

        self.__sapShortcutExePathVar.set(self.__config.sapShortcutExePath)
        self.__keepassDbPathVar.set(self.__config.keepassDbPath)

        sapShortcutExePathLabel = Label(self.__screen, text = 'SAP shortcut exe path')
        sapShortcutExePathEntry = Entry(self.__screen,textvariable = self.__sapShortcutExePathVar, width=50, state=DISABLED)
        sapShortcutExePathButton = Button(self.__screen, text = '...', command=self.__openFileDialogSap)
        
        keepassDbPathLabel = Label(self.__screen, text = 'Keepass DB file path')
        keepassDbPathEntry = Entry(self.__screen, textvariable = self.__keepassDbPathVar, width=50, state=DISABLED)
        keepassDbPathButton = Button(self.__screen, text = '...', command=self.__openFileDialogKeepass)
        
        saveButton = Button(self.__screen, text = 'Save', command=self.__onSave, width=25)
        
        sapShortcutExePathLabel.grid(row=0,column=0)
        sapShortcutExePathEntry.grid(row=0,column=1)
        sapShortcutExePathButton.grid(row=0,column=2)

        keepassDbPathLabel.grid(row=1,column=0)
        keepassDbPathEntry.grid(row=1,column=1)
        keepassDbPathButton.grid(row=1,column=2)

        saveButton.grid(rowspan=2, row=6, columnspan=3)
        
        self.__screen.mainloop()
        
    def close(self):
        self.__screen.destroy()
    
    def __openFileDialogSap(self):
        filetypes = (  ('SAP Shortcut exe file', '*.exe'), ('All files', '*.*') )
        filepath = filedialog.askopenfilename(title='Open SAP shortcut exe file', initialdir='/', filetypes=filetypes)
        self.__sapShortcutExePathVar.set(filepath)

    def __openFileDialogKeepass(self):
        filetypes = (  ('Keepass file', '*.kdbx'), ('All files', '*.*') )
        filepath = filedialog.askopenfilename(title='Open Keepass file', initialdir='/', filetypes=filetypes)
        self.__keepassDbPathVar.set(filepath)

    def __onSave(self):
        self.__config = Config(sapShortcutExePath=self.__sapShortcutExePathVar.get(), keepassDbPath=self.__keepassDbPathVar.get())
        self.onSave(self, self.__config)