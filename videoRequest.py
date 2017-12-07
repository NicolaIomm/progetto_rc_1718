#ApiKey: AIzaSyCLnubplEKe0q1igtTkI_Sa-t2SHqWFWaY
#getVideos restitusce una lista contenente (nome, VideoId, statistiche) dei primi 5 risultati cercando "q" su youtube

import http.client
import ssl
import json

ssl._create_default_https_context = ssl._create_unverified_context

def getStats(videoId):
	parameters = 'part=statistics&id=' + videoId + '&key=AIzaSyCLnubplEKe0q1igtTkI_Sa-t2SHqWFWaY'
	conn = http.client.HTTPSConnection('www.googleapis.com')
	resource = '/youtube/v3/videos?' + parameters
	conn.request('GET', resource)
	r = conn.getresponse()
	d = json.loads(r.read().decode('utf-8'))	
	return d['items'][0]['statistics']

def getVideos(q):
	query = q.replace(' ', '+')
	parameters = 'part=snippet&type=video&q=' + query + '&key=AIzaSyCLnubplEKe0q1igtTkI_Sa-t2SHqWFWaY'
	conn = http.client.HTTPSConnection('www.googleapis.com')
	resource = '/youtube/v3/search?' + parameters
	conn.request('GET', resource)
	r = conn.getresponse()
	d = json.loads(r.read().decode('utf-8'))
	videos = []
	for e in d['items']:
		name = e['snippet']['title']
		id = e['id']['videoId']
		videos.append((name, id, getStats(id)))
	return videos

