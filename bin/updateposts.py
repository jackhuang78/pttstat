#!/usr/bin/python
import os, sys
import json
import re
from datetime import datetime

from pymongo import MongoClient

client = MongoClient()
db = client.pttstat

dir = 'out/'+sys.argv[1]
reset = bool(sys.argv[2]) if len(sys.argv) > 2 else False

if reset:
	print 'reset db'
	for table in ['users', 'posts', 'messages']:
		db[table].delete_many({})

for filename in os.listdir(dir):
	with open('%s/%s' % (dir, filename)) as infile:
		print 'update', dir+'/'+filename
		posts = json.load(infile)
		for post in posts:

			try:
				user = post['author']
				i = user.rfind('(')
				j = user.rfind(')')
				userid = user[:i].strip()
				useralt = user[i+1:j].strip()
				url = post['url']
				title = post['title']
				ts = datetime.strptime(post['date'].strip(), '%a %b %d %H:%M:%S %Y')

				db.users.update({'_id':userid}, {'alt':useralt}, upsert=True)
				db.posts.update({'_id':url}, {'author':userid, 'title':title, 'ts':ts}, upsert=True)

				if 'messages' in post:
					for messageNo in post['messages']:
						try:
							message = post['messages'][messageNo]
							db.messages.update({'_id':'%s_%s' % (url, messageNo)}, {
								'tag':message['push_tag'],
								'user':message['push_userid'],
								'ts':datetime.strptime(message['push_datetime'].strip(), '%m/%d %H:%M').replace(year=ts.year)
							}, upsert=True)
						except ValueError:
							print 'Error processing message', url, messageNo
			except ValueError:
				print 'Error pricessing post', url

			





