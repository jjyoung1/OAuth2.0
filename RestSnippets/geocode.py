import json
import httplib2


def getGeocodeLocation(inputString):
    google_api_key = 'AIzaSyDrQ143pmSUD4d8-IXhogfrIOiTo1UGgCE'
    locationString = inputString.replace(" ", "+")
    url = ("https://maps.googleapis.com/maps/api/geocode/"
           "json?address=%s&key=%s"%(locationString, google_api_key))
    h = httplib2.Http()
    response, content = h.request(url,'GET')
    result = json.loads(content)
    # print("response header: %s \n \n" % response)
    latitude = result['results'][0]['geometry']['location']['lat']
    longitude = result['results'][0]['geometry']['location']['lng']
    return (latitude, longitude)

if __name__ == "__main__":
    lat, lng = getGeocodeLocation("Dallas, TX")

    print("Dallas: %s latitude, %s longitude"%(lat,lng))
    