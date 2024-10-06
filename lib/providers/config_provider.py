import json
import os

FILE_NAME = "config.json"

class Config:
    sapShortcutExePath : str
    keepassDbPath : str

    def __init__(self, sapShortcutExePath = "", keepassDbPath = ""):
        self.sapShortcutExePath = sapShortcutExePath
        self.keepassDbPath = keepassDbPath

class ConfigProvider:

    filePath: str
    config : Config

    def __init__(self):

        self.filePath = os.getcwd() + "/" + FILE_NAME

        if not ConfigProvider.isConfigFileExists(self.filePath):
            self.__createConfig()
        else:
            self.__readConfig()

    def isConfigFileExists(filePath):
        return os.path.exists(filePath)

    def __createConfig(self):
        self.config = Config()

        with open(self.filePath, "w") as file:
            json.dump(self.config.__dict__, file, indent=4)
            
    def __readConfig(self):
        with open(self.filePath,"r") as file:
            jsonData = json.load(file) 

            if not jsonData:
                return
            
            self.config = Config(sapShortcutExePath=jsonData["sapShortcutExePath"], keepassDbPath=jsonData["keepassDbPath"])
                    
    def getConfig(self) -> Config:
        return self.config

    def updateConfig(self, config: Config):
        self.config = config

        with open(self.filePath, "w") as file:
            json.dump(self.config.__dict__, file, indent=4)