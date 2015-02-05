# Refactor this page to look more like: https://gist.github.com/onyxfish/299803
# And http://stackoverflow.com/questions/2665743/how-do-i-create-a-postgresql-user-with-fabric

from fabric.api import local, run, env
from fabric.colors import green

env.project_name = 'seattlestats'
env.hosts = ['seattlestats.com']
env.user = 'ubuntu'
env.sudo_user = env.user
env.postgres_user = 'postgres'
env.postgres_user_password = '1234abcd'

def hello(name="world"):
    print("Hello %s!" % name)

def fake_deploy(name="test"):
    local("echo test")
    print(green("This text is green!"))

def fake_remote_deploy():
    run("echo fake deploy")

def update_server():
    sudo("apt-get update")
    sudo("apt-get upgrade")
    sudo("apt-get dist-upgrade")

def install_required_software():
    sudo("apt-get install nginx")
    sudo("easy_install supervisor") # TODO: Need to add init script for reboot
    sudo("apt-get install git")
    sudo("apt-get install binutils libproj-dev gdal-bin") # Geospatial libraries
    sudo("apt-get install postgresql-9.3 postgresql-server-dev-9.3 python-psycopg2")
    sudo("apt-get install build-essential libxml2-dev libgdal-dev libproj-dev libjson0-dev xsltproc docbook-xsl docbook-mathml") # PostGIS

def start_nginx():
    sudo("service nginx start")

def install_python_packages():
    sudo("apt-get install python-pip")
    sudo("pip install --upgrade pip")
    run("pip install virtualenv")
    run("virtualenv %(project_name)s" % env)
    sudo("pip install gunicorn")

def install_redis():
    sudo("apt-get install redis-server") # Will restart on reboot

def test_redis():
    run("redis-cli ping | grep 'PONG'")

def configure_postgres():
    sudo("psql -c \"CREATE ROLE %(postgres_user)s WITH ENCRYPTED PASSWORD '%(postgres_user_password)s';\"", user='postgres')

def install_postgis():
    run("wget http://download.osgeo.org/postgis/source/postgis-2.1.3.tar.gz")
    run("tar xfz postgis-2.1.3.tar.gz")
    run("cd postgis-2.1.3")
    run("./configure")
    run("make")
    sudo("make install")
    sudo("ldconfig")
    sudo("make comments-install")
    sudo("ln -sf /usr/share/postgresql-common/pg_wrapper /usr/local/bin/shp2pgsql")
    sudo("ln -sf /usr/share/postgresql-common/pg_wrapper /usr/local/bin/pgsql2shp")
    sudo("ln -sf /usr/share/postgresql-common/pg_wrapper /usr/local/bin/raster2pgsql")

def configure_server():
    update_server()
    install_required_software()
    start_nginx()
    install_python_packages()
    install_redis()
    test_redis()
    configure_postgres()
    install_postgis()
    

    # Install code from Github

    # Create databases and spatially enable

    # Create admin user

    # Create gunicorn log

    # Configure nginx

    # Create environment variables?
