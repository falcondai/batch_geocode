#!/usr/bin/python

# geocode_csv.py
#	A script to geocode the "address" column in a CSV and outputing the result
# into a new CSV with "latitude" and "longitude" columns
#
# Author: Falcon Dai
# Date: 4/7/2013
# License: MIT License


if __name__ == '__main__':
	import sys, csv, time
	from batch_geocode import batch_geocode_csv
	
	def print_result(r, j):
		print r['address'], j['status']
	
	if len(sys.argv) < 2:
		print 'Usage: %s <in-csv-filename> [<out-csv-filename>]' % sys.argv[0]
		exit(1)
	
	# output csv file name
	if sys.argv[1].endswith('.csv'):
		out_cn = sys.argv[1].replace('.csv', '.geocoded.csv')
	else:
		out_cn = sys.argv[1]+'.geocoded'
	if len(sys.argv) > 2:
		out_cn = sys.argv[2]
	
	t0 = time.time()
	
	with open(sys.argv[1], 'r') as ic:
		with open(out_cn, 'wb') as oc:
			r = csv.DictReader(ic)
			w = csv.DictWriter(oc, r.fieldnames+['latitude', 'longitude'])
			w.writeheader()
			batch_geocode_csv(r, w, process_func=print_result)
	
	l, dt = r.line_num - 1, time.time() - t0
	print 'Done geocoding %d addresses in %.2fs, average %.2f geocode/s' % (l, dt, l/dt)
	print 'Saved to file: %s' % out_cn