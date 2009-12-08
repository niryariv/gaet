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


        # org_get = getattr(cls, 'get')
        # 
        # def get(self, *params, **kws):
        #     p = list(params)
        #     action_name = p.pop(0)
        #     if action_name != '':
        #         action = getattr(cls, action_name)
        #         if len(p) == 0:
        #             action(self, *kws)
        #         else:
        #             action(self, p, *kws)
        #     else:
        #         org_get(self, *params, **kws)
        # 
        # setattr(cls, 'get', get)
        



class baseview(webapp.RequestHandler):
    '''
    Base class for views, which injects the metaclass and adds a render() convenience method
    
    '''
    __metaclass__ = baseview_meta


    def render(self, output, content_type=None):
        if content_type is not None:
            self.response.headers["Content-Type"] = content_type
            
        self.response.out.write(output)
        
    def error(self, error_code, tmpl_vars={}, text=None, quiet=False):
        # self.render_template(('errors/%s.html'% error_code), tmpl_vars)
        super(baseview, self).error(error_code)
        if quiet: return
        
        if text is not None:
            self.render(text)
        else:
            try: 
                self.render_template(('errors/%s.html'% error_code), tmpl_vars)
            except: # TODO: catch TemplateDoesNotExist
                return
            
        
    def render_template(self, path, tmpl_vars={}):
        '''
        Renders a template.
        path is the template's location inside app/templates (eg, for a template in "app/templates/hello/index.html" path would be "hello/index.html")
        Template variables can be either passed as dictionary to render() or stored in self.tmpl
        '''
        template_path = os.path.join(os.path.dirname(__file__), '..', 'app', 'templates', path)
        self.render(template.render(template_path, tmpl_vars))
    

    def db_to_dict(self, db_obj):
        ''' converts a DB object to a dictionary'''
        out = {}
        data = db_obj.__dict__['_entity']
        for k in data:
            out.update({k : str(data[k])})
            
        return out
        
    def render_json(self, data, indent=None, callback=None):
        ''' render a json response. indent is 0/1/2/etc identation level, callback is for JSONP callbacks'''
        clean_data = data
        
        if hasattr(data, '__module__') and data.__module__ == 'app.models':
            clean_data = self.db_to_dict(data)
            
        elif str(type(data)) == "<type 'list'>" and hasattr(data[0], '__module__') and data[0].__module__ == 'app.models':
            clean_data = []
            for i in data:
                clean_data.append(self.db_to_dict(i))

        json_out = simplejson.dumps(clean_data, indent=indent)
        if callback is not None:
            json_out = "%s( %s )" % (callback, json_out)
            
        self.render(json_out, 'application/json')
        
        