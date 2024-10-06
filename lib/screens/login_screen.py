from tkinter import Tk, StringVar, Label, Entry, Button

from .base_screen import BaseScreen

class LoginScreen(BaseScreen):

    __screen: Tk
    __screenGeometry = '300x150'

    passwordVar: StringVar

    onLogin: callable
    onConfig: callable

    def __init__(self, onLogin, onConfig):
        super().__init__(self.__screenGeometry)

        self.onLogin = onLogin
        self.onConfig = onConfig
        pass

    def show(self):
        
        self.__screen = super().getNewAppFrame()
        self.__screen.geometry(self.__screenGeometry)

        self.passwordVar = StringVar(self.__screen)
        passwordLabel = Label(self.__screen, text = 'Keepass password:')
        passwordEntry = Entry(self.__screen, show="*", textvariable=self.passwordVar, width=40)
        passwordEntry.bind('<Return>', self.__onLogin)

        loginButton = Button(self.__screen, text="Login",command=self.__onLogin)
        configButton = Button(self.__screen, text="Edit config",command=self.__onConfig)

        passwordLabel.grid(row=0, columnspan=2, sticky='w')
        passwordEntry.grid(row=1, columnspan=2, sticky='we')

        loginButton.grid(row=2, column=0, sticky='we')
        configButton.grid(row=2, column=1, sticky='we')

        self.__screen.mainloop()
    
    def close(self):
        self.__screen.destroy()

    def __onLogin(self, event = ""):
        self.onLogin(self, self.passwordVar.get())
        return
    
    def __onConfig(self):
        self.onConfig(self.__screen)
        return