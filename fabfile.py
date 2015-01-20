# Refactor this page to look more like: https://gist.github.com/onyxfish/299803


from fabric.api import local, run, env
from fabric.colors import green

env.hosts = ['seattlestats.com']
env.user = 'ubuntu'

def hello(name="world"):
    print("Hello %s!" % name)

def fake_deploy(name="test"):
    local("echo test")
    print(green("This text is green!"))

def fake_remote_deploy():
    run("echo fake deploy")

def configure_server():
    # Server hygiene
    run("sudo apt-get update")
    run("sudo apt-get upgrade")
    run("sudo apt-get dist-upgrade")

    # Install required software packages
    run("sudo apt-get install nginx")
    run("sudo service nginx start")
    run("sudo easy_install supervisor")
    run("sudo apt-get install git")
    run("sudo apt-get install binutils libproj-dev gdal-bin") # Geospatial libraries
    run("sudo apt-get install postgresql-9.3 postgresql-server-dev-9.3 python-psycopg2")
    run("sudo apt-get install build-essential libxml2-dev libgdal-dev libproj-dev libjson0-dev xsltproc docbook-xsl docbook-mathml") # PostGIS

    # Install Python-powered items
    run("sudo apt-get install python-pip")
    run("sudo pip install --upgrade pip")
    run("pip install virtualenv")
    run("virtualenv seattlestats")
    run("sudo pip install gunicorn")

    # Configure PostgreSQL

    # Install & Configure PostGIS

    # Install & Configure Redis

    # Install code from Github

    # Create gunicorn log

    # Configure nginx

