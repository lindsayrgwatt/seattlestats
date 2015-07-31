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
env.virtualenv_dir = os.path.join(env.project_dir, 'venv')
env.hosts = ['ec2-52-10-132-110.us-west-2.compute.amazonaws.com']
env.user = 'ubuntu'
env.sudo_user = env.user
env.postgres_user_password = 'iluvpostgres'
env.postgres_project_database = 'seattlestats'
env.postgres_project_user = 'seattlestats'
env.postgres_project_user_password = '1234abcd'

def update_server():
    run("sudo apt-get -y -q update")
    run("sudo apt-get -y -q upgrade")
    # All the options in the following command are to avoid getting stuck on a grub update screen
    # http://askubuntu.com/questions/146921/how-do-i-apt-get-y-dist-upgrade-without-a-grub-config-prompt
    run('sudo DEBIAN_FRONTEND=noninteractive apt-get -y -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold" dist-upgrade')

def install_required_software():
    run("sudo apt-get -y -q install python-dev") # Needed to avoid GCC compilation error for pycrypto
    run("sudo apt-get -y -q install nginx")
    run("sudo apt-get -y -q install git")
    run("sudo apt-get -y -q install binutils libproj-dev gdal-bin") # Geospatial libraries
    run("sudo apt-get -y -q install postgresql postgresql-contrib python-psycopg2")
    run("sudo apt-get -y -q install postgis postgresql-9.3-postgis-2.1")
    run("sudo apt-get -y -q install build-essential libxml2-dev libgdal-dev libproj-dev libjson0-dev xsltproc docbook-xsl docbook-mathml") # PostGIS

def start_nginx():
    sudo("service nginx start")

def install_python_packages():
    run("sudo apt-get -y -q install python-pip")
    run("sudo pip install --upgrade pip")
    run("sudo pip install virtualenv")

def install_redis():
    run("sudo apt-get -y -q install redis-server") # Will restart on reboot

def test_redis():
    run("sudo redis-cli ping | grep 'PONG'")

def configure_postgres():
    print "Now you need to do two things:"
    print "1. Give the postgres user in your database a password"
    print "2. Update the authentication method of postgres so that you can actually connect"
    print "Some details here: http://suite.opengeo.org/4.1/dataadmin/pgGettingStarted/firstconnect.html"
    print "Part 1."
    print "1. ssh into your server: ssh %(user)s@%(hosts)s" % env
    print "2. open psql as the postgres user. No password is required as none exists yet: sudo -u postgres psql postgres"
    print "3. change the password: \password postgres"
    print "4. quit: \q"
    print "5. end session: exit"
    print "\n"
    print "Part 2."
    run("sudo find / -name \"pg_hba.conf\" -print")
    print "Now you need to do the following to change peer authentication to md5"
    print "1. SSH into your server as above"
    print "2. Change the file listed in print statement above e.g., sudo vi /etc/postgresql/9.3/main/pg_hba.conf"
    print "3. Change the lines:"
    print "local   all             postgres                                peer"
    print "local   all             all                                     peer"
    print "to:"
    print "local   all             postgres                                md5"
    print "local   all             all                                     md5"
    print "4. Save, end the SSH session and from your local machine run: fab restart_postgres"

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

def set_up_database():
    run("sudo psql -U postgres -c \"CREATE DATABASE %(postgres_project_database)s;\"" % env)
    run("sudo psql -U postgres -c \"CREATE USER %(postgres_project_user)s WITH PASSWORD '%(postgres_project_user_password)s';\"" % env)
    run("sudo psql -U postgres <<EOF\n\c %(postgres_project_database)s\nCREATE EXTENSION postgis;\nEOF" % env)
    run("sudo psql -U postgres <<EOF\n\c %(postgres_project_database)s\nCREATE EXTENSION postgis_topology;\nEOF" % env)
    run("sudo psql -U postgres -c \"GRANT ALL PRIVILEGES ON DATABASE %(postgres_project_database)s TO %(postgres_project_user)s;\"" % env)

def test_database_created():
    run("sudo psql -U %(postgres_project_user)s <<EOF\n\c %(postgres_project_database)s\nSELECT postgis_full_version();\nEOF" % env)
    # Should see something like:
    #                                                                          postgis_full_version                                                                         
    # ----------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #  POSTGIS="2.1.2 r12389" GEOS="3.4.2-CAPI-1.8.2 r3921" PROJ="Rel. 4.8.0, 6 March 2012" GDAL="GDAL 1.10.1, released 2013/08/26" LIBXML="2.9.1" LIBJSON="UNKNOWN" RASTER
    # (1 row)

def deploy():
    # Install or update the code
    with settings(warn_only=True):
        if run('test -d ' + env.project_dir).failed:
            # First install of code
            run("sudo git clone %(github_url)s" % env) # First install of code

            # Set up virtualenv and change write permissions
            run("sudo virtualenv %(virtualenv_dir)s" % env)
            run("sudo chmod -R 754 %(virtualenv_dir)s" % env)

            install_gunicorn()

        else:
            with cd(env.project_dir):
                run("sudo git pull")
    
    # Install or update any required packages
    with prefix('source %(virtualenv_dir)s/bin/activate' % env):
        with cd(env.project_dir):
            run("pip install -r requirements.txt") # DO NOT use sudo here or will install outside your virtualenv
            # You can see this packages installed at env.virtualenv_dir/lib/python2.7/site-packages

            run("sudo git pull")

def install_gunicorn():
    with prefix('source %(virtualenv_dir)s/bin/activate' % env):
        run("pip install gunicorn")


#run("sudo apt-get install -y -q supervisor")
#run("sudo service supervisor restart")
    
# http://nurupoga.org/articles/deployment-with-fabric-and-virtualenv
# http://stackoverflow.com/questions/9337149/is-virtualenv-recommended-for-django-production-server -> scroll down
# http://dangoldin.com/2014/02/10/using-virtualenv-in-production/
# http://thecodeship.com/deployment/deploy-django-apache-virtualenv-and-mod_wsgi/


#def first_deploy():
    
    # Create admin user

    # Create gunicorn log

    # Configure nginx and gunicorn and supervisor

    # Create environment variables

    # Add celery

def hello(name="world"):
    print("Hello %s!" % name)

def fake_deploy(name="test"):
    local("echo test")
    print(green("This text is green!"))

def fake_remote_deploy():
    run("echo fake deploy")

