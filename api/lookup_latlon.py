#!/usr/bin/env python
import sys, geohash, redis, json

rds = redis.Redis('localhost')

sitekey = "sites";

def fetch_id(id):

    key = "site:%s" % id
    site = rds.get(key)
    site = json.loads(site)

    return site



if __name__ == '__main__':

    lat, lon = sys.argv[1], sys.argv[2]
    ghash = geohash.encode(float(lat), float(lon))

    hashes = geohash.neighbors(ghash)
    hashes.append(ghash)

    sites = rds.zrange(sitekey, 0, -1, withscores = True)

    hashmatches = {}

    for chars in range(6,3,-1):
        for sitehash, id in sites:
            for currenthash in hashes:

                if currenthash[0:chars] == sitehash[0:chars]:
                    hashmatches[sitehash] = int(id)

        if len(hashmatches) > 0:
            break


    if len(hashmatches) > 0:
        for hash, id in hashmatches.items():

            site = fetch_id(id)
            for (key, value) in site.items():
                print "%s: %s" % (key, value)

            print
