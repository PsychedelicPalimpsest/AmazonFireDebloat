import src
import json

class Config:

	def __init__(self, configFile):
		
		self.jsonData = json.loads(configFile.read())
		print(f"\n\nLoading config: {self.jsonData.get('name')}\n\n")

		node = src
		for part in self.jsonData["jarvis"].split("/"):
			node = getattr(node, part)
		self.jarvis = node(self)