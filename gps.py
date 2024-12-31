# Importing Necessary Modules
# pip install requests
# pip install selenium
# pip install folium
# pip install datetime

import requests
from selenium import webdriver
import folium
import datetime
import time

# this method will return us our actual coordinates using our ip address
def locationCoordinates():
    try: 
        # get ip address from ipinfo.io website
        response = requests.get('https://ipinfo.io')
        data = response.json() # get the data
        # get location, latitude, longitude, city and state information from IP Address
        loc = data['loc'].split(',')
        lat, long = float(loc[0]), float(loc[1])
        city = data.get('city', 'Unknown')
        state = data.get('region', 'Unknown')
        return lat, long, city, state # return found data
    except: # if any error happens
        # Displaying ther error message
        print("Internet Not avialable")
        # closing the program
        exit()
        return False


# this method will fetch our coordinates and create a html file of the map
def gps_locator():

    # create a map
    obj = folium.Map(location=[0, 0], zoom_start=2)

    try:
        # print current location in console
        lat, long, city, state = locationCoordinates()
        print("You Are in {},{}".format(city, state))
        print("Your latitude = {} and longitude = {}".format(lat, long))
        # put marker of current location on the map
        folium.Marker([lat, long], popup='Current Location').add_to(obj)

        # save html
        fileName = "D:/Projects/GPS-Tracker/" + \
            str(datetime.date.today()) + ".html"

        obj.save(fileName)

        return fileName

    except:
        return False


# Main method
if __name__ == "__main__":

    print("---------------GPS Using Python---------------\n")

    # function Calling
    page = gps_locator()
    page = gps_locator()
    print(f"Generated page: {page}")
    print("\nOpening File.............")
    dr = webdriver.Chrome()
    dr.get(page)
    print("\nPress Enter to close the browser...")
    input()
    dr.quit()
    print("\nBrowser Closed..............")