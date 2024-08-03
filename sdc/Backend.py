import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time
from .models import Order

def Distance_scapper(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode (without opening a window)
    driver = webdriver.Chrome() #options=options
    
    try:
        # Open the URL
        url = driver.get(url)
        
        # Wait for the page to load
        print(url)
        get_location = driver.find_element(By.XPATH,"/html/body/div[2]/div[3]/div[8]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[2]/div[1]/h1/span")
        match = re.match(r"(.+?)\s*\(([^)]+)\)", get_location.text)
        if match:
            return match.group(1).strip(), match.group(2).strip()
        else:
            return get_location.text, ""
    
    finally:
        # Close the driver
        driver.quit()

def extract_coordinates(google_maps_url):
    pattern = r'@(-?\d+\.\d+),(-?\d+\.\d+)'
    match = re.search(pattern, google_maps_url)
    
    if match:
        latitude = match.group(1)
        longitude = match.group(2)
        return (latitude, longitude)
    else:
        return None

def Direction_Gen(current_lat, current_lng, dest_lat, dest_lng):
    #https://www.google.com/maps/embed/v1/directions?&origin=23.07553126947766,76.85918941881717&destination=23.2000817,77.0841725&travelmode=driving
    base_url = "https://www.google.com/maps/embed/v1/directions"
    origin = f"{current_lat},{current_lng}"
    destination = f"{dest_lat},{dest_lng}"
    travel_mode = "driving"  # You can change this to "walking", "bicycling", or "transit"

    direction_url = f"{base_url}&origin={origin}&destination={destination}&key=AIzaSyBFw0Qbyq9zTFTd-tUY6dZWTgaQzuU17R8"
    return direction_url


def generate_map_link(latitude, longitude):
    base_url = "https://www.google.com/maps?q="
    map_link = f"{base_url}{latitude},{longitude}"
    return map_link


def extract_lat_long(url):
    match = re.search(r'q=(-?\d+\.\d+),(-?\d+\.\d+)', url)
    
    if match:
        latitude = float(match.group(1))
        longitude = float(match.group(2))
        return latitude, longitude
    else:
        raise ValueError("Invalid Google Maps URL")


def getDirection_(current_lat, current_long, destination_lat, destination_long):
    base_url = "https://www.google.com/maps/dir/"
    link = f"{base_url}{current_lat},{current_long}/{destination_lat},{destination_long}/am=t"
    return link

def numeric_distance(distance_str):
    match = re.search(r"(\d+(\.\d+)?)", distance_str)
    return float(match.group(1)) if match else 0

def Distance(orderno,employee):
    orders = Order.objects.filter(Assigned_to__username = employee).filter(order_no=orderno).first()
    route1 = orders.route1
    route2 = orders.route2
    r1_duration, r1_distance = Distance_scapper(route1)
    r2_duration, r2_distance = Distance_scapper(route2)
    print("Route 1 ",r1_distance,r1_duration)
    print("Route 2 ",r2_distance,r2_duration)
    
    distance = round( numeric_distance(r1_distance) + numeric_distance(r2_distance),1)
    
    orderss = Order.objects.filter(Assigned_to__username = employee).filter(order_no=orderno).first()
    print(orderss)
    print(orderss.duration1,orderss.distance2,orderss.duration1,orders.duration2)
    orderss.distance1 = r1_distance
    orderss.distance2 = r2_distance
    orderss.duration1 = r1_duration
    orderss.duration2 = r2_duration
    print("DISSSSSSSSSTANCE ----> ",distance)

    orderss.distance = f"{distance} km"
    orderss.save()
    
