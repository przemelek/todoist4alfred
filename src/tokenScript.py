import sys

query = sys.argv[1]

f = open("token.dat","w+")
f.write(query)
f.close()
