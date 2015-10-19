===================================================

ROUTER:
router 192.168.1.1 / 4141800

===================================================

APACHE2:

1. restart service:
sudo service apache2 restart

2. I'll use Django
https://www.djangoproject.com/start/

3. deploy django & apache in Ubuntu
https://www.digitalocean.com/community/tutorials/how-to-serve-django-applications-with-apache-and-mod_wsgi-on-ubuntu-14-04

  cd catadb
  # create virtual env (own version of pip and python)
  virtualenv catadbenv
  # activate env.
  source catadb/bin/activate
  # to deactivate
  deactivate
  ....
  #before restarting apache2, install mod_wsgi:
  sudo apt-get install libapache2-mod-wsgi



# to give access to media files 
sudo chmod -R 777 /home/ydelgado/Public/catadb_django/uploads/
