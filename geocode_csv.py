#!/usr/bin/python

if __name__ == '__main__':
	import sys, csv, time
	from batch_geocode import batch_geocode_csv
	
	def print_result(r, j):
		print r['address'], j['status']
	
	if len(sys.argv) < 2:
		print 'Usage: %s <in-csv-filename> [<out-csv-filename>]' % sys.argv[0]
		exit(1)
	
	out_cn = 'geocoded-'+sys.argv[1]
	if len(sys.argv) > 2:
		out_cn = sys.argv[2]
	
	t0 = time.time()
	
	with open(sys.argv[1], 'r') as ic:
		with open(out_cn, 'w') as oc:
			r = csv.DictReader(ic)
			w = csv.DictWriter(oc, r.fieldnames+['latitude', 'longitude'])
			w.writeheader()
			batch_geocode_csv(r, w, process_func=print_result)
	
	l, dt = r.line_num - 1, time.time() - t0
	print 'Done geocoding %d addresses in %.2fs, average %.2f geocode/s' % (l, dt, l/dt)