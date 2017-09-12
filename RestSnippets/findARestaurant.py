from geocode import getGeocodeLocation
import json
import httplib2

import sys
import codecs

sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)

foursquare_client_id = "OBNNEB0ELVH2RJLJKBUGCYU25EJ2KKOCIYC0CYX25XZ1LDUG"
foursquare_client_secret = "5CMBNN3VHMYTYJJHNTF2CBI2DUJCUIEFPV3MSP4OWTMEOL4X"


def findARestaurant(mealType, location):


    # 1. Use getGeocodeLocation to get the latitude and longitude coordinates of the location string.
    (lat, lng) = getGeocodeLocation(location)

    # 2.  Use foursquare API to find a nearby restaurant with the latitude, longitude, and mealType strings.
    # HINT: format for url will be something like https://api.foursquare.com/v2/venues/search?client_id=CLIENT_ID&client_secret=CLIENT_SECRET&v=20130815&ll=40.7,-74&query=sushi
    url = "https://api.foursquare.com/v2/venues/search?client_id=%s&client_secret=%s&v=20170901&" \
                      "ll=%s,%s&radius=1600&query=%s&intent=browse" % (foursquare_client_id, foursquare_client_secret, lat, lng, mealType)
    h = httplib2.Http()
    response, content = h.request(url,"GET")

    # 3. Grab the first restaurant
    content = json.loads(content)
    if not content["response"]['venues']:
        return { 'name': "", 'address': "", 'image': ""}
    restaurant = content["response"]["venues"][0]
    name = restaurant['name']
    address = restaurant['location']['address']

    # 4. Get a  300x300 picture of the restaurant using the venue_id (you can change this by altering the 300x300 value in the URL or replacing it with 'orginal' to get the original picture
    url = "https://api.foursquare.com/v2/venues/%s/photos?client_id=%s&client_secret=%s&v=20170901" % \
          (restaurant['id'], foursquare_client_id, foursquare_client_secret)
    response, content = h.request(url,"GET")
    content = json.loads(content)
    # 5. Grab the first image
    image = content['response']['photos']['items'][0]['prefix'] + '300x300' + content['response']['photos']['items'][0]['suffix']
    if not image:
        image = "http://www.saborpos.com/wp-content/uploads/2017/01/Full-Service-300x300.jpg"
    # 6. If no image is available, insert default a image url
    # 7. Return a dictionary containing the restaurant name, address, and image url
    print(location)
    print("Restaurant Name: %s"% name)
    print("Restaurant Address: %s"% address)
    print("Image: %s\n"% image)

    return { 'name': name, 'address': address, 'image': image}

if __name__ == '__main__':
    r = []
    r.append(findARestaurant("Pizza", "Tokyo, Japan"))
    r.append(findARestaurant("Tacos", "Jakarta, Indonesia"))
    r.append(findARestaurant("Tapas", "Maputo, Mozambique"))
    r.append(findARestaurant("Falafel", "Cairo, Egypt"))
    r.append(findARestaurant("Spaghetti", "New Delhi, India"))
    r.append(findARestaurant("Cappuccino", "Geneva, Switzerland"))
    r.append(findARestaurant("Sushi", "Los Angeles, California"))
    r.append(findARestaurant("Steak", "La Paz, Bolivia"))
    r.append(findARestaurant("Gyros", "Sydney Australia"))

    print("done")