import datetime
from google.appengine.ext import db

class Opinion(db.Model):
  opinion        = db.StringProperty   (required=True)
  conceived_at   = db.DateTimeProperty (auto_now_add=True)
  changed_mind_at= db.DateTimeProperty (auto_now=True)
  

