#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 12:34:31 2020

@author: erikedmonds
Script to initialize mongodb. 
"""

import pymongo, argparse, getpass
import polls_twitter as pt

class PasswordPromptAction(argparse.Action):
    """Get password argument from command line, avoiding cleartext."""
    def __init__(self, option_strings, dest=None, nargs=0, default=None, required=False, type=None, metavar=None, help=None):
        super(PasswordPromptAction, self).__init__(option_strings= option_strings, dest=dest, nargs=nargs, default=default,required=required,
            metavar=metavar, type=type, help=help)
    
    def __call__(self, parser, args, values, option_string=None):
        password=getpass.getpass()
        setattr(args, self.dest, password)

def mongo(database,collection,user, passwd):
    """Returns mongo database, or creates it if is doesn't exist. expects 
    database argument to be a tuple of db, (collection)"""
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    if database not in client.list_database_names():
        db = client[database]
        try:
            db.command("createUser", user, pwd=passwd,roles=["readWrite"])
            db.create_collection(collection)
        except pymongo.errors.OperationFailure:
            if collection not in db.list_collection_names():
                db.create_collection(collection)
        except pymongo.errors.CollectionInvalid:
            pass
        finally: return db
    database = client[database]
    if collection not in database.list_collection_names():
        database.create_collection(collection)
    return database[collection]


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', dest='user', type=str, required=True)
    parser.add_argument('-p', dest='password', action=PasswordPromptAction,type=str,required=True)
    parser.add_argument("-d", dest='database',type=str, required = False)
    parser.add_argument("-c", dest='collection', type=str, required = True)
    args = parser.parse_args()
    db_name = lambda x: x if x is not None else "data"
    collection = mongo(db_name(args.database),args.collection, args.user, args.password)
    api = pt.twitter_connection(pt.API_KEY,pt.API_SECRET,pt.ACCESS_TOKEN,pt.ACCESS_SECRET)
    Stream = pt.TwitterStream(api, collection)
    pt.get_tweet_stream(Stream, api, ["Trump"])