import webapp2
import json
import logging
import datetime
import time
import os
from google.appengine.ext.webapp import template
from google.appengine.ext import db
from google.appengine.api import users

HEADER_HTML='''
<html>
    <head>
        <link rel="stylesheet" href="http://yui.yahooapis.com/pure/0.6.0/pure-min.css">
        <style>
          .center {
            margin-left: auto;
            margin-right: auto;
            width: 70%;
            background-color: #b0e0e6;
          }
        </style>
    </head>
    <body>
        <div style="padding-left:25px">
            <div>
                <h1>S.T.R.I.K.E</h1>
            </div>
'''

FOOTER_HTML='''
        </div>
    </body>
</html>
'''

class MainPageController(webapp2.RequestHandler):
    def get(self):
        body_html='<div><a href="' + webapp2.uri_for('games') + '">Games</a></div>'
        self.response.write(HEADER_HTML + body_html + FOOTER_HTML)

class GameListPageController(webapp2.RequestHandler):
    def get(self):
        body_html = '''<table class="pure-table pure-table-bordered">
                        <thead>
                            <tr>
                                <th>Program</th>
                                <th>Opponent</th>
                                <th>Date</th>
                                <th>Link</th>
                            </tr>
                        </thead>'''  
        body_html += '<tbody>'
        for e in Game.all():
            body_html += '<tr><td>' + str(e.program.name) + \
                        '</td><td>' + e.opponent + \
                        '</td><td>' + e.game_date + \
                        '</td><td><a href="' + webapp2.uri_for('games')  + "/" + str(e.key().id_or_name()) + '">Go</a></td></tr>'
        body_html += '</tbody></table>' 
        #template_values = {
        #    'game_html': body_html
        #}
        #path = os.path.join(os.path.dirname(__file__), 'gamelist.html')
        #self.response.out.write(template.render(path, template_values))
        self.response.out.write(HEADER_HTML + body_html + FOOTER_HTML)

class GamePageController(webapp2.RequestHandler):
    def get(self, game_id):
        game = Game.get_by_id(int(game_id))
        pitchers = []
        for p in Pitcher.all():
          pitchers.append({'name':p.name, 'id':str(p.key().id_or_name())})
#        pitchers = Pitcher.all() #["Bob Jackson", "Sam Walters", "Mike Stevens"]

        template_values = {
            'program_name': game.program.name,
            'opponent_name': game.opponent,
            'pitchers': pitchers,
            'innings': range(1,9),
            'game_id': game_id,
        }

        path = os.path.join(os.path.dirname(__file__), 'game.html')
        self.response.out.write(template.render(path, template_values))

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
        
class ApiPitcherController(webapp2.RequestHandler):
    def get(self, pitcher_id):
        e = Program.get_by_id(int(pitcher_id))
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json.dumps(e.to_dict()))

class ApiPitcherListController(webapp2.RequestHandler):
    def get(self):
        entities = Pitcher.all()
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json.dumps([e.to_dict() for e in entities]))

    def post(self):
        js = self.request.body
        jo = json.loads(js)
        jo['create_time']=datetime.datetime.now()
        p=Program.get_by_id(int(jo['program_id']))
        se = Pitcher(program=p,**jo)
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
        p=Program.get_by_id(int(jo['program_id']))
        #jo.pop('program',None)
        se = Game(program=p,**jo)
        se.put() 
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(js)
        
class ApiGamePitcherInningListController(webapp2.RequestHandler):
    def get(self, game_id):
        g = Game.get_by_id(int(game_id))
        entries = db.GqlQuery("SELECT * FROM PitcherInning WHERE game = :1", g)
        self.response.headers['Content-Type'] = 'application/json'
        nlist = []
        for entry in entries:
          o = entry.to_dict()
          o["pitcher_name"] = entry.pitcher.name
          nlist.append(o)
        self.response.write(json.dumps([e for e in nlist]))

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
        g=Game.get_by_id(int(jo['game_id']))
        p=Pitcher.get_by_id(int(jo['pitcher_id']))
        jo['strikeouts'] = int(jo['strikeouts'])
        jo['inning'] = int(jo['inning'])
        #logging.debug("value of my g ")
        #check for uniqueness
        #entries = db.GqlQuery("SELECT * FROM PitcherInning WHERE game = :1 AND pitcher = :2 AND inning = :3", g, p, jo['inning'])

        resp = ""
        #if len(entries) == 0:
        se = PitcherInning(game=g,pitcher=p,**jo)
        se.put() 
        #resp = js
        resp = json.dumps(se.to_dict())
        #resp = json.dumps(g.to_dict())
        #else:
        #  resp = '{"msg":"ERROR: This Inning and Pitcher combo already exists for this game"}'
        self.response.headers.add_header("Access-Control-Allow-Origin", "*") 
        self.response.headers.add_header("Access-Control-Allow-Headers", "x-requested-with") 
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(resp)
        
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

class Pitcher(db.Model):
  program = db.ReferenceProperty(Program)
  name = db.StringProperty(required=True)
  create_time = db.DateTimeProperty(required=True)

  def to_dict(self):
    return model_to_dict(self)

class PitcherInning(db.Model):
  game = db.ReferenceProperty(Game)
  inning = db.IntegerProperty(required=True)
  pitcher = db.ReferenceProperty(Pitcher)
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
      output[key] = str(value)
    elif isinstance(value, db.Model):
      output[key] = value.key().id_or_name()
    else:
      raise ValueError('cannot encode ' + repr(prop))

  return output

#####
application = webapp2.WSGIApplication(
    [webapp2.Route('/', handler=MainPageController, name='home'),
     webapp2.Route('/Games', handler=GameListPageController, name='games'),
     ('/Games/(\d+)', GamePageController),
     ('/api/PitcherInnings', ApiPitcherInningListController),
     ('/api/PitcherInnings/(\d+)', ApiPitcherInningController),
     ('/api/Programs', ApiProgramListController),
     ('/api/Programs/(\d+)', ApiProgramController),
     ('/api/Games', ApiGameListController),
     ('/api/Games/(\d+)', ApiGameController),
     ('/api/Games/(\d+)/PitcherInnings', ApiGamePitcherInningListController),
     ('/api/Pitchers', ApiPitcherListController),
     ('/api/Pitchers/(\d+)', ApiPitcherController)
    ], debug=True)




