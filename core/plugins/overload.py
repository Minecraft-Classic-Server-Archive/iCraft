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
#                   <Jonathon Dunford> sk8rjwd@yahoo.com AKA "sk8rjwd"
#                   <Joseph Connor> destroyerx100@gmail.com AKA "destroyerx1"
#                   <Joshua Connor> fooblock@live.com AKA "Fooblock"
#                   <Kamyla Silva> supdawgyo@hotmail.com AKA "NotMeh"
#                   <Kristjan Gunnarsson> kristjang@ffsn.is AKA "eugo"
#                   <Nathan Coulombe> NathanCoulombe@hotmail.com AKA "Saanix"
#                   <Nick Tolrud> ntolrud@yahoo.com AKA "ntfwc"
#                   <Noel Benzinger> ronnygmod@gmail.com AKA "Dwarfy"
#                   <Randy Lyne> qcksilverdragon@gmail.com AKA "goober"
#                   <Willem van der Ploeg> willempieeploeg@live.nl AKA "willempiee"
#
#    Disclaimer: Parts of this code may have been contributed by the end-users.
#
#    iCraft is licensed under the Creative Commons
#    Attribution-NonCommercial-ShareAlike 3.0 Unported License. 
#    To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/3.0/
#    Or, send a letter to Creative Commons, 171 2nd Street,
#    Suite 300, San Francisco, California, 94105, USA.

from reqs.twisted.internet import reactor
from core.plugins import ProtocolPlugin
from core.decorators import *
from core.constants import *

class OverloadPlugin(ProtocolPlugin):
    
    commands = {
        "overload": "commandOverload",
        #"send": "commandSend",
        "blazer": "commandBlazer",
    }
    
    @player_list
    @admin_only
    @username_command
    def commandOverload(self, client, byuser, overriderank):
        "/overload username - Admin\nSends the users client a massive fake world."
        client.sendOverload()
        self.client.sendServerMessage("Overload sent to %s" % client.username)

    #@player_list
    #@mod_only
    #@username_command
    #def commandSend(self, client, byuser, overriderank):
        #"/send username [world] - Mod\nSends the users client another world."
        #if user.isMod():
            #self.client.sendServerMessage("You cannot send Staff!")
        #if len(parts) == 2:
            #self.client.sendServerMessage("Please specify a world ID.")
        #else:
            #world_id = parts[2]
            #user.changeToWorld("%s" % world_id)
            #else:
                #user.sendServerMessage("You were sent to '%s'." % self.client.world.id)
                #user.changeToWorld("default")
                #self.client.sendServerMessage("User %s was sent." % user.username)
        #else:
            #self.client.sendServerMessage("Your user is in another world!")

    @mod_only
    def commandBlazer(self, parts, byuser, overriderank):
        "/blazer - Mod\nBlazer!"
        for i in range(10):
            self.client.sendServerMessage("SPAM!")
