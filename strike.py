import webapp2
import json
import logging
import datetime
import time
from google.appengine.ext import db
from google.appengine.api import users

class MainPageController(webapp2.RequestHandler):
    def get(self):
        self.response.write('''
<html><body><h1>S.T.R.I.K.E</h1></body></html>
''')

class ProgramListController(webapp2.RequestHandler):
    def get(self):
        e = Program.all()
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json.dumps(e.to_dict()))

class ApiProgramController(webapp2.RequestHandler):
    def get(self, program_id):
        e = Program.get_by_id(int(program_id))
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json.dumps(e.to_dict()))

class ApiProgramListController(webapp2.RequestHandler):
    def get(self):
        entities = Program.all()
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json.dumps([e.to_dict() for e in entities]))

    def post(self):
        js = self.request.body
        jo = json.loads(js)
        jo['create_time']=datetime.datetime.now()
        se = Program(**jo)
        se.put() 
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(js)
        
class ApiGameController(webapp2.RequestHandler):
    def get(self, game_id):
        e = Game.get_by_id(int(game_id))
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json.dumps(e.to_dict()))

class ApiGameListController(webapp2.RequestHandler):
    def get(self):
        entities = Game.all()
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json.dumps([e.to_dict() for e in entities]))

    def post(self):
        js = self.request.body
        jo = json.loads(js)
        jo['create_time']=datetime.datetime.now()
        p=Program.get_by_id(jo['program'])
        jo.pop('program',None)
        se = Game(program=p,**jo)
        se.put() 
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(js)
        
class ApiPitcherInningController(webapp2.RequestHandler):
    def get(self, pitcher_inning_id):
        e = PitcherInning.get_by_id(int(pitcher_inning_id))
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json.dumps(e.to_dict()))

class ApiPitcherInningListController(webapp2.RequestHandler):
    def get(self):
        entries = PitcherInning.all()
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json.dumps([e.to_dict() for e in entries]))

    def post(self):
        js = self.request.body
        jo = json.loads(js)
        jo['create_time']=datetime.datetime.now()
        g=Game.get_by_id(jo['game'])
        jo.pop('game',None)
#        jo['create_user']=users.get_current_user().email()
        se = PitcherInning(game=g,**jo)
        se.put() 
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(js)
        
class Program(db.Model):
  name = db.StringProperty(required=True)
  create_time = db.DateTimeProperty(required=True)

  def to_dict(self):
    return model_to_dict(self)

class Game(db.Model):
  program = db.ReferenceProperty(Program)
  game_date = db.StringProperty(required=True)
  opponent = db.StringProperty(required=True)
  create_time = db.DateTimeProperty(required=True)

  def to_dict(self):
    return model_to_dict(self)

class PitcherInning(db.Model):
  game = db.ReferenceProperty(Game)
  inning = db.IntegerProperty(required=True)
  pitcher = db.StringProperty(required=True)
  create_time = db.DateTimeProperty(required=True)
  shutdown_inning = db.BooleanProperty(required=True)
  less_than_13_pitches = db.BooleanProperty(required=True)
  retired_first_batter = db.BooleanProperty(required=True)
  three_and_out = db.BooleanProperty(required=True)
  strikeouts = db.IntegerProperty(required=True)
  ended_inning = db.BooleanProperty(required=True)

  def to_dict(self):
    return model_to_dict(self)

def model_to_dict(model):
  SIMPLE_TYPES = (int, long, float, bool, dict, basestring, list)
  output = {}
  output['id'] = model.key().id_or_name()
  for key, prop in model.properties().iteritems():
    value = getattr(model, key)

    if value is None or isinstance(value, SIMPLE_TYPES):
      output[key] = value
    elif isinstance(value, datetime.date):
      # Convert date/datetime to simple string representation
      #ms = time.mktime(value.utctimetuple()) * 1000
      #ms += getattr(value, 'microseconds', 0) / 1000
      #output[key] = int(ms)
      output[key] = str(value)
    elif isinstance(value, db.GeoPt):
      output[key] = {'lat': value.lat, 'lon': value.lon}
    elif isinstance(value, db.Model):
#      output[key] = value.to_dict()
      output[key] = value.key().id_or_name()
    else:
      raise ValueError('cannot encode ' + repr(prop))

  return output

#####
application = webapp2.WSGIApplication(
    [webapp2.Route('/', handler=MainPageController, name='home'),
     webapp2.Route('/api/PitcherInnings', handler=ApiPitcherInningListController, name='api_pitcher_innings'),
     webapp2.Route('/api/PitcherInnings/(\d+)', handler=ApiPitcherInningController),
     webapp2.Route('/api/Programs', handler=ApiProgramListController, name='api_programs'),
     webapp2.Route('/api/Programs/(\d+)', handler=ApiProgramController, name='api_programs'),
     webapp2.Route('/api/Games', handler=ApiGameListController, name='api_games'),
     webapp2.Route('/api/Games/(\d+)', handler=ApiGameController)
    ], debug=True)




