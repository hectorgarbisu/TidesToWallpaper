import urllib2
URL = "https://www.tide-forecast.com/tides/Puerto-de-la-Luz-Gran-Canaria-Canary-Islands.js"
content = urllib2.urlopen(URL).read()
print content