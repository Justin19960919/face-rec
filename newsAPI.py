# https://gnewsapi.net/settings#/api

# import modules
import json
import requests
import os

# load api key
from dotenv import load_dotenv
load_dotenv()


API_TOKEN = os.getenv("GNEWS")
QUERY = "kpop"
COUNTRY = "kr"
LANGUAGE = "en"


# set a time everyday to fetch the new news

def getNews():
	# save fetched news everyday
	request_url = f"https://gnewsapi.net/api/search?q={QUERY}&country={COUNTRY}&language={LANGUAGE}&api_token={API_TOKEN}"
	response = requests.get(request_url)
	data = response.text
	file = open("news.txt","w")
	file.write(data)
	file.close()


def readNews():
	# returns the articles in a list, with date cleaned
	readFile = open("news.txt","r")
	file = readFile.read()
	articles = json.loads(file)['articles']

	for article in articles:
		datetime = article['published_datetime']
		new_datetime = datetime.split("T")[0]
		article['published_datetime'] = new_datetime

	return articles


def main():
	getNews()


if __name__ == "__main__":
	main()






