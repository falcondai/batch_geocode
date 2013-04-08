batch_geocode
=============

A python module to geocode addresses in batch via [Google Geocoding API][1], i.e. it turns addresses into latitude-longitude coordinates.

What it is
=======

The library contains a few easily extendable functions to make Google Geocoding API more convenient to use. The library handles the frequent, interrupting `OVER_QUERY_LIMIT` response elegantly for you. The implementation uses generator to minimize memory use and enables to geocode larger-than-memory files or streams. Functions takes advantage of default values and extensive function arguments to keep simple tasks simple while remaining high flexibility.

Uses
====

The library contains a convenient script to geocode a CSV.

``` bash
$ geocode_csv.py <in-csv-filename> [<out-csv-filename>]
```

Examples
========
``` python
# geocoding a list of places
places = ['North Pole', 'South Pole', 'Royal Observatory Greenwich']
	
# implement a simple process function
# print out response jsons
def print_result(r, j):
  print r['address'], j
	
batch_geocode(places, process_func=print_result)
```

``` python
# geocoding data stored in CSV
reader = csv.DictReader(open('sample.csv', 'r'))
writer = csv.DictWriter(open('geocoded-sample.csv', 'w'), fieldnames=reader.fieldnames+['latitude', 'longitude'])
writer.writeheader()
	
batch_geocode_csv(reader, process_func=lambda r, j: write_csv(writer, r, j), address_func=lambda x: x['address'])
```

Restrictions
=========

The library relies on Google Geocoding API to geocode: this dependency _might_ change in the future. But while this is the case, users should observe restrictions on their use according to [Google Geocoding API's documentation][1]. “[T]he Geocoding API may only be used in conjunction with a Google map; geocoding results without displaying them on a map is prohibited. For complete details on allowed usage, consult the Maps API Terms of Service License Restrictions.”

[1]: https://developers.google.com/maps/documentation/geocoding
