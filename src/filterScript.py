import urllib
import urllib2
import json
import pickle
import os
import sys

def filter(lines,marker,end,lookOnlyOnFront,projects):
	  if query.count(marker)>0:
	  	pos = query.rfind(marker)+1
		if lookOnlyOnFront:
			pos = query.find(marker)+1
	  	project = query[pos:]
	  	shown = False
	  	for p in projects:
	  		if p[0].lower().count(project.lower())>0:
	  			if p[0].lower().find(project.lower())==0:
	  				txt = query[:pos]
	  				shown = True
	  				lines.append("<item autocomplete=\""+txt+p[0]+end+" \" arg=\""+txt+p[0]+end+"\" valid=\"no\"><title>"+txt+p[0]+end+"</title><subtitle>Add "+txt+p[0]+end+" to your Todo</subtitle></item>")
	  	if not shown:
	  		lines.append("<item subtitle=\"Add "+query+" to your Todo\" arg=\""+query+"\" valid=\"yes\"><title>"+query+"</title><subtitle>Add "+query+" to your Todo</subtitle></item>")
	  else:
	  	lines.append("<item subtitle=\"Add "+query+" to your Todo\" arg=\""+query+"\" valid=\"yes\"><title>"+query+"</title><subtitle>Add "+query+" to your Todo</subtitle></item>")


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

if not os.path.exists("token.dat"):
	print("<items><item><title>Call todotoken yourToken</title></item></items>")
	sys.exit()
else:
  token = open("token.dat").readline()

  PROJECTS = "projects.dat"
  LABELS = "labels.dat"

  if not os.path.exists(PROJECTS) or not os.path.exists(LABELS):
      pickle.dump(retrieveObj("https://api.todoist.com/rest/v1/projects"),open(PROJECTS,"w+"))
      pickle.dump(retrieveObj("https://api.todoist.com/rest/v1/labels"),open(LABELS,"w+"))

  projects = pickle.load(open(PROJECTS))
  labels = pickle.load(open(LABELS))

  query = " ".join(sys.argv[1:])
  query = query.decode('utf-8')

  print("<?xml version=\"1.0\"?>")
  print("<items>")
  lines = []
  filter(lines,"[",']',True,projects)
  filter(lines,"#","",True,projects)
  filter(lines,"@","",False,labels)
  s = set()
  for line in lines:
	  if len(s.intersection([line]))==0:
	  	print line
	  s.add(line)
  print("</items>")
