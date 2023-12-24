import src
import json

class Config:

    def __init__(self, configFile):
        self.onExit = []
        
        self.jsonData = json.loads(configFile.read())

        self.updateTimeing = self.jsonData.get("update_minutes", 60)*60

        print(f"\n\nLoading config: {self.jsonData.get('name')}\n\n")

        node = src
        for part in self.jsonData["jarvis"].split("/"):
            node = getattr(node, part)
        self.root = node(self)
    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        print("asd")
        for F in self.onExit: 
            print(F)
            F()