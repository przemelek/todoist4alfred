import urllib
import urllib2
import json
import pickle
import os
import sys

token = open("token.dat").readline()

headers = {"Authorization":"Bearer "+token}

PROJECTS = "projects.dat"
LABELS = "labels.dat"

if not os.path.exists(PROJECTS):
    url = "https://api.todoist.com/rest/v1/projects"

    req = urllib2.Request(url, headers=headers)
    response = urllib2.urlopen(req)
    jsonResponse = response.read()

    projects = json.loads(jsonResponse)

    projs = []

    for project in projects:
        name = project["name"]
        id = project["id"]
        projs.append([name,id])

    pickle.dump(projs,open(PROJECTS,"w+"))

projects = pickle.load(open(PROJECTS))
labels = pickle.load(open(LABELS))

query = " ".join(sys.argv[1:])
query = query.decode('utf-8')

projectId = -1

pos = 2**32

qw = (query+" ").lower()

due_string = None

if query.count("{")==1:
    pos = query.rfind("{")
    due_string = query[pos+1:]
    query = query[:pos]

for project in projects:
    q = "#"+project[0].lower()+" "
    if qw.count(q)>0:
        p = qw.find(q)
        if p<pos:
            pos = p
            projectId = int(project[1])

for project in projects:
    q = "["+project[0].lower()+"] "
    if qw.count(q)>0:
        p = qw.find(q)
        if p<pos:
            pos = p
            projectId = int(project[1])

labelIds = []
for label in labels:
    q = "@"+label[0].lower()+" "
    if qw.count(q)>0:
        p = qw.find(q)
        labelIds.append(int(label[1]))

url = "https://api.todoist.com/rest/v1/tasks"

msg = {"content":query}
if projectId!=-1:
    msg["project_id"]=projectId
if len(labelIds)>0:
    msg["label_ids"]=labelIds
if due_string:
    msg["due_string"]=due_string

body=json.dumps(msg)


headers["Content-Type"]="application/json"

req = urllib2.Request(url, body, headers)
response = urllib2.urlopen(req)

print query
