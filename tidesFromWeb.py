import urllib2
import datetime

def get_current_day_forecast(number_of_10_minute_increments):
    URL = "https://www.tide-forecast.com/tides/Puerto-de-la-Luz-Gran-Canaria-Canary-Islands.js"
    tides_as_list = urllib2.urlopen(URL).read().translate(None,'[] ;').split('\n')[1:number_of_10_minute_increments+1]
    waves = [float(x.split(',')[3]) for x in tides_as_list]
    return waves

def get_now_index():
    now = datetime.datetime.now()
    now_index = int((now.hour*60 + now.minute)/10)
    return now_index
