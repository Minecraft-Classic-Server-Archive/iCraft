#    iCraft is Copyright 2010-2011 both
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

import apsw, traceback
from collections import deque
from threading import Thread

class dbconnection(Thread):
    "Establish a connection to the memory database and define the cursor."

# Startup variables
    def __init__(self, world):
        self.dbpath = world.basename +"/database.db"
        self.memcon = apsw.Connection(':memory:')
        self.memcursor = self.memcon.cursor()
        self.memlist = deque()
        self.disklist = deque()
        self.worlddb = apsw.Connection('{0}'.format(self.dbpath))
        self.worldcursor = self.worlddb.cursor()
        self.worldcursor.execute("pragma journal_mode=wal")
        self.counter = 0
        self.run = True
        try:
            self.memcursor.execute('CREATE TABLE main (id INTEGER PRIMARY KEY,matbefore INTEGER, matafter INTEGER, name VARCHAR(50), date DATE)')
        except:
            pass
        try:
            self.worldcursor.execute('CREATE TABLE main (id INTEGER PRIMARY KEY,matbefore INTEGER, matafter INTEGER, name VARCHAR(50), date DATE)')
        except:
            pass

# Core functions, not normally used by plugins
    def tableopen(self):
        self.memcursor = None
        self.worldcursor = None
        self.memcon.backup("main", self.worlddb, "main").step()
        self.memcursor = self.memcon.cursor()
        self.worldcursor = self.worlddb.cursor()
        print ("World opened succesfully.")

    def dbclose(self):
        self.memwrite()
        self.diskwrite()
        print ("Database closing..")
        self.memcursor = None
        self.worldcursor = None
        self.memcon = None
        self.worlddb = None
        self.run = False

    def writetable(self, blockoffset, matbefore, matafter, name, date):
        if self.run:
            self.memlist.append((blockoffset, matbefore, matafter, name, date))
            self.disklist.append((blockoffset, matbefore, matafter, name, date))
            if len(self.memlist) > 150:
                self.memwrite()
                self.counter = self.counter + 1
                if self.counter > 5:
                    self.diskwrite()

    def memwrite(self):
        if self.run:
            self.memcursor.executemany("INSERT OR REPLACE INTO main VALUES (?,?,?,?,?)",self.memlist)
            self.memlist.clear()
            print ("Memory database updated.")

    def diskwrite(self):
        if self.run:
            self.worldcursor.executemany("INSERT OR REPLACE INTO main VALUES (?,?,?,?,?)",self.disklist)
            self.disklist.clear()
            self.counter = 0
            print ("Disk database updated.")

    def readdb(self, entry, column, filt = None):
        returncolumn = 'id, matbefore, matafter, name, date'
        # Currently tested to accept tuples with strings, lists with strings. won't work with things that have only a single entry, so single strings and ints are out
        # Example filters are "and where date is < foo and > foo"
        if len(self.memlist)>0:
            self.memwrite()
        if isinstance(entry, (int, str)): 
            if filt != None:
                string = 'select * from main as main where {0} = ? {1}'.format(column,filt)
            else:
                string = 'select * from main as main where {0} = ?'.format(column)
            print(string)
            self.memcursor.execute(string, [entry])
            undolist = self.memcursor.fetchall()
            if len(undolist) == 1:
                undolist = undolist[0]
            return(undolist)
            #Or you could put your old stuff in here
        if isinstance(entry, (tuple, list)):
            qmarks = ('?,'*len(entry))[:-1]
            if filt != None:
                string = 'select * from main as main where {0} in ({1}) {2}'.format(column,qmarks,filt)
            else:
                string = 'select * from main as main where {0} in ({1})'.format(column,qmarks)
            print (string)
            self.memcursor.execute(string, entry)
            print(self.memcursor.fetchall())
            undolist = self.memcursor.fetchall()
            return(undolist)
        else:
            print traceback.format_exc()
            print ("ERROR - Please make sure readdb input is correct!")
            print ("Dumping Variables..")
            print ("Entry:", entry)
            print ("Column:", column)
            print ("Return Column:", returncolumn)
            print ("string:", string)
            print ("Qmarks:", qmarks)
            print ("Filter:", filt)
