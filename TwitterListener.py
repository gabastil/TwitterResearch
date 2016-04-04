#!/usr/bin/env Python
# -*- coding: utf-8 -*-
#
#	Name: 		Twitter.py
#	Author:		Glenn Abastillas
#	Version:	1.0.0
#	Date:		April 3, 2016
#
"""	connects to Twitter's API to collect data for linguistic research

Twitter utilizes the tweepy package to gain functionality allowing for
connecting to an manipulating Twitter data. Information required by the
API include the consumer key, secret consumer key, access token token and
the secret access token token. These can be found on your online Twitter 
account for developers.
"""

from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener

import json

CONSUMER_KEY 		= '5uM58Xdlu3H3yWNFQuqZAqFYg'
CONSUMER_KEY_SECRET = 'Q1QoWve8HgtMJVy5zybWn3LYc54aTMs9NbqfgVDg7ElvxzjpLv'
ACCESS_TOKEN 		= '2357328096-AREvcO4bvh8fj1QN6iZVSlHzjGIe1bbaGyamNFB'
ACCESS_TOKEN_SECRET = '7MAbtODd19EUuAVpjqyDfThkEhcHiFlaFo7zYhhidyG1g'

FIELDS_OF_INTEREST1 = ['text', 'id_str', 'source']
FIELDS_OF_INTEREST2 = ['user', 'entities']

SUBFIELDS_OF_INTEREST1 = ['id_str', 'name', 'followers_count_str']
SUBFIELDS_OF_INTEREST2 = ['hashtags', 'user_mentions']



OUTPUT_PATH	= "data/data.txt"

class TwitterListener(StreamListener):

	"""
		Important fields to use for research:
			json['text'] 	- String representation of tweet
			json['id']	 	- Unique ID of Tweet
			json['source']	- Source of Tweet (e.g., mobile, web)

			json['user']['id']				  - Unique ID of User
			json['user']['name']			  - User name
			json['user']['followers_count']	  - Count of followers for this user

			json['entities']['hashtags'] 	  - Hashtags in tweet
			json['entities']['user_mentions'] - Users mentioned in tweet
	"""

	def on_data(self, data):
		"""	Manage new data coming from the Twitter stream
			@param	data: new data coming from the Twitter stream
		"""

		#print type(jdata), jdata['text'].decode("UTF-8", "ignore"), jdata['contributors'], jdata['id'], jdata['source']
		#print u"{0}".format(jdata['text']).encode("utf-8"), "id:\t", jdata['id'], "source:\t", jdata['source']
		#print u"{0}".format(jdata['text']).encode("utf-8"), "id:\t", jdata['id'], "id str:\t", jdata['id_str'], "source:\t", jdata['source']
		#print "User:\t", jdata['user']['id'], "Name:\t", jdata['user']['name'], 
		#print "user:\t", jdata['user'].keys(), "entities:\t", jdata['entities']
		#print jdata.keys()
		#print u"\u266", "\u266"
		#saveFile = open('twitDB.csv','a')
		#saveFile.write(data)
		#saveFile.write('\n')
		#saveFile.close()

		with open(OUTPUT_PATH, 'r') as outputFile:
			jdata = json.loads(data)
			"""
			fieldsOfInterest1 = [jdata[element] for element in jdata.keys() if element in FIELDS_OF_INTEREST1]

			foi2  = [jdata[element] for element in jdata.keys() if element in FIELDS_OF_INTEREST2]
			foi2u = [foi2[element] for element in foi2[0] if element in SUBFIELDS_OF_INTEREST1]
			foi2e = [foi2[element] for element in foi2[1] if element in SUBFIELDS_OF_INTEREST2]
			fieldsOfInterest1 = u"\t".join(fieldsOfInterest1).encode("utf-8")
			fieldsOfInterest2 = u"\t".join(foi2u).encode("utf-8")
			fieldsOfInterest3 = u"\t".join(foi2e).encode("utf-8")

			outputContent = "\t".join([fieldsOfInterest1, fieldsOfInterest2, fieldsOfInterest3]).replace("\n", "__n__")
			"""
			text = jdata['text']
			tweet_id = jdata['id_str']
			source = jdata['source']

			user_id	= jdata['user']['id_str']
			user_name = jdata['user']['name']
			user_followers_count = jdata['user']['followers_count']

			entities_hashtags = [item['text'] for item in jdata['entities']['hashtags']]
			entities_hashtags = ", ".join(entities_hashtags)
			entities_user_mentions =  [item['id_str'] for item in jdata['entities']['user_mentions']]
			entities_user_mentions =  ", ".join(entities_user_mentions)

			outputContent = u"{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}".format(text, tweet_id, source, user_id, user_name, user_followers_count, entities_hashtags, entities_user_mentions).encode('utf-8')

			self.save(str("\n"+outputContent.replace("\n", "__n__")))

		return True

	def on_error(self, status):
		"""	Print error status to screen
			@param	status: error status from Twitter stream
		"""
		print status

	def save(self, data):
		"""	Save contents to file
			@param	data: contents to save
		"""
		outputFile = open(OUTPUT_PATH, 'a')
		outputFile.write(data)
		outputFile.close()

if __name__=="__main__":
	# Configure credentials required by Twitter's OAuthHandler
	auth = OAuthHandler(CONSUMER_KEY, CONSUMER_KEY_SECRET)
	auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

	twitterStream = Stream(auth, TwitterListener())
	test = twitterStream.filter(track=["ako"])