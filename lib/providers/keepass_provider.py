from pykeepass import PyKeePass

class Credential(object):
    title: str
    notes: str
    systemId: str
    client: str
    username: str
    password: str
    language: str
    presentationText: str
    
    def __init__(self, title, notes, systemId, client, username, password, language):
        self.title            = title
        self.notes            = notes
        self.systemId         = systemId
        self.client           = client
        self.username         = username
        self.password         = password
        self.language         = language
        self.presentationText = title + " (" + systemId + ", " + client + ")"

class KeepassProvider:
     
    path : str
    password : str
    credentials : list[Credential]
    credentialsCache : list[Credential]
    credentialsCount: int

    def __init__(self, path, password):
        self.path = path
        self.password = password
        self.credentials = self.credentialsCache = self.__readFile()
        self.credentialsCount = self.credentials.count

    def __readFile(self):
        pyKeePass = PyKeePass(filename=self.path, password=self.password)

        credentials = []
        for entry in pyKeePass.entries:

            try:
                systemId = entry.custom_properties["systemId"]
                client = entry.custom_properties["client"]
                language = entry.custom_properties["language"]
            except KeyError:
                continue
            
            notes = ""
            if entry.notes:
                notes = entry.notes
            
            credentials.append(Credential(title=entry.title,
                                          notes=notes,
                                          systemId=systemId,
                                          client=client,
                                          username=entry.username,
                                          password=entry.password,
                                          language=language))
            
        credentials.sort(key=lambda x: x.presentationText, reverse=False)

        return credentials
    
    def getCredential(self, title):
        for credential in self.credentials:
            if credential.title == title:
                return credential
            
    def getCredentials(self):
        return self.credentialsCache
    
    def applyFilter(self, filter = ""):
        if filter == "":
            self.credentialsCache = self.credentials
            return self.credentialsCache

        self.credentialsCache = []
        for credential in self.credentials:
            if filter.upper() in credential.presentationText.upper():
                self.credentialsCache.append(credential)

        return self.credentialsCache
    
    def clearFilter(self):
        self.credentialsCache = self.credentials