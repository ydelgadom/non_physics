import tornado.ioloop
import tornado.web
import json
import os
import uuid

from htmls import templates
from mysqldb import mysqldb as db
from utils import crypt
from utils.unicode_util import to_unicode
from utils import forms_util


class StartHandler(tornado.web.RequestHandler):
    """
    username and password template
    """
    def get(self):
        tc = templates.Template()
        html = unicode(tc.make_start_template())
        self.write(html)

    def post(self):
        tc = templates.Template()
        udb = db.Users()

        # get the email and validate it
        email = self.get_argument("email")
        email = email.lower().strip()
        user = udb.get_by_email(email)
        if not user:
            data = {
                "message": "This email is not registered"
            }
            html = unicode(tc.make_start_template(data))
            self.write(html)
            return

        # get the password and validate it
        password = self.get_argument("password")
        password = password.strip()
        password = crypt.convert_to_md5(password)
        if password != user['password']:
            data = {
                "message": "Wrong password!"
            }
            html = unicode(tc.make_start_template(data))
            self.write(html)
            return

        # make url:
        serialized = crypt.encrypt_userid(str(user['userid']))
        url = unicode("/welcome/" + serialized)

        # redirect to Welcome URL
        self.redirect(url)


class SignupHandler(tornado.web.RequestHandler):
    """
    create new user
    """
    def post(self):
        tc = templates.Template()
        udb = db.Users()

        # username
        username = self.get_argument("username")
        username = to_unicode(username.strip())
        user = udb.get_by_username(username)
        if user:
            data = {
                "message": "Username already exists"
            }
            html = unicode(tc.make_start_template(data))
            self.write(html)
            return

        # email
        email = self.get_argument("email")
        email = to_unicode(email.lower().strip())
        user = udb.get_by_email(email)
        if user:
            data = {
                "message": "This email is already registered"
            }
            html = unicode(tc.make_start_template(data))
            self.write(html)
            return

        # real name
        realname = self.get_argument("realname")
        realname = to_unicode(realname.strip())

        # get the password and validate it
        password = self.get_argument("password")
        password = to_unicode(password.strip())
        password = crypt.convert_to_md5(password)

        # create user
        userid = udb.insert(realname, username, email, password)
        if not userid:
            self.write("OOPS!!")
            return

        # make url:
        serialized = crypt.encrypt_userid(str(userid))
        url = unicode("/welcome/" + serialized)

        # redirect to Welcome URL
        self.redirect(url)


class WelcomeHandler(tornado.web.RequestHandler):
    """
    show older tasting notes and
    create a new tasting note
    """
    def get(self, encrypted_userid):
        # decrypt the userid
        userid = crypt.decrypt_userid(encrypted_userid)
        if not userid:
            self.write("OOPS!")
            return

        udb = db.Users()
        user = udb.get_by_userid(userid)
        if not userid:
            self.write("OOPS!")
            return

        # check if this is the first time that a user
        # visits this page
        phrase = u"How are you doing?  Glad to have you here again."
        if encrypted_userid in self.request.headers.get('Referer'):
            phrase = u"Your tasting notes were successfully saved."

        # url where user can see older tasting notes
        url_old_tasting_notes = "/old_notes/" + encrypted_userid

        template_data = {
            'name': unicode(user['real_name'].title()),
            'welcome_text': phrase,
            'url_old_tasting_notes': url_old_tasting_notes,
        }
        tc = templates.Template()
        html = unicode(tc.make_welcome_template(template_data))
        self.write(html)

    def post(self, encrypted_userid):
        # decrypt the userid
        userid = crypt.decrypt_userid(encrypted_userid)
        if not userid:
            self.write("OOPS!")
            return

        udb = db.Users()
        user = udb.get_by_userid(userid)
        if not userid:
            self.write("OOPS!")
            return

        wine_type = self.get_argument("wine_type")
        if not wine_type:
            self.write("ERROR: wine_type")
            return

        # make tasting notes URL
        url = '/notes/' + encrypted_userid + '/tasting_notes_' + wine_type 
        url = unicode(url)

        data = {
            'url': url,
            'username': unicode(user['username'].title()),
        }
        tc = templates.Template()
        html = unicode(tc.make_tastingnotes_template(wine_type, data))
        self.write(html)


class NotesHandler(tornado.web.RequestHandler):
    """
    red wine or white wine tasting notes form.
    """
    def post(self, encrypted_userid, wine_type):
        # decrypt the userid
        userid = crypt.decrypt_userid(encrypted_userid)
        if not userid:
            self.write("OOPS!")
            return

        udb = db.Users()
        user = udb.get_by_userid(userid)
        if not userid:
            self.write("OOPS!")
            return

        # store both pictures in the data base
        try:
            file_pic = self.request.files["front_label"]
            file_pic = file_pic[0]
            original_fname = file_pic['filename']
            extension = os.path.splitext(original_fname)[1]
            filename_front = "data/uploads/" + str(uuid.uuid4()) + extension
            output_file = open(filename_front, 'wb')
            output_file.write(file_pic['body'])
            print "file " + filename_front + " is uploaded."
        except:
            filename_front = ""

        # store both pictures in the data base
        try:
            file_pic = self.request.files["back_label"]
            file_pic = file_pic[0]
            original_fname = file_pic['filename']
            extension = os.path.splitext(original_fname)[1]
            filename_back = "data/uploads/" + str(uuid.uuid4()) + extension
            output_file = open(filename_back, 'wb')
            output_file.write(file_pic['body'])
            print "file " + filename_back + " is uploaded."
        except:
            filename_back = ""

        pics = {
            'front_label': to_unicode(filename_front),
            'back_label': to_unicode(filename_back)
        }

        # process all the elements from the forms
        args = { k: self.get_argument(k) for k in self.request.arguments }
        args['pics'] = pics
        if 'red' in wine_type:
            args['type'] = 'red'
        else:
            args['type'] = 'white'

        res = forms_util.store_wine_data(args, userid)
        if not res:
            self.write("OOPS")
            return

        # redirect to Welcome URL
        url = unicode("/welcome/" + encrypted_userid)
        self.redirect(url)


