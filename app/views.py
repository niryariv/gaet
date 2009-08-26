from lib.baseview import baseview
from models import *


class Default(baseview):

    def get(self):
        
        o = Opinion.all()
        if o.count() == 0:
            o = []
        tmpl = { 
                    "opinions": o
                }
        
        self.render('opinions/index.html', tmpl)
        #self.render_json(tmpl)
        
        
    def post(self):
        o = Opinion(opinion = self.request.get('opinion'))
        o.put()
        
        self.redirect('/')        
            
    def put(self):
        print 'PUT'
        print self.request.get('x')
    
    
    def delete(self):
        print 'DELETE'