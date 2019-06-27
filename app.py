#!/usr/bin/python 3.5
# -*- coding: iso-8859-15 -*-

import sys
import os
import json
import requests
import datetime
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
	#print(API_STRING.format(location[0], API_KEY))
	api_request = requests.get(API_STRING.format(location[0], API_KEY))
	if api_request.status_code == 200:
		# Creaete/Edit Datafile for Location
		try:
			if os.path.isfile("./weather_data_{}.csv".format(unidecode(location[1]))) == False:
				data_file = open("weather_data_{}.csv".format(unidecode(location[1])), "a")
				data_file.write(API_STRING.format(location[0], API_KEY) + "\n")
				data_file.write("timestamp,weather,description,temp,temp_min,temp_max,pressure,wind_speed,wind_deg,sunrise,sunset\n")
			else:
				data_file = open("weather_data_{}.csv".format(unidecode(location[1])), "a")
		except:
			exit_on_error("Error while creating/reading weather_data_{}.csv".format(unidecode(location[1])))
		# Write to Datafile
		now = datetime.datetime.now()
		data_file.write(str(now.strftime("%Y-%m-%d %H:%M")) + ",")
		if api_request.json()["weather"][0] != None:
			# Get weather JSON
			try:
				data_weather = api_request.json()["weather"][0]
			except:
				data_file.write("ERROR WEATHER JSON,")
				
			# WEATHER main
			try:
				data_file.write(unidecode(data_weather["main"]) + ",")
			except:
				data_file.write("ERROR WEATHER main,")
				
			# WEATHER description
			try:
				data_file.write(unidecode(data_weather["description"]) + ",")
			except:
				data_file.write("ERROR WEATHER description,")
		if api_request.json()["main"] != None:
			# Get main JSON
			try:
				data_main = api_request.json()["main"]
			except:
				ddata_file.write("ERROR MAIN JSON,")
			
			# MAIN temp
			try:
				data_file.write(str(data_main["temp"]) + ",")
			except:
				data_file.write("ERROR MAIN temp,")
				
			# MAIN temp_min
			try:
				data_file.write(str(data_main["temp_min"]) + ",")
			except:
				data_file.write("ERROR MAIN temp_min,")
				
			# MAIN temp_max
			try:
				data_file.write(str(data_main["temp_max"]) + ",")
			except:
				data_file.write("ERROR MAIN temp_max,")
				
			# MAIN pressure
			try:
				data_file.write(str(data_main["pressure"]) + ",")
			except:
				data_file.write("ERROR MAIN pressure,")
				
		if api_request.json()["wind"] != None:
			# Get wind JSON
			try:
				data_wind = api_request.json()["wind"]
			except:
				ddata_file.write("ERROR WIND JSON,")
				
			# WIND speed
			try:
				data_file.write(str(data_wind["speed"]) + ",")
			except:
				data_file.write("ERROR WIND speed,")
				
			# WIND deg
			try:
				data_file.write(str(data_wind["deg"]) + ",")
			except:
				data_file.write("ERROR WIND deg,")
				
		if api_request.json()["sys"] != None:
			# Get sys JSON
			try:
				data_sys = api_request.json()["sys"]
			except:
				data_file.write("ERROR SYS JSON,")
				
			# SYS sunrise
			try:
				data_file.write(str(data_sys["sunrise"]) + ",")
			except:
				data_file.write("ERROR SYS sunrise,")
				
			# SYS sunset
			try:
				data_file.write(str(data_sys["sunset"]) + "\n")
			except:
				data_file.write("ERROR SYS sunset,")
	else:
		print("Error getting information for {}\nMessage: {}".format(unidecode(location[1]), api_request.json()["message"]))
