#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 16:11:42 2020

@author: erikedmonds

Generation of Twitter data stream to a Mongo Database. 
"""

import tweepy, time, twitter
#from io import UnsupportedOperation

#TODO: Hide tokens
ACCESS_SECRET = '6OD5KiRDjjL2jpYlyiCJzYSuzgQdJgR22Qnfj1Sj0FrhM'
ACCESS_TOKEN = '1222549710503923713-KaMJ9gjQ9lsrx5ASnV4BPVb44B35BJ'
API_KEY = 'ze1WpqToFkEbT5lkWwtPyAYVo'
API_SECRET = 'xZvhYerdf5cZI8vE3M4PRkVuHJAg0qWfbrHnBIrAqwJW54y8A7'

def native_wrapper():
    return twitter.oauth.OAuth(ACCESS_TOKEN, ACCESS_SECRET, API_KEY, API_SECRET)
 
#Listener object. Singleton?
class TwitterStream(tweepy.StreamListener):
    """A listener to handle twitter streaming data"""
    
    def __init__(self, api, mongodb):
        """To keep memory from getting too big, tweets are written out
        to a file. 
        UPDATE: File now written to mongo database. mongodb parameter refers to 
        a mongo database collection object."""
        super().__init__(api)
        #if 'write' not in dir(std_out):
        #    raise UnsupportedOperation("Must be a writeable stream.")
        #self.out = std_out
        self.mongodb = mongodb
        
    def on_status(self, status):
        """Currently writes stream of tweets to a text file. Need to 
        update to write to database.
        UPDATE: Now streams to mongo database."""
        if status.place is not None:
            self.mongodb.insert_one({"place":status.place.full_name,"user":status.user._json,"tweet":status.text})
        

def twitter_connection(*args,native=False, **kwargs):
    """Allows authentication with either Twitter or Tweepy. If using Twitter, an 
    auth object needs to be passed in. If using Tweepy, access and consumer tokens
    need to be passed in."""
    if native:
        try:
            assert kwargs.get('auth') is not None
            auth = kwargs.get('auth')
            oauth = tweepy.OAuthHandler(auth.consumer_key, auth.consumer_secret)
            oauth.set_access_token(auth.token, auth.token_secret)
        except AssertionError:
            raise ValueError('auth object must be passed if using native api')
    else:
        if len(args) != 4: 
            raise TypeError("Incorrect number of authentication arguments given")
        oauth = tweepy.OAuthHandler(args[0],args[1])
        oauth.set_access_token(args[2],args[3])
    return tweepy.API(oauth)


def get_tweet_stream(listener, auth, queries, duration = 300):
    """Opens up a stream, and runs for a set duration (in seconds).
    Default is 5 minutes"""
    stream = tweepy.Stream(auth.auth, listener = listener)
    stream.filter(track = queries, is_async = True)
    start = time.monotonic()
    while (time.monotonic() - start <= duration):
        pass
    stream.disconnect()
    
