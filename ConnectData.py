# -*- coding: utf-8 -*-

import sqlite3 as db
from collections import Counter

class ExistsAlready(Exception):
    pass

class DataConnection():
    def __init__(self, fileName='meineRezepte.db'):
        self.con = db.connect(fileName)
        self.cur = self.con.cursor()
        cur = self.cur
        cur.execute('CREATE TABLE IF NOT EXISTS Dishes(Id INT, Name STR, Ingreds STR, Recipe STR, TagList STR)')
        cur.execute('CREATE TABLE IF NOT EXISTS Tags(Id STR)')
        self.allTags = set()
        self.availableTags = list(self.allTags)
        self.availableTags.sort()
        self.appliedTags = set()
        for tag in self.availableTags:
            self.__exec('CREATE TABLE IF NOT EXISTS %s(Dish INT)' % tag)

        self.__exec('SELECT * FROM Dishes')
        tmp = cur.fetchall()
        self.N = 1 if len(tmp) == 0 else max((x[0] for x in tmp)) + 1
        self.applyFilter()
        
    def __del__(self):
        self.con.commit()
        self.cur.close()
        self.con.close()

    def addRecipe(self, name, ingr, rcpe, tags, img=None):
        cur = self.cur
        ingr = ingr.replace('\n', '<br>')
        rcpe = '<p>' + rcpe.replace('\n', '</p><p>') + '</p>'

        # avoid duplicates
        self.__exec('SELECT Id FROM Dishes WHERE Name == "%s" AND Ingreds == "%s" AND Recipe == "%s"' % (name, ingr, rcpe))
        if len(cur.fetchall()) > 0:
            raise(ExistsAlready)
        
        self.__exec('INSERT INTO Dishes VALUES(%d, "%s", "%s", "%s", "%s")' % (self.N, name, ingr, rcpe, tags))
        tags = self._striptag(tags.lower())
        tags = tags.split(',')
        newTags = []
        for tag in tags:
            tag = tag.strip()
            if len(tag) == 0: continue
            if not tag in self.availableTags:
                self.__exec('INSERT INTO Tags VALUES("%s")' % tag)
                self.__exec('CREATE TABLE IF NOT EXISTS %s(Dish INT)' % tag)
                self.availableTags.append(tag)
                newTags.append(tag)
            self.__exec('INSERT INTO %s VALUES(%d)' %(tag, self.N))
        self.N += 1
        return newTags

    def getRecipe(self, id):
        self.__exec('SELECT * FROM Dishes WHERE Id = %d' % id)
        dish = self.cur.fetchone()
        name = dish[1]
        ingreds = dish[2]
        recipe = dish[3]
        image = None
        return name, ingreds, recipe, image

    def addFilter(self, tag):
        tag = self._striptag(tag)
        self.appliedTags.add(tag)
        self.applyFilter()

    def removeFilter(self, tag='', update = False):
        '''
        No tag given = remove last aplied tag.
        Else search and remove tag
        '''
        tag = self._striptag(tag)
        if len(self.appliedTags) == 0 or not tag in self.appliedTags:
            return
        if tag == '':
            self.appliedTags = self.appliedTags[:-1]
        else:
            self.appliedTags.remove(tag)
        if update:
            self.applyFilter()

    def searchDB(self, term):
        cur = self.cur
        dishlist = set()
        self.__exec('SELECT Id FROM Dishes WHERE Name LIKE "%%%s%%"' % term)
        findings = cur.fetchall()
        if len(findings) > 0:
            map( lambda x: dishlist.add(x[0]), findings )
        self.__exec('SELECT * FROM Tags WHERE Id LIKE "%%%s%%"' % term)
        tags = cur.fetchall()
        if len(tags) > 0:
            for tag in tags:
                self.__exec('SELECT Dish FROM %s' % tag)
                findings = cur.fetchall()
                if len(findings) > 0:
                    map( lambda x: dishlist.add(x[0]), findings )
        dishes = []
        for id in dishlist:
            self.__exec('SELECT * FROM Dishes Where Id == %d;' % id)
            dishes.append(cur.fetchall()[0])
        self.appliedTags = set()
        self.setDishes(dishes, True)

    def setDishes(self, dishList, updateTags = False):
        dishes = []
        tags = set()
        for dish in dishList:
            dishes.append( (dish[0], dish[1]) )
            for tag in dish[4].split(','):
                tags.add(tag.strip().lower())
        self.findings = dishes
        self.availableTags = list(tags)
        self.availableTags.sort()

    def applyFilter(self):
        cur = self.cur
        dishes = []
        if len(self.appliedTags) == 0:
            '''
            No filtering applied yet, so list all recipes
            '''
            self.__exec('SELECT * FROM Dishes')
            dishes = cur.fetchall()
            self.availableTags = set(self.allTags)
        else:
            ids = []
            tmp = []
            for tag in self.appliedTags:
                self.__exec('SELECT * FROM %s' % tag)
                for id in cur.fetchall():
                    tmp.append(id[0]) # possible hits

            '''
            if an entry has all applied tags, it is a hit
            '''
            cntKeys = list(Counter(tmp))
            cntVals = list(Counter(tmp).values())
            L = len(self.appliedTags)
            for i in xrange(len(cntVals)):
                if cntVals[i] == L:
                    ids.append(cntKeys[i])
                
            for id in ids:
                self.__exec('SELECT * FROM Dishes WHERE Id == %d' % id)
                tmp = cur.fetchone()
                dishes.append(tmp)
                
        self.setDishes(dishes, True)

    def _striptag(self, tag):
        return tag.lower().strip().replace(' ', '_') #\
#            .replace(u'ä', 'ae') \
#            .replace(u'ö', 'oe') \
#            .replace(u'ü', 'ue') \
#            .replace(u'ß', 'ss')


    def __exec(self, cmd):
        try:
            self.cur.execute(cmd)
        except db.OperationalError:
            print 'Error executing: ', cmd
