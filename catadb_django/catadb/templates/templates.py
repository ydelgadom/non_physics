from django.template.context_processors import csrf

import jinja2
import os

class Template():
    path_notes = "jinja/tasting-grid.jinja.html"
    path_start = "jinja/start.jinja.html"
    path_welcome = "jinja/welcome.jinja.html" 
    path_wine = "jinja/wine.jinja.html"


    def make_start_template(self, request, data={}):
        """
        Template that asks for email and password
        """
        data['csrf_token'] = csrf(request)['csrf_token']
        path = self.path_start
        templateLoader = jinja2.FileSystemLoader(
            searchpath=os.path.join(
                os.path.dirname(__file__)))
        templateEnv = jinja2.Environment(loader=templateLoader)
        template = templateEnv.get_template(path)
        return template.render(data)


    def make_welcome_template(self, request, data):
        """
        Template that asks to see older entries or
        to create a new tasting note.
        """
        data['csrf_token'] = csrf(request)['csrf_token']
        path = self.path_welcome
        try:
            templateLoader = jinja2.FileSystemLoader(
                searchpath=os.path.join(
                    os.path.dirname(__file__)))
            templateEnv = jinja2.Environment(loader=templateLoader)
            template = templateEnv.get_template(path)
            return template.render(data)

        except Exception as e:
            print "Failed to render welcome template %s" % e
        return None


    def make_tastingnotes_template(self, request, data):
        """
        Form with the tasting notes for red and white wine.
        """
        data['csrf_token'] = csrf(request)['csrf_token']
        path = self.path_notes
        try:
            templateLoader = jinja2.FileSystemLoader(
                searchpath=os.path.join(
                    os.path.dirname(__file__)))
            templateEnv = jinja2.Environment(loader=templateLoader)
            template = templateEnv.get_template(path)
            return template.render(data)

        except Exception as e:
            print "Failed to render template %s" % e
        return None


    def make_old_tastingnotes_template(self, request, data):
        """
        Form to show list of stored wines 
        """
        data['csrf_token'] = csrf(request)['csrf_token']
        path = self.path_wine
        try:
            templateLoader = jinja2.FileSystemLoader(
                searchpath=os.path.join(
                    os.path.dirname(__file__)))
            templateEnv = jinja2.Environment(loader=templateLoader)
            template = templateEnv.get_template(path)
            return template.render(data)

        except Exception as e:
            print "Failed to render template %s" % e
        return None
