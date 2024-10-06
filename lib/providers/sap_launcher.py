import os

class SAPLauncher:
    sapShortcutExePath : str
    
    def __init__(self,sapShortcutExePath):
        self.sapShortcutExePath = sapShortcutExePath
    
    def openSystem(self, systemId, client, username, password, language):
        path = '"' + self.sapShortcutExePath + '" ' + '-system=&1 -client=&2 -user=&3 -pw=&4 -language=&5'

        path = path.replace("&1", systemId)
        path = path.replace("&2", client)
        path = path.replace("&3", username)
        path = path.replace("&4", password)
        path = path.replace("&5", language)

        os.system(path)