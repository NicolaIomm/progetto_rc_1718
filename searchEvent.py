#search event ritorna una lista di dizionari, dove ogni dizionario rappresenta un evento associato
#alla string q passata. 
#
#Ogni dizionario ha ha le seguenti chiavi:
#
#title  -> titolo dell'evento
#venue  -> sede (es: palalottomatica, ippodromo delle capannelle...)
#city   -> città
#price  -> prezzo
#start_time -> data ed ora di inizio

import http.client
import ssl
import json
import xml.etree.ElementTree

ssl._create_default_https_context = ssl._create_unverified_context

def searchEvent(q):
	query = q.replace(' ', '+')
	apikey = '7FZjXFZ4ZRP7FmtV'
	parameters = '&date=Future' +  '&keywords=' + query + '&app_key=' + apikey
	conn = http.client.HTTPConnection('api.eventful.com')
	resource = '/json/events/search?' + parameters
	conn.request('GET', resource)
	r = conn.getresponse()
	d = json.loads(r.read().decode())
	events = []
	for e in d['events']['event']:
		info = getInfoEvent(e['id'])
		events.append(info)
	return events

def getInfoEvent(idEvent):
	apikey = '7FZjXFZ4ZRP7FmtV'
	parameters = '&id=' + idEvent + '&app_key=' + apikey
	conn = http.client.HTTPConnection('api.eventful.com')
	resource = '/json/events/get?' + parameters
	conn.request('GET', resource)
	r = conn.getresponse()
	d = json.loads(r.read().decode())
	ris = {}
	ris['title'] = d['title']
	ris['city'] = d['city']
	ris['venue'] = d['venue_name']
	ris['price'] = d['price']
	ris['start_time'] = d['start_time']
	return ris


#l = searchEvent(input('Cerca concerto: '))
#for e in l:
#	print(e)
#	print('\n')
