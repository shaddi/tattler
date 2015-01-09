from fabric.api import cd, lcd, local, env, run, settings, execute, hosts
from fabric.contrib.files import exists
from fabric.operations import put, prompt, sudo, get

import datetime
import glob

def bbb():
    """ Host config for local Vagrant VM. """
    env.hosts = ['root@192.168.7.2'] # USB connection
    env.password="" # blank password login

def connect():
    local('sudo ifconfig eth2 192.168.7.1 netmask 255.255.255.0')
    local('ssh root@192.168.7.2')

def date():
    local('sudo ifconfig eth2 192.168.7.1 netmask 255.255.255.0')
    datestr = datetime.datetime.utcnow().strftime("%a %b  %-d %H:%M:%S UTC %Y")
    local("ssh root@192.168.7.2 'date -s \"%s\"'" % datestr)

def buildreq():
    """
    Deploys all the requirements onto the box.
    """
    with open('requirements.txt') as f:
        for line in f:
            run('pip install %s' % line.strip())
    put('deps', '/root')
    with cd('deps'):
        run('dpkg -i *.deb')
    run('sudo apt-get install -y python-imaging python-smbus')

def rmreq():
    with open('requirements.txt') as f:
        for line in f:
            run('yes | pip uninstall %s' % line.strip())
    pkgs = []
    with cd('deps'):
        files = run('ls *.deb')
        files = files.split()
        for f in files:
            pkgname = f.split("_")[0]
            pkgs.append(pkgname)
    run('sudo apt-get remove -y python-imaging python-smbus %s' % (" ".join(pkgs)))

def deploy():
    print "Move along."
