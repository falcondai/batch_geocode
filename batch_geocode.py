#!/usr/bin/python

# batch_geocode.py
# A python module to geocode addresses in batch via Google Geocoding API.
#
# Author: Falcon Dai
# Date: 4/7/2013
# License: MIT License

import csv, json, time
import urllib2 as ul

# Google Geocode API endpoint format string
endpoint = 'http://maps.googleapis.com/maps/api/geocode/json?%s&sensor=false'

# quota on requests per IP per day
quota_request = 2500

# default constant backoff time in seconds
default_sleep = 1

# cache the requested addresses
geocode_cache = {}

def request_geocode(address):
	return ul.urlopen(endpoint % ('address='+ul.quote(address)))

def geocode(address, use_cache=True):
	if not geocode_cache.has_key(address):
		j = json.load(request_geocode(address))
		if use_cache and (j['status'] == 'OK' or j['status'] == 'ZERO_RESULTS'):
			geocode_cache[address] = j
		return j
	
	if use_cache:
		return geocode_cache[address]
	else:
		return json.load(request_geocode(address))
	
def gecode_generator(iterable, address_func=lambda x: x, sleep=default_sleep, max_retry=0, max_time=0, limit=quota_request, use_cache=True):
	for row in iterable:
		address = address_func(row)
		t0 = time.time()
		retry = 0
		j = geocode(address, use_cache)
		limit -= 1
		while j['status'] == 'OVER_QUERY_LIMIT' and (max_time == 0 or time.time() - t0 < max_time) and (max_retry == 0 or retry < max_retry) and limit > 0:
			j = geocode(address, use_cache)
			time.sleep(sleep)
			retry += 1
		if j['status'] == 'OVER_QUERY_LIMIT':
			break
		yield row, j

def batch_geocode(iterable, process_func, address_func=lambda x: x, sleep=default_sleep, max_retry=0, max_time=0, limit=quota_request, use_cache=True):
	for row, j in gecode_generator(iterable, address_func, sleep, max_retry, max_time, limit, use_cache):
		process_func(row, j)

def extract_latlong(j, i=0):
	# output the lat-long of the i-th result
	return {'latitude': j['results'][i]['geometry']['location']['lat'],
		'longitude': j['results'][i]['geometry']['location']['lng']}
		
def write_csv(csv_writer, row, j, extract_func=extract_latlong, process_func=None):
		if j['status'] == 'OK':
			row.update(extract_func(j))
		csv_writer.writerow(row)
		if process_func:
			process_func(row, j)

def batch_geocode_csv(iterable, csv_writer, process_func=None, address_func=lambda x: x['address'], extract_func=extract_latlong, sleep=default_sleep, max_retry=0, max_time=0, limit=quota_request, use_cache=True):
	batch_geocode(iterable, lambda r, j: write_csv(csv_writer, r, j, extract_func, process_func), address_func, sleep, max_retry, max_time, limit, use_cache)
		
if __name__ == '__main__':
	# example 0
	# geocoding a list of places
	places = ['North Pole', 'South Pole', 'Royal Observatory Greenwich']
	
	# implement a simple process function
	# print out response jsons' status and location
	def print_result(r, j):
		print r, j['status'], extract_latlong(j)
	
	batch_geocode(places, process_func=print_result)
	
	# example 1
	# geocoding data stored in CSV
	reader = csv.DictReader(open('sample.csv', 'r'))
	writer = csv.DictWriter(open('sample.geocoded.csv', 'wb'), fieldnames=reader.fieldnames+['latitude', 'longitude'])
	writer.writeheader()
	
	batch_geocode_csv(reader, writer, address_func=lambda x: x['address'], process_func=print_result)
	
	# example 2
	# geocoding data stored in CSV living at Google Drive
	from urllib2 import urlopen
	reader = csv.DictReader(urlopen('https://docs.google.com/spreadsheet/pub?key=0Ah73xeahAckPdHJrRktnZlAwUENfcHk5SFM1cXhoOHc&output=csv'))
	writer = csv.DictWriter(open('chicago_redlight_cameras.geocoded.csv', 'wb'), fieldnames=reader.fieldnames+['latitude', 'longitude'])
	writer.writeheader()
	
	batch_geocode_csv(reader, writer, address_func=lambda x: x['INTERSECTION']+', Chicago', process_func=print_result)