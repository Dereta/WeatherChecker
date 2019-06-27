#!/usr/bin/python 3.5
# -*- coding: iso-8859-15 -*-

import sys
import os
import json
import requests
from configparser import ConfigParser
from unidecode import unidecode

def exit_on_error(msg):
	print(msg)
	sys.exit()
	
# Try to read config file
try:
	config = ConfigParser()
	config.read("config.ini")
except:
	exit_on_error("Error while reading config file")
	
# Get API_KEY from config.ini
try:
	API_KEY = config.get("DEFAULT", "API_KEY").replace("\"", "")
	
except:
	exit_on_error("Error while reading API_KEY")
	
# Get API_STRING from config.ini
try:
	API_STRING = config.get("DEFAULT", "API_STRING").replace("\"", "")	
except:
	exit_on_error("Error while reading API_KEY")

# Get LOCATIONS from config.ini
try:
	LOCATIONS = json.loads(config.get("DEFAULT", "LOCATIONS"))
except:
	exit_on_error("Error while reading LOCATIONS")
	
# Get Data from OpenWeatherMap via API and STORE it in a CSV
for location in LOCATIONS:
	print(API_STRING.format(location[0], API_KEY))
	api_request = requests.get(API_STRING.format(location[0], API_KEY))
	if api_request.status_code == 200:
		# Creaete/Edit Datafile for Location
		try:
			if os.path.isfile("./weather_data_{}.csv".format(unidecode(location[1]))) == False:
				data_file = open("weather_data_{}.csv".format(unidecode(location[1])), "a")
				data_file.write("weather,description,temp,temp_min,temp_max,pressure,wind_speed,wind_deg,sunrise,sunset\n")
			else:
				data_file = open("weather_data_{}.csv".format(unidecode(location[1])), "a")
		except:
			exit_on_error("Error while creating/reading weather_data_{}.csv".format(unidecode(location[1])))
		# Write to Datafile
		data_weather = api_request.json()["weather"][0]
		data_main = api_request.json()["main"]
		data_wind = api_request.json()["wind"]
		data_sys = api_request.json()["sys"]
		data_file.write(unidecode(data_weather["main"]) + ",")
		data_file.write(unidecode(data_weather["description"]) + ",")
		data_file.write(str(data_main["temp"]) + ",")
		data_file.write(str(data_main["temp_min"]) + ",")
		data_file.write(str(data_main["temp_max"]) + ",")
		data_file.write(str(data_main["pressure"]) + ",")
		data_file.write(str(data_wind["speed"]) + ",")
		data_file.write(str(data_wind["deg"]) + ",")
		data_file.write(str(data_sys["sunrise"]) + ",")
		data_file.write(str(data_sys["sunset"]) + "\n")
	else:
		print("Error getting information for {}\nMessage: {}".format(unidecode(location[1]), api_request.json()["message"]))
