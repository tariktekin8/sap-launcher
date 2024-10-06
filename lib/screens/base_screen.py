from tkinter import Tk

class BaseScreen:

    __screenGeometry: str

    def __init__(self, screenGeometry):
        self.__screenGeometry = screenGeometry

    def getNewAppFrame(self) -> Tk:
        tk = Tk()
        tk.eval('tk::PlaceWindow . center')
        tk.geometry(self.__screenGeometry)
        tk.config(padx=20, pady=30)
        tk.title("SAP Launcher")
        return tk