from lib.baseview import baseview
from models import *


class Default(baseview):

    def get(self):
        
        op = Opinion.all() #.fetch(1)

        if self.request.get('format') == 'json':
            self.render_json(op.fetch(10))
        else:
            self.render_template('opinions/index.html', { "opinions" : op })
        
        
    def post(self):
        o = Opinion(opinion = self.request.get('opinion'))
        o.put()
        
        self.redirect('/')        
            
    def put(self):
        print 'PUT'
        print self.request.get('x')
    
    
    def delete(self):
        print 'DELETE'