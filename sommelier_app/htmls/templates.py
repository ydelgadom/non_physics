import jinja2
import os

class Template():
    path_red = "jinja/red-tasting-notes.jinja.html"
    path_white = "jinja/white-tasting-notes.jinja.html"
    path_start = "jinja/start.jinja.html"
    path_welcome = "jinja/welcome.jinja.html" 
    path_wine = "jinja/wine.jinja.html"


    def make_start_template(self, data={}):
        """
        Template that asks for email and password
        """
        path = self.path_start
        #try:
        templateLoader = jinja2.FileSystemLoader(
            searchpath=os.path.join(
                os.path.dirname(__file__)))
        templateEnv = jinja2.Environment(loader=templateLoader)
        template = templateEnv.get_template(path)
        return template.render(data)

        #except Exception as e:
        #    print "Failed to render start template %s" % e
        #return None


    def make_welcome_template(self, data):
        """
        Template that asks to see older entries or
        to create a new tasting note.
        """
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


    def make_tastingnotes_template(self, wine_type, data):
        """
        Form with the tasting notes for red and white wine.
        """
        if wine_type == "red":
            path = self.path_red
        else:
            path = self.path_white
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


    def make_old_tastingnotes_template(self, data):
        """
        Form to show list of stored wines 
        """
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
