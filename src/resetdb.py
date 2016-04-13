#!/usr/bin/python
import os, sys
from pymongo import MongoClient

os.system('rm -rf out/*')

client = MongoClient()
db = client.pttstat

for table in ['authors', 'posts', 'messages']:
	db[table].delete_many({})