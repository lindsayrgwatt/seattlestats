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
