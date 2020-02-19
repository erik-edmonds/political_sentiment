#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 14:41:34 2020

@author: erikedmonds


Generates data for the mysql database using the polls data, 
credits: Nate Silver, https://github.com/fivethirtyeight/data/blob/master/polls/README.md
"""

from mysql.connector import connect

def populate(connection_string, local=False):
    """Populates the database, using the connection string."""
    database = connect(*connection_string)
    cursor = database.cursor()
    