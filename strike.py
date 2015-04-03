import webapp2
import json
import logging
import datetime
import time
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

ENTRY_FORM_HTML='''
<form class="pure-form">
  <fieldset>
    <table class="pure-table">
      <tbody>
        <tr>
          <th>Pitcher:</th>
          <td>
            <span id="in_pitcher"></span>
          </td>
        </tr>
        <tr>
          <th>Inning:</th>
          <td>
            <select id="in_inning">
              <option>1</option>
              <option>2</option>
              <option>3</option>
              <option>4</option>
              <option>5</option>
              <option>6</option>
              <option>7</option>
              <option>8</option>
              <option>9</option>
            </select>
          </td>
        </tr>
        <tr>
          <th>Shutdown:</th>
          <td>
            <input id="in_shutdown" type="checkbox">
          </td>
        </tr>
        <tr>
          <th>Less than 13 pitches:</th>
          <td>
            <input id="in_less_than_13_pitches" type="checkbox">
          </td>
        </tr>
        <tr>
          <th>Retired First Batter:</th>
          <td>
            <input id="in_retired_first_batter" type="checkbox">
          </td>
        </tr>
        <tr>
          <th>Three and out:</th>
          <td>
            <input id="in_three_and_out" type="checkbox">
          </td>
        </tr>
        <tr>
          <th>Strikeouts:</th>
          <td>
            <select id="in_strikeouts">
              <option>0</option>
              <option>1</option>
              <option>2</option>
              <option>3</option>
            </select>
          </td>
        </tr>
        <tr>
          <th>Ended Inning:</th>
          <td>
            <input id="in_ended_inning" type="checkbox">
          </td>
        </tr>
        <tr>
          <td colspan="2" class="center">
            <a class="pure-button" href="#">Submit</a></div>
          </td>
        </tr>
      </tbody>
    </table>
  </fieldset>
</form>
'''

class MainPageController(webapp2.RequestHandler):
    def get(self):
        self.response.write(HEADER_HTML + FOOTER_HTML)

class GameListPageController(webapp2.RequestHandler):
    def get(self):
        bodyHtml = '''<table class="pure-table pure-table-bordered">
                        <thead>
                            <tr>
                                <th>Program</th>
                                <th>Opponent</th>
                                <th>Date</th>
                                <th>Link</th>
                            </tr>
                        </thead>'''  
        bodyHtml += '<tbody>'
        for e in Game.all():
            bodyHtml += '<tr><td>' + str(e.program.name) + \
                        '</td><td>' + e.opponent + \
                        '</td><td>' + e.game_date + \
                        '</td><td><a href="' + webapp2.uri_for('games')  + "/" + str(e.key().id_or_name()) + '">Go</a></td></tr>'
        bodyHtml += '</tbody></table>' 
        self.response.write(HEADER_HTML + bodyHtml + FOOTER_HTML)

class GamePageController(webapp2.RequestHandler):
    def get(self, game_id):
        game = Game.get_by_id(int(game_id))
        bodyHtml = '<div>' + \
                        '<span style="padding-right:25px">' + game.program.name+ '</span>'\
                        '<span style="padding-right:25px">vs</span>'\
                        '<span style="padding-right:25px">' + game.opponent + '</span>'\
                    '</div>'

        bodyHtml += ENTRY_FORM_HTML

        self.response.write(HEADER_HTML + bodyHtml + FOOTER_HTML)

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
      output[key] = str(value)
    elif isinstance(value, db.GeoPt):
      output[key] = {'lat': value.lat, 'lon': value.lon}
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
     ('/api/Games/(\d+)', ApiGameController)
    ], debug=True)




