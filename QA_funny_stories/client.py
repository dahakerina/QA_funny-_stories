#!/usr/bin/env python
import sys
import urllib2
import json


class createURL:

    def __init__(self):
        pass

    def list_all(self):
        f = urllib2.urlopen('http://localhost:5000/list_all')
        fread = f.read()
        #print fread
        return [fread, f.code]

    def list_story(self, i):
        f = urllib2.urlopen('http://localhost:5000/story_id/' + str(i))
        fread = f.read()
        #print fread
        return [fread, f.code]

    def author_stories(self, name):
        f = urllib2.urlopen('http://localhost:5000/author_story/' + name)
        fread = f.read()
        #print fread
        return [fread, f.code]

    def list_rating(self, r):
        f = urllib2.urlopen('http://localhost:5000/list_rating/' + str(r))
        fread = f.read()
        #print fread
        return [fread, f.code]

    def add_story(self, arg1, arg2):
        story = {'name': arg1, 'body': arg2}
        url1 = 'http://localhost:5000/add_story'
        req = urllib2.Request(url1)
        req.add_header('Content-Type', 'application/json')
        f = urllib2.urlopen(req, json.dumps(story))
        fread = f.read()
        #print fread
        return [fread, f.code]

    def registration(self, arg1, arg2):
        story = {'log': arg1, 'pass': arg2}
        url1 = 'http://localhost:5000/registration'
        req = urllib2.Request(url1)
        req.add_header('Content-Type', 'application/json')
        f = urllib2.urlopen(req, json.dumps(story))
        fread = f.read()
        #print fread
        return [fread, f.code]

    def log_in(self, arg1, arg2):
        story = {'log': arg1, 'pass': arg2}
        url1 = 'http://localhost:5000/log_in'
        req = urllib2.Request(url1)
        req.add_header('Content-Type', 'application/json')
        f = urllib2.urlopen(req, json.dumps(story))
        fread = f.read()
        #print fread
        return [fread, f.code]

    def log_out(self):
        f = urllib2.urlopen('http://localhost:5000/log_out')
        fread = f.read()
        #print fread
        return [fread, f.code]

    def like_story(self, ID):
        f = urllib2.urlopen('http://localhost:5000/like/' + str(ID))
        fread = f.read()
        #print fread
        return [fread, f.code]

    def dislike_story(self, ID):
        f = urllib2.urlopen('http://localhost:5000/dislike/' + str(ID))
        fread = f.read()
        #print fread
        return [fread, f.code]

    def del_story(self, ID):
        f = urllib2.urlopen('http://localhost:5000/delete/' + str(ID))
        fread = f.read()
        #print fread
        return [fread, f.code]

    def help(self):
        print 'list_all'
        print 'list_story'
        print 'author_stories'
        print 'list_rating'
        print 'add_story'
        print 'registration'
        print 'log_in'
        print 'log_out'
        print 'like_story'
        print 'dislike_story'
        print 'del_story'

    def startCls(self):
        a = self
        try:
            f = getattr(a, sys.argv[1])
            if callable(f):
                if len(sys.argv) == 2:
                    return f()
                if len(sys.argv) == 3:
                    return f(sys.argv[2])
                if len(sys.argv) == 4:
                    return f(sys.argv[2], sys.argv[3])
        except:
            print "Command not found"


if __name__ == "__main__":
    a = createURL()
    a.startCls()
