from tkinter import Tk, messagebox

from .providers import SAPLauncher, KeepassProvider, ConfigProvider, Config
from .screens import LoginScreen, ConfigScreen, LaunchScreen

class App:

    __configProvider: ConfigProvider
    __sapLauncher: SAPLauncher
    __keepassProvider: KeepassProvider

    def __init__(self):
        self.__configProvider = ConfigProvider()
        LoginScreen(onLogin=self.onLogin, onConfig=self.onConfig).show()

    # Login screen event
    def onLogin(self, loginScreen: LoginScreen, password):
        if not password:
            return
        
        config = self.__configProvider.getConfig()

        if not config.sapShortcutExePath or not config.keepassDbPath:
            messagebox.showwarning(title="Warning", message="Please make sure the configurations are complete!\nSAP shortcut exe path or Keepassxc path are missing!")
            return
        
        loginScreen.close()

        self.__keepassProvider = KeepassProvider(config.keepassDbPath, password)
        self.__sapLauncher = SAPLauncher(config.sapShortcutExePath)

        credentials = self.__keepassProvider.getCredentials()

        listData = []
        for data in credentials:
            listData.append(data.presentationText)

        LaunchScreen(listData=listData, onFilterChange=self.onFilterChange, onLaunch=self.onLaunch).show()

    # Login screen event
    def onConfig(self, loginScreen: LoginScreen):
        ConfigScreen(onSave=self.onSave, config=self.__configProvider.getConfig()).show()

    # Config screen event
    def onSave(self, configScreen: ConfigScreen, config: Config):
        self.__configProvider.updateConfig(config)
        configScreen.close()

    # Launch screen event
    def onFilterChange(self, launchScreen: LaunchScreen, filterValue):
        credentials = self.__keepassProvider.applyFilter(filter=filterValue)

        listData = []
        for data in credentials:
            listData.append(data.presentationText)

        launchScreen.updateList(listData)

    # Launch screen event
    def onLaunch(self, launchScreen: LaunchScreen, selectedIndex):
        if not selectedIndex:
            return

        credential = self.__keepassProvider.getCredentials()[selectedIndex]
        self.__sapLauncher.openSystem(systemId=credential.systemId, client=credential.client,
                                      username=credential.username, password=credential.password, language=credential.language)

        launchScreen.hide()