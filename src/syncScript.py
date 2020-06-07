import urllib
import urllib2
import json
import pickle
import os

if not os.path.exists("token.dat"):
	print("<items><item><title>Call todotoken yourToken</title></item></items>")
	sys.exit()


token = open("token.dat").readline()

def retrieveObj(url):
      headers = {"Authorization":"Bearer "+token}
      req = urllib2.Request(url, headers=headers)
      response = urllib2.urlopen(req)
      jsonResponse = response.read()
      response = json.loads(jsonResponse)
      objs = []
      for obj in response:
          name = obj["name"]
          id = obj["id"]
          objs.append([name,id])
      return objs

PROJECTS = "projects.dat"
LABELS = "labels.dat"

headers = {"Authorization":"Bearer "+token}

pickle.dump(retrieveObj("https://api.todoist.com/rest/v1/projects"),open(PROJECTS,"w+"))
pickle.dump(retrieveObj("https://api.todoist.com/rest/v1/labels"),open(LABELS,"w+"))
