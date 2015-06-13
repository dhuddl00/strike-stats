import requests, json

def add_program(data):
  url = "http://localhost:9080/api/Programs"
  rqst = requests.post(url, data)
  print str(rqst.status_code) + "|" + data
  return rqst.json()

def add_pitcher(data):
  url = "http://localhost:9080/api/Pitchers"
  rqst = requests.post(url, data)
  print str(rqst.status_code) + "|" + data
  return rqst.json()

def add_game(data):
  url = "http://localhost:9080/api/Games"
  rqst = requests.post(url, data)
  print str(rqst.status_code) + "|" + data
  return rqst.json()

#Add Programs
def add_all(program_name, pitcher_names, games):
  program = add_program(json.dumps({"name":program_name}))
  [ add_pitcher(json.dumps({"program_id":program['id'],"name":p})) for p in pitcher_names ]
  [ add_game(json.dumps({"program_id":program['id'],"opponent":g['o'],"game_date":g['d']})) for g in games ]

add_all("El Reno", 
        ["Bob","Sam","David","Dan","Joe","Mike","Jason"], 
        [{"o":"North Tulsa","d":"2015-04-02"},
         {"o":"South OKC","d":"2015-04-08"},
         {"o":"Dover East","d":"2015-04-14"},
         {"o":"Ft Smith","d":"2015-05-02"},
         {"o":"Nebraska High","d":"2015-05-12"}])

add_all("South Dallas", 
        ["Walter","Jamar","Juan","Pablo","Teak"], 
        [{"o":"Tulsa","d":"2015-02-02"},
         {"o":"Dallas South","d":"2015-02-08"},
         {"o":"Lakeside","d":"2015-02-14"},
         {"o":"Austin","d":"2015-03-02"},
         {"o":"Nebraska","d":"2015-03-12"}])

#programs = [ add_program(x) for x in 
#    [ '{"name":"El Reno"}'
#    , '{"name":"Jessieville"}'
#    , '{"name":"JA Fair"}'
#    , '{"name":"Dover"}'] ]
#
#Add Pitchers



#from_url = "http://beaconmapper.appspot.com/MapPointObservation"
#fr = requests.get(from_url)

