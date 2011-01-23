import socket, BaseHTTPServer, urlparse, sys, geohash, redis, json

rds = redis.Redis('localhost')
sitekey = "sites";

class Handler(BaseHTTPServer.BaseHTTPRequestHandler):

    def fetch_id(self, id):
        key = "site:%s" % id
        site = rds.get(key)
        site = json.loads(site)

        return site

    def get_sites_near_latlon(self, lat, lon):
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

        sites = []

        if len(hashmatches) > 0:

            for hash, id in hashmatches.items():
                site = self.fetch_id(id)
                if site:
                    sites.append(site)

        return sites


    # Disable logging DNS lookups
    def address_string(self):
        return str(self.client_address[0])


    def do_GET(self):

        url = urlparse.urlparse(self.path)
        params = urlparse.parse_qs(url.query)

        if 'lat' not in params or 'lon' not in params:
            self.send_response(400)
            return
 
        self.send_response(200)
        self.send_header("Content-type", "application/x-javascript; charset=utf-8")
        self.end_headers()

        sites = []
        try:
            sites = self.get_sites_near_latlon(params['lat'][0], params['lon'][0])
        except:
            pass

        try:

            if 'jsonp' in params:
                self.wfile.write("%s(" % (params['jsonp'][0]))

            self.wfile.write(json.dumps(sites))

            if 'jsonp' in params:
                self.wfile.write(');')

            self.wfile.write("\n")
            self.wfile.flush()

        except socket.error, e:
            print "Client disconnected.\n"


PORT = 8910
httpd = BaseHTTPServer.HTTPServer(("", PORT), Handler)

print "Serving on %s" % PORT
httpd.serve_forever()
