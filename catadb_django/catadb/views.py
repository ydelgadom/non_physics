from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse
from django.db import models
from django.views.decorators.csrf import csrf_exempt

from catadb_django.settings import BASE_DIR

import json
import os
import uuid

from templates import templates
from mysqldb import mysqldb as db
from utils import crypt
from utils.unicode_util import to_unicode
from utils import forms_util


def start(request):
    """
    username and password template
    """
    if request.method == 'GET':
        tc = templates.Template()
        html = unicode(tc.make_start_template(request, data={}))
        return HttpResponse(html)

    elif request.method == 'POST':
        tc = templates.Template()
        udb = db.Users()

        # get the email and validate it
        email = request.POST["email"]
        email = email.lower().strip()
        user = udb.get_by_email(email)
        if not user:
            data = {
                "message": "This email is not registered"
            }
            html = unicode(tc.make_start_template(request, data))
            return HttpResponse(html)

        # get the password and validate it
        password = request.POST["password"]
        password = password.strip()
        password = crypt.convert_to_md5(password)
        if password != user['password']:
            data = {
                "message": "Wrong password!"
            }
            html = unicode(tc.make_start_template(request, data))
            return HttpResponse(html)

        # make url:
        serialized = crypt.encrypt_userid(str(user['userid']))
        url = unicode("/welcome/" + serialized)

        # redirect to Welcome URL
        return redirect(url)


def signup(request):
    """
    create new user
    """
    if request.method == "POST":
        tc = templates.Template()
        udb = db.Users()

        # username
        username = request.POST["username"]
        username = to_unicode(username.strip())
        user = udb.get_by_username(username)
        if user:
            data = {
                "message": "Username already exists"
            }
            html = unicode(tc.make_start_template(request, data))
            return HttpResponse(html)

        # email
        email = request.POST["email"]
        email = to_unicode(email.lower().strip())
        user = udb.get_by_email(email)
        if user:
            data = {
                "message": "This email is already registered"
            }
            html = unicode(tc.make_start_template(request, data))
            return HttpResponse(html)

        # real name
        realname = request.POST["realname"]
        realname = to_unicode(realname.strip())

        # get the password and validate it
        password = request.POST["password"]
        password = to_unicode(password.strip())
        password = crypt.convert_to_md5(password)

        # create user
        userid = udb.insert(realname, username, email, password)
        if not userid:
            html = "OOPS!"
            return HttpResponse(html)

        # make url:
        serialized = crypt.encrypt_userid(str(userid))
        url = unicode("/welcome/" + serialized)

        # redirect to Welcome URL
        return redirect(url)


def welcome(request, encrypted_userid):
    """
    show older tasting notes and
    create a new tasting note
    """
    if request.method == "GET":
        # decrypt the userid
        userid = crypt.decrypt_userid(encrypted_userid)
        if not userid:
            html = "OOPS!"
            return HttpResponse(html)

        udb = db.Users()
        user = udb.get_by_userid(userid)
        if not userid:
            html = "OOPS!"
            return HttpResponse(html)

        # check if this is the first time that a user
        # visits this page
        phrase = u"Welcome back!"
        if encrypted_userid in request.META['HTTP_REFERER']:
            phrase = u"Your tasting notes were successfully saved."

        # url where user can see older tasting notes
        url_old_tasting_notes = "/old_notes/" + encrypted_userid

        template_data = {
            'name': unicode(user['real_name'].title()),
            'welcome_text': phrase,
            'url_old_tasting_notes': url_old_tasting_notes,
        }
        tc = templates.Template()
        html = unicode(tc.make_welcome_template(request, template_data))
        return HttpResponse(html)

    elif request.method == "POST":
        # decrypt the userid
        userid = crypt.decrypt_userid(encrypted_userid)
        if not userid:
            html = "OOPS!"
            return HttpResponse(html)

        udb = db.Users()
        user = udb.get_by_userid(userid)
        if not userid:
            html = "OOPS!"
            return HttpResponse(html)

        wine_type = request.POST["wine_type"]
        if not wine_type:
            html = "ERROR: wine_type"
            return HttpResponse(html)

        # make tasting notes URL
        url = '/notes/' + encrypted_userid + '/tasting_notes_' + wine_type 
        url = unicode(url)

        if wine_type == "red":
            color = "#990000"
        else:
            color = "#99CC33"

        data = {
            'url': url,
            'username': unicode(user['username'].title()),
            'type': unicode(wine_type),
            'color': unicode(color),
        }
        tc = templates.Template()
        html = unicode(tc.make_tastingnotes_template(request, data))
        return HttpResponse(html)