class OldNotesHandler(tornado.web.RequestHandler):
    """
    Template where stored tasting notes are shown
    """
    def get(self, encrypted_userid):
        # decrypt the userid
        userid = crypt.decrypt_userid(encrypted_userid)
        if not userid:
            self.write("OOPS!")
            return

        # get the list of stores wines
        wdb = db.Wines()
        wines = wdb.get_by_userid(userid)
        if not wines:
            # redirect to Welcome URL
            url = unicode("/welcome/" + encrypted_userid)    
            self.redirect(url)
            return

        wines = [{ 'name': x['name'].title(),
                   'wineid': x['wineid'] } for x in wines]

        templatedata = {
            'wines': wines,
            'show_tasting_note': False,
            'welcome_url': unicode("/welcome/" + encrypted_userid),
            'color': "#990000;",
            'post_url': unicode("/old_notes/" + encrypted_userid)
        }

        # check if delete button is redirecting here
        print "referer", self.request.headers.get('Referer')
        if 'old_notes' in self.request.headers.get('Referer'):
            templatedata['message'] = "The entry was deleted succesfully."

        tc = templates.Template()
        html = to_unicode(tc.make_old_tastingnotes_template(templatedata))
        self.write(html)

    def post(self, encrypted_userid):
        # decrypt the userid
        userid = crypt.decrypt_userid(encrypted_userid)
        if not userid:
            self.write("OOPS!")
            return

        # get the selected wine
        wineid = self.get_argument("name")
        if not wineid:
            # redirect to Welcome URL
            url = unicode("/welcome/" + encrypted_userid)    
            self.redirect(url)
            return

        # get the list of stored wines
        wdb = db.Wines()
        wines = wdb.get_by_userid(userid)
        if not wines:
            # redirect to Welcome URL
            url = unicode("/welcome/" + encrypted_userid)    
            self.redirect(url)
            return

        # pick the selected wine
        wine = [x for x in wines if x['wineid']==wineid]
        if not wine:
            print "ERROR: ", wineid
            # redirect to Welcome URL
            url = unicode("/welcome/" + encrypted_userid)    
            self.redirect(url)
            return

        # list of wines for <select>
        wines = [{ 'name': x['name'].title(),
                   'wineid': x['wineid'] } for x in wines]

        wine = wine[0]
        if wine['typed'] == "red":
            color = "#990000;"
        else:
            color = "#99CC33;"

        templatedata = forms_util.compose_wine_data_for_template(wine)
        templatedata['wines'] = wines
        templatedata['show_tasting_note'] = True
        templatedata['welcome_url'] = unicode("/welcome/" + encrypted_userid)
        templatedata['color'] = color
        templatedata['post_url'] = unicode("/old_notes/" + encrypted_userid)
        templatedata['delete_url'] = unicode("/delete/" + encrypted_userid + "/" + wineid)

        tc = templates.Template()
        html = unicode(tc.make_old_tastingnotes_template(templatedata))
        self.write(html)


class DeleteWineHandler(tornado.web.RequestHandler):
    def get(self, encrypted_userid, wineid):
        # decrypt the userid
        userid = crypt.decrypt_userid(encrypted_userid)
        if not userid:
            self.write("OOPS!")
            return

        # delete the pictures
        wdb = db.Wines()
        wine = wdb.get_by_wineid(wineid)
        if not wine:
            self.write("no wine")        

        path = "/home/ydelgado/sommelier_app/"
        if wine['pics']['front_label']:
            pic_path = path + wine['pics']['front_label']
            os.remove(pic_path)

        if wine['pics']['back_label']:
            pic_path = path + wine['pics']['back_label']
            os.remove(pic_path)

        # delete wine from database
        res = wdb.delete_by_wineid(wineid)
        if not res:
            print "ERROR: ", wineid
            # redirect to Welcome URL
            url = unicode("/welcome/" + encrypted_userid)    
            self.redirect(url)
            return

        # redirect to Old Tasting Notes URL
        url = unicode("/old_notes/" + encrypted_userid)
        self.redirect(url)



settings = {
    "xsrf_cookies": False
}

if __name__ == "__main__":
    application = tornado.web.Application([
        (r"/", StartHandler),
        (r"/sign_up", SignupHandler),
        (r"/welcome/([^/]+)", WelcomeHandler),
        (r"/notes/([^/]+)/([^/]+)", NotesHandler),
        (r"/old_notes/([^/]+)", OldNotesHandler),
        (r"/delete/([^/]+)/([^/]+)", DeleteWineHandler),
        (r'/static/js/(.*)', tornado.web.StaticFileHandler, {'path': "/home/ydelgado/Public/sommelier_app/htmls/jinja/static/js"}),
        (r'/static/css/(.*)', tornado.web.StaticFileHandler, {'path': "/home/ydelgado/Public/sommelier_app/htmls/jinja/static/css"}),
        (r'/old_notes/data/uploads/(.*)', tornado.web.StaticFileHandler, {'path': "/home/ydelgado/Public/sommelier_app/data/uploads"}),
    ], debug=True, **settings)
    application.listen(8000)
    tornado.ioloop.IOLoop.current().start()

