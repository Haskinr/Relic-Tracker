"""import random
letters = "abcdefghijklmnopqrstuvwxyz"
relics = []

for i in range(10):
  relic = letters[random.randrange(0, len(letters))] + str(random.randrange(1, 11))
  relics.append(relic)

print(relics)"""

"""connects to server"""
from couchbase.cluster import Cluster
from couchbase.cluster import PasswordAuthenticator
cluster = Cluster('couchbase://localhost')
authenticator = PasswordAuthenticator('username', 'password')
#(username, password) created in couchbase with the cluster. user needs to have read and write privleges
cluster.authenticate(authenticator)
bucket = cluster.open_bucket('Rewards')

from couchbase.n1ql import N1QLQuery
"""#placeholder query sequence
from couchbase.n1ql import N1QLQuery
node= "'beryhinia'"
query = N1QLQuery("SELECT round2 FROM Rewards WHERE node = " + node)
#create list of  known  relics
reliclist = []
for row in bucket.n1ql_query(query):
    for key in row:
      for item in row[key]:
              reliclist.append(item)
print reliclist"""
#Update Node Ph query
"""UPDATE Rewards set round2 = ARRAY_APPEND(Rewards.round2, {"lith h2" : 1})"""
#Update  Reward value ph query
"""UPDATE Rewards set round2 = OBJECT_put(round2, "meso b2", 3) Returning round2"""
#New Reward Ph query
"""UPDATE Rewards set round2 = OBJECT_ADD(round2, "meso b2", 3) Returning round2"""
#New node Placeholder query
"""UPSERT INTO Rewards (Key, Value) VALUES ("beryhinia", {"planet" : "sedna", "node": "beryhinia", 
"type" : "nodesummary", "round1" : {}, "round2" : {}, "round3" : {}, "round4" : {}   })"""


options = [ "1 log relics", "2 test"]
def menu():
    print("pick a thing", options) 
    while True:
        thing = raw_input()
        if thing == "log relics" or thing == "1":
          logrelic()
        else:
          print("invalid option")
#REWARD INPUT FUNCTIONS
def logrelic():
  cont = True
  while cont == True:
    #check for  planet, create if missing
    planet = raw_input("planet: ")
    planetlist=bucket.n1ql_query(N1QLQuery('Select planetlist From Rewards where planetlist is not missing', p = planet)).get_single_result()
    if planet not in planetlist["planetlist"]:
       print("not in there")
       bucket.n1ql_query("UPDATE Rewards set planetlist = ARRAY_APPEND(Rewards.planetlist, " + repr(planet)+")").execute()
       bucket.n1ql_query(N1QLQuery('UPSERT INTO Rewards (Key, Value) VALUES ($p, {"nodelist" :  [] , "planet" : $p})' , p = planet)).execute()
    node = raw_input("node: ")
    #check for node, create if missing
    planetinfo= bucket.n1ql_query(N1QLQuery('Select nodelist From Rewards where planet = $p and nodelist is not missing', p = planet)).get_single_result()
    
    if planetinfo==None:
        new_node(node, planet)
    elif node not in planetinfo["nodelist"]:
        new_node(node, planet)
      

    fulllist, fullcount = import_list(node)
    
    while True:
      ro= raw_input("round: ")
      if ro == "q" or ro == "quit":
        cont = False
        break
      else:
          while ro.isdigit() == False:
              ro=(raw_input("enter a number:" ))
      re = raw_input("reward: ")
      if re == "q" or ro == "quit":
        cont = False
        break
      #check if reward has been previously entered in the database.  add if it isn't
      if re not in fulllist[int(ro)-1]: 
          print("not in there")
          fulllist[int(ro)-1].append(re)
          fullcount[int(ro)-1].append(1)
      else:
          for i, item in enumerate(fulllist[int(ro)-1]):
              if item == re:
                  fullcount[int(ro)-1][i] += 1
                  break
          
      #print(fulllist[int(ro)-1])
      #print(fullcount[int(ro)-1])

  for i, items in enumerate(fulllist):
      d = {}
      for j, item in enumerate(items):
          d[item] = fullcount[i][j]
      u = N1QLQuery("UPDATE Rewards set round"+str(i+1)+" = $m where node = "+repr(node) , m=d)
      bucket.n1ql_query(u).execute()
      print (d)
      
  cont = True

def new_node(nodename , planet):
    mission = raw_input("mission type: ")
    
    rounds = raw_input("number of rounds: ")
    while rounds.isdigit() == False:
        rounds = raw_input("number of rounds: ")
    stagestring = ""
    for i in range(1, int(rounds) + 1):
        stagestring = stagestring + '"round' + str(i) + '" : {}'
        if i != int(rounds):
            stagestring = stagestring + ', '
    
    bucket.n1ql_query(N1QLQuery('UPDATE Rewards set nodelist = ARRAY_APPEND(Rewards.nodelist, $n) where nodelist is not missing and planet = '+ repr(planet), n = nodename)).execute()
    p=bucket.n1ql_query(N1QLQuery('UPSERT INTO Rewards (Key, Value) VALUES ($n, {"planet" : '+ repr(planet) +', "node": $n , "type" : "nodesummary", "rounds" : '+repr(rounds)+', "mission": '+repr(mission)+ ', ' + stagestring + ' }) returning *', n=nodename)).execute()
    
    

#IMPORT FUNCTIONS
def import_list(node):
    print(node)
    q = bucket.n1ql_query(N1QLQuery('SELECT rounds FROM Rewards where node = $n', n = node)).get_single_result()
    while q == None:
      #print(q)
      q = bucket.n1ql_query(N1QLQuery('SELECT rounds FROM Rewards where node = $n', n = node)).get_single_result()
    rounds = q["rounds"]
    #r1 = N1QLQuery("SELECT round1 FROM Rewards WHERE node = " +'"'+ node+'"')# ' " ' single-quote, double-quote, single-quote so that the query reads ("node")
    #r2 = N1QLQuery("SELECT round2 FROM Rewards WHERE node = " +'"'+ node+'"')
    #r3 = N1QLQuery("SELECT round3 FROM Rewards WHERE node = " +'"'+ node+'"')
    #r4 = N1QLQuery("SELECT round4 FROM Rewards WHERE node = " +'"'+ node+'"')
    full_list = []
    full_count = []
    i = 1
    while i <= int(rounds):
        round1 = []
        count1 =[]
        r1 = N1QLQuery("SELECT round"+str(i)+" FROM Rewards WHERE node = " +'"'+ node+'"')
        for row in bucket.n1ql_query(r1):
            for key in row:
              for item in row[key]:
                  round1.append(str(item))
                  
                  count1.append(row[key][item])
                  print(str(item), row[key][item])
         
        full_list.append(round1)
        full_count.append(count1)
        i += 1
            

    return full_list, full_count
#import_list("bounty 5")
logrelic()
#new_node("wampus", "krampus")
"""menu()"""