def new_tasting_note(request, encrypted_userid, wine_type):
    """
    red wine or white wine tasting notes form.
    """
    if request.method == "POST":
        # decrypt the userid
        userid = crypt.decrypt_userid(encrypted_userid)
        if not userid:
            html = "OOPS!"
            return HttpResponse(html)

        udb = db.Users()
        user = udb.get_by_userid(userid)
        if not userid:
            html = "OOPS!"
            return HttpResponse(html)

        # store both pictures in the data base
        try:
            front_pic = request.FILES["front_label"]
            extension = os.path.splitext(front_pic.name)[1]
            front_pic_name = "uploads/" + str(uuid.uuid4()) + extension
            pic_name = os.path.join(BASE_DIR, front_pic_name)
            try:
                output_file = open(pic_name, 'wb')
            except Exception as e:
                print e
            output_file.write(front_pic.read())
            print "file " + front_pic_name + " is uploaded."
        except:
            front_pic_name = ""

        # store both pictures in the data base
        try:
            back_pic = request.FILES["back_label"]
            extension = os.path.splitext(back_pic.name)[1]
            back_pic_name = "uploads/" + str(uuid.uuid4()) + extension
            pic_name = os.path.join(BASE_DIR, back_pic_name)
            output_file = open(pic_name, 'wb')
            output_file.write(back_pic.read())
        except:
            back_pic_name = ""

        pics = {
            'front_label': to_unicode(front_pic_name),
            'back_label': to_unicode(back_pic_name)
        }

        # process all the elements from the forms
        args = request.POST
        args['pics'] = pics
        if 'red' in wine_type:
            args['type'] = 'red'
        else:
            args['type'] = 'white'

        res = forms_util.store_wine_data(args, userid)
        if not res:
            html = "OOPS!"
            return HttpResponse(html)

        # redirect to Welcome URL
        url = unicode("/welcome/" + encrypted_userid)
        return redirect(url)


@csrf_exempt
def old_notes(request, encrypted_userid):
    """
    Template where stored tasting notes are shown
    """
    if request.method == "GET":
        # decrypt the userid
        userid = crypt.decrypt_userid(encrypted_userid)
        if not userid:
            html = "OOPS!"
            return HttpResponse(html)

        # get the list of stores wines
        wdb = db.Wines()
        wines = wdb.get_by_userid(userid)
        if not wines:
            # redirect to Welcome URL
            url = unicode("/welcome/" + encrypted_userid)    
            return redirect(url)

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
        if 'old_notes' in request.META['HTTP_REFERER']:
            templatedata['message'] = "The entry was deleted succesfully."

        tc = templates.Template()
        html = to_unicode(tc.make_old_tastingnotes_template(request, templatedata))
        return HttpResponse(html)

    elif request.method == "POST":
        # decrypt the userid
        userid = crypt.decrypt_userid(encrypted_userid)
        if not userid:
            html = "OOPS!"
            return HttpResponse(html)

        # get the selected wine
        wineid = request.POST["name"]
        if not wineid:
            # redirect to Welcome URL
            url = unicode("/welcome/" + encrypted_userid)    
            return redirect(url)

        # get the list of stored wines
        wdb = db.Wines()
        wines = wdb.get_by_userid(userid)
        if not wines:
            # redirect to Welcome URL
            url = unicode("/welcome/" + encrypted_userid)    
            return redirect(url)

        # pick the selected wine
        wine = [x for x in wines if x['wineid']==wineid]
        if not wine:
            print "ERROR: ", wineid
            # redirect to Welcome URL
            url = unicode("/welcome/" + encrypted_userid)    
            return redirect(url)

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
        html = unicode(tc.make_old_tastingnotes_template(request, templatedata))
        return HttpResponse(html)


def delete_wine(request, encrypted_userid, wineid):
    """
    delete wine with wineid from the DB and also
    the pictures from the /uploads/ folder.
    """
    if request.method == "GET":
        # decrypt the userid
        userid = crypt.decrypt_userid(encrypted_userid)
        if not userid:
            html = "OOPS!"
            return HttpResponse(html)

        # delete the pictures
        wdb = db.Wines()
        wine = wdb.get_by_wineid(wineid)
        if not wine:
            html = "no wine!"
            return HttpResponse(html)        

        if wine['pics']['front_label']:
            pic_path = os.path.join(BASE_DIR, wine['pics']['front_label'])
            os.remove(pic_path)

        if wine['pics']['back_label']:
            pic_path = os.path.join(BASE_DIR, wine['pics']['back_label'])
            os.remove(pic_path)

        # delete wine from database
        res = wdb.delete_by_wineid(wineid)
        if not res:
            print "ERROR: ", wineid
            # redirect to Welcome URL
            url = unicode("/welcome/" + encrypted_userid)    
            return redirect(url)

        # redirect to Old Tasting Notes URL
        url = unicode("/old_notes/" + encrypted_userid)
        return redirect(url)
