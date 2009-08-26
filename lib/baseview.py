import os

from django.utils import simplejson

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

class baseview_meta(type):
    '''
    This meta class adds Rails-like _method routing 
    So you can call PUT or DELETE by adding a _method=[PUT|DELETE] variable to an HTTP POST request
    Code by Toby Ho ( http://stackoverflow.com/questions/255157/how-to-override-http-request-verb-in-gae )
    
    '''
    def __init__(cls, name, bases, dct):
        super(baseview_meta, cls).__init__(name, bases, dct)
        org_post = getattr(cls, 'post')

        def post(self, *params, **kws):
            verb = self.request.get('_method')
            if verb:
                verb = verb.upper()
                if verb ==  'DELETE':
                    self.delete(*params, **kws)
                elif verb == 'PUT':
                    self.put(*params, **kws)
            else:
                org_post(self, *params, **kws)

        setattr(cls, 'post', post)

        



class baseview(webapp.RequestHandler):
    '''
    Base class for views, which injects the metaclass and adds a render() convenience method
    
    '''
    __metaclass__ = baseview_meta


    def render(self, path, tmpl_vars):
        '''
        Renders a template.
        path is the template's location inside app/templates (eg, for a template in "app/templates/hello/index.html" path would be "hello/index.html")
        Template variables can be either passed as dictionary to render() or stored in self.tmpl
        '''
        
        template_path = os.path.join(os.path.dirname(__file__), '..', 'app', 'templates', path)
        self.response.out.write(template.render(template_path, tmpl_vars))
        
    def render_json(self, tmpl_vars):
        # self.response.out.write(tmpl_vars)
        self.response.headers["Content-Type"] = 'Content-type: application/json'
        self.response.out.write(simplejson.dumps(tmpl_vars))


