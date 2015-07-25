# Refactor this page to look more like: https://gist.github.com/onyxfish/299803
# And http://stackoverflow.com/questions/2665743/how-do-i-create-a-postgresql-user-with-fabric
import os, sys

from fabric.api import local, run, env, sudo, settings, warn_only, cd, prefix
from fabric.colors import green
from fabric.contrib import django

env.github_url = "https://github.com/lindsayrgwatt/seattlestats"
env.http_dir = '/home/ubuntu'
env.project_name = 'seattlestats'
env.project_dir = os.path.join(env.http_dir, env.project_name)
env.hosts = ['ec2-54-69-157-24.us-west-2.compute.amazonaws.com']
env.user = 'ubuntu'
env.sudo_user = env.user
env.postgres_user_password = '1234abcd'
env.postgres_project_database = 'seattlestats'
env.postgres_project_user = 'seattlestats'
env.postgres_project_user_password = '1234abcd'

def hello(name="world"):
    print("Hello %s!" % name)

def fake_deploy(name="test"):
    local("echo test")
    print(green("This text is green!"))

def fake_remote_deploy():
    run("echo fake deploy")

def update_server():
    run("sudo apt-get update")
    run("sudo apt-get upgrade")
    run("sudo apt-get dist-upgrade")

def install_required_software():
    run("sudo apt-get install -y -q python-dev") # Needed to avoid GCC compilation error for pycrypto
    run("sudo apt-get install -y -q nginx")
    run("sudo apt-get install -y -q supervisor")
    run("sudo service supervisor restart")
    run("sudo apt-get install -y -q git")
    run("sudo apt-get install -y -q binutils libproj-dev gdal-bin") # Geospatial libraries
    run("sudo apt-get install -y -q postgresql postgresql-contrib python-psycopg2")
    run("sudo apt-get install -y -q postgis postgresql-9.3-postgis-2.1")
    run("sudo apt-get install -y -q build-essential libxml2-dev libgdal-dev libproj-dev libjson0-dev xsltproc docbook-xsl docbook-mathml") # PostGIS

def start_nginx():
    sudo("service nginx start")

def install_python_packages():
    run("sudo apt-get install -y -q python-pip")
    run("sudo pip install --upgrade pip")
    run("sudo pip install virtualenv")
    run("sudo pip install virtualenvwrapper")
    run("virtualenv %(project_name)s" % env) # Creates virtualenv in project dir
    run("source %(project_name)s/bin/activate" % env)
    run("pip install gunicorn")

def install_redis():
    run("sudo apt-get install -y -q redis-server") # Will restart on reboot

def test_redis():
    run("sudo redis-cli ping | grep 'PONG'")

def configure_postgres():
    run("sudo psql -U postgres -c \"ALTER USER postgres WITH PASSWORD '%(postgres_user_password)s';\"" % env)
    run("sudo find / -name \"pg_hba.conf\" -print")
    print "Now you need to do the following to change peer authentication to md5"
    print "SSH into your server e.g., ssh env.user@env.hosts"
    print "Change the file listed in print statement above e.g., sudo vi /etc/postgresql/9.3/main/pg_hba.conf"
    print "Change the lines:"
    print "local   all             postgres                                peer"
    print "local   all             all                                     peer"
    print "to:"
    print "local   all             postgres                                md5"
    print "local   all             all                                     md5"
    print "Now manually run fab restart_postgres"

def restart_postgres():
    run("sudo service postgresql restart")

def configure_server():
    update_server()
    install_required_software()
    start_nginx()
    install_python_packages()
    install_redis()
    test_redis()
    configure_postgres()

def deploy():
    # Install or update the code
    with settings(warn_only=True):
        if run('test -d ' + env.project_dir).failed:
            run("sudo git clone %(github_url)s" % env) # First install of code
        else:
            with cd(env.project_dir):
                run("sudo git pull")
    
    # Install or update any required packages
    with prefix('source %(project_dir)s/bin/activate' % env):
        with cd(env.project_dir):
            run("pip install -r requirements.txt") # DO NOT use sudo here or will install outside your virtualenv

    # http://nurupoga.org/articles/deployment-with-fabric-and-virtualenv
    # http://stackoverflow.com/questions/9337149/is-virtualenv-recommended-for-django-production-server -> scroll down
    # http://dangoldin.com/2014/02/10/using-virtualenv-in-production/
    # http://thecodeship.com/deployment/deploy-django-apache-virtualenv-and-mod_wsgi/

def set_up_database():
    run("sudo psql -U postgres -c \"CREATE DATABASE %(postgres_project_database)s;\"" % env)
    run("sudo psql -U postgres -c \"CREATE USER %(postgres_project_user)s WITH PASSWORD '%(postgres_project_user_password)s';\"" % env)
    run("sudo psql -U postgres <<EOF\n\c %(postgres_project_database)s\nCREATE EXTENSION postgis;\nEOF" % env)
    run("sudo psql -U postgres <<EOF\n\c %(postgres_project_database)s\nCREATE EXTENSION postgis_topology;\nEOF" % env)
    run("sudo psql -U postgres -c \"GRANT ALL PRIVILEGES ON DATABASE %(postgres_project_database)s TO %(postgres_project_user)s;\"" % env)

def test_database_created():
    run("sudo psql -U %(postgres_project_user)s <<EOF\n\c %(postgres_project_database)s\nSELECT postgis_full_version();\nEOF" % env)
    # Should see something like

#def first_deploy():
    
    # Create admin user

    # Create gunicorn log

    # Configure nginx and gunicorn and supervisor

    # Create environment variables

    # Add celery