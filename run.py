#    iCraft is Copyright 2010 both
#
#    The Archives team:
#                   <Adam Guy> adam@adam-guy.com AKA "Adam01"
#                   <Andrew Godwin> andrew@aeracode.org AKA "Aera"
#                   <Dylan Lukes> lukes.dylan@gmail.com AKA "revenant"
#                   <Gareth Coles> colesgareth2@hotmail.com AKA "gdude2002"
#
#    And,
#
#    The iCraft team:
#                   <Andrew Caluzzi> tehcid@gmail.com AKA "tehcid"
#                   <Andrew Dolgov> fox@bah.org.ru AKA "gothfox"
#                   <Andrew Horn> Andrew@GJOCommunity.com AKA "AndrewPH"
#                   <Brad Reardon> brad@bradness.co.cc AKA "PixelEater"
#                   <Clay Sweetser> CDBKJmom@aol.com AKA "Varriount"
#                   <James Kirslis> james@helplarge.com AKA "iKJames"
#                   <Jason Sayre> admin@erronjason.com AKA "erronjason"
#                   <Joseph Connor> destroyerx100@gmail.com AKA "destroyerx1"
#                   <Nathan Coulombe> NathanCoulombe@hotmail.com AKA "Saanix"
#                   <Nick Tolrud> ntolrud@yahoo.com AKA "ntfwc"
#                   <Noel Benzinger> ronnygmod@gmail.com AKA "Dwarfy"
#                   <Randy Lyne> qcksilverdragon@gmail.com AKA "goober"
#                   <Willem van der Ploeg> willempieeploeg@live.nl AKA "willempiee"
#
#    iCraft is licensed under the Creative Commons
#    Attribution-NonCommercial-ShareAlike 3.0 Unported License. 
#    To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/3.0/
#    Or, send a letter to Creative Commons, 171 2nd Street,
#    Suite 300, San Francisco, California, 94105, USA.

#!/usr/bin/python

import os
import sys
import time
import logging
import os,shutil
from myne.constants import *
from logging.handlers import SMTPHandler

if not sys.version_info[:2] == (2, 6):
    print ("ATTENTION: Do you need help with iCraft? hlmc.net or irc.esper.net #iCraft")
    try:
        if (os.uname()[0] == "Darwin"):
            print ("NOTICE: Sorry, but your Mac OS X version is outdated. We recommend running iCraft for Mac on 10.6+ or you need to install Python 2.6.x on 10.5")
        else:
            print ("NOTICE: Sorry, but you need Python 2.6.x (Zope, Twisted and SimpleJSON) to run iCraft; http://www.python.org/download/releases/2.6.5/")
    except:
        print ("NOTICE: Sorry, but you need Python 2.6.x (Zope, Twisted and SimpleJSON) to run iCraft; http://www.python.org/download/releases/2.6.5/")
    exit(1);

def LogTimestamp():
    if os.path.exists("logs/console/console.log"):
        shutil.copy("logs/console/console.log", "logs/console/console" +time.strftime("%Y%m%d%H%M%S",time.localtime(time.time())) +".log")
        f=open("logs/console/console.log",'w')
        f.close()
LogTimestamp()
logging.basicConfig(
    format="%(asctime)s - %(levelname)7s - %(message)s",
    level=("--debug" in sys.argv) and logging.DEBUG or logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",  filename="logs/console/console.log",
)
# define a Handler which writes DEBUG messages or higher to the sys.stderr
console = logging.StreamHandler()
# set a format which is simpler for console use
formatter = logging.Formatter("%(asctime)s - %(levelname)7s - %(message)s")
# tell the handler to use this format
console.setFormatter(formatter)
# add the handler to the root logger
logging.getLogger('').addHandler(console)

print ("Now starting up iCraft %s..." % VERSION)
print ("- Please don't forget to check for updates. Do you need help with iCraft? Feel free to stop by; http://hlmc.net/ | irc.esper.net #iCraft")

try:
    from twisted.internet import *
    from zope.interface import *
except ImportError:
    logging.log(logging.ERROR, "Sorry, but you need Twisted + Zope to run iCraft; http://twistedmatrix.com/trac/wiki/Downloads You can also try using this, readme included: http://www.mediafire.com/?i2wmtfnzmay")
    exit(1);

try:
    import Image
except ImportError:
    logging.log(logging.INFO, "Sorry, but you'll need PIL to use imagedraw.")

from twisted import reactor
from myne.server import MyneFactory
from myne.controller import ControllerFactory

reactor.callLater(6*60*60, LogTimestamp)#24hours*60minutes*60seconds
factory = MyneFactory()
controller = ControllerFactory(factory)
reactor.listenTCP(factory.config.getint("network", "port"), factory)
reactor.listenTCP(factory.config.getint("network", "controller_port"), controller)
money_logger = logging.getLogger('TransactionLogger')
fh = logging.FileHandler('logs/server.log')
formatter = logging.Formatter("%(asctime)s: %(message)s")
fh.setFormatter(formatter)
#Add the handler
money_logger.addHandler(fh)

# Setup email handler
if factory.config.has_section("email"):
    emh = SMTPHandler(
        factory.config.get("email", "host"),
        factory.config.get("email", "from"),
        [factory.config.get("email", "to")],
        factory.config.get("email", "subject"),
    )
    emh.setLevel(logging.ERROR)
    logging.root.addHandler(emh)

try:
    reactor.run()
finally:
    # Make sure worlds are flushed
    logging.log(logging.INFO, "Saving server meta...")
    factory.saveMeta()
    logging.log(logging.INFO, "Flushing worlds to disk...")
    for world in factory.worlds.values():
        logging.log(logging.INFO, "Saving: %s" % world.basename);
        world.stop()
        world.save_meta()
    print ("ATTENTION: Please don't forget to check for updates; http://hlmc.net/ | irc.esper.net #iCraft")
    exit(1);
