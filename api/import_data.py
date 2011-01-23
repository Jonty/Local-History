#!/usr/bin/env python
import sys, geohash, redis, json
from lxml import etree

import eventlet
from eventlet.green import urllib2  

rds = redis.Redis('localhost')

sitekey = "sites";

def fetch_site_id(id):

    key = "site:%s" % id
    site = rds.get(key)

    if site:
        site = json.loads(site)

    if site == None:
        url = "http://www.museumoflondon.org.uk/laarcWS/v1/rest/?op=GetSite&search_type=bykey&terms=%d" % id

        code = 0
        tries = 0
        response = None
        root = None

        while code != 200:
            response = urllib2.urlopen(url)
            code = response.code
            root = etree.XML(response.read())

            if root.find(".//ErrorCode") is not None:
                code = int(root.find(".//ErrorCode").text.strip())

            if code != 200:
                tries += 1
                print "Retrying %s, try %s" % (id, tries)
                eventlet.sleep(1)

                if tries > 20:
                    break


        if root.find(".//Site") is not None:

            (latitude, longitude) = (float(root.find(".//Latitude").text), float(root.find(".//Longitude").text))

            site = {
                'id':           root.find(".//Site").get('id'),
                'year':         root.find(".//SiteYear").text,
                'name':         root.find(".//SiteName").text,
                'description':  root.find(".//Description").text.strip(),
                'article':      root.find(".//GazetteerArticle").text.strip(),
                'period':       [l.strip() for l in root.find(".//Period").text.split(',')],
                'latitude':     latitude,
                'longitude':    longitude,
                'location':     root.find(".//Location").text,
                'geohash':      geohash.encode(latitude, longitude),
            }
            
            rds.set(key, json.dumps(site))
            rds.zadd('sites', site['geohash'], int(site['id']))

        else:
            pass
            rds.set(key, '')

    return site



if __name__ == '__main__':

    urls = []

    for id in range(301, 5643):
        urls.append(id)

    pool = eventlet.GreenPool(1)
    for site in pool.imap(fetch_site_id, urls):
        if site:
            print "%s: %s" % (site['geohash'], site['id'])
