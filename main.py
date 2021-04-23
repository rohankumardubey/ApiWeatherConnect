#importing all the required modules
import requests, json
import matplotlib.pyplot as plt
from datetime import datetime,timezone
import time
import arrow
import csv
import os
import urllib3


#rmoving of the old existing files the extension of txt or csv or jpg during the old run 
def removeFiles(path):  
   if os.path.exists(f"{path}"):
      #list all the files in directory
      files_in_directory = os.listdir(f'{path}')
      #adding files list with csv,txt,jpg extension the list 
      filtered_files = [file for file in files_in_directory if file.endswith(".csv") or file.endswith(".txt") or file.endswith(".jpg")]
      
      #removing the files which are present in the list 
      for file in filtered_files:
         path_to_file = os.path.join(f'{path}', file)
         os.remove(path_to_file)
         

#function used to 
def Display_Data(CITY_NAME,API_KEY):
   
   #URL for displaying data
   Display_Data_URL = "https://api.openweathermap.org/data/2.5/weather?" + "q=" + CITY_NAME + "&appid=" + API_KEY

   # HTTP request
   request = requests.get(Display_Data_URL,verify =False)

   try:
      # checking the status code of the request if it is 200 then the status is good to proceed
      request.status_code == 200

      # fetching data in the json format
      DATA = request.json()


      # getting the main dictonary block
      ROOT = DATA['main']
      # getting temperature from json
      temperature = ROOT['temp'] 
      # getting the pressure from json
      pressure = ROOT['pressure']
      # getting the humidity from json
      humidity = ROOT['humidity'] 
      # SunsetSunRise report from json
      SunsetSunRise = DATA['sys']
      #sunrise report from json
      sunrise = SunsetSunRise['sunrise']
      #sunset report from json
      sunset = SunsetSunRise['sunset']

      ##printing the current day data for the banglore data
      print("#"*30)
      print(f"{CITY_NAME:|^30}")
      print("#"*30)
      print("      TODAYS CLIMATE")
      print("#"*30)
      print(f"Temperature: {temperature}")
      print(f"Humidity: {humidity}")
      print(f"SunRise: "+arrow.get(sunrise).to('local').format())
      print(f"SunSet: " +arrow.get(sunset).to('local').format())
      print("#"*30)

   except:
      #printing error message
      print("Issue in fetching the request")


#function used to write the header to the CSV file 
def WriteHeader(path):

    textfile = open(f"{path}\\DATA.txt", "w+")
    ##header input for the CSV file
    textfile.write('Index,Day,temperature, pressure,humidity,windspeed,Time,')
    textfile.close()

##function used to dump the data to the CSV file from the API for the past five days 
def DumpData(LAT,LON,API_KEY,TIME,DAY,INDEX):
   #banglore Longitude and Latitude 
   #latitude: 12.972442
   #longitude : 77.580643
   path=os.getcwd()
   #URL for dumping data
   DumpData_URL= "http://api.openweathermap.org/data/2.5/onecall/timemachine?"+"lat="+LAT +"&lon="+LON+"&dt="+str(TIME)+"&appid="+ API_KEY

   # HTTP request
   request = requests.get(DumpData_URL)

   try:
     # checking the status code of the request
      request.status_code == 200
    # getting data in the json format
      DATA = request.json()
      ROOT = DATA['hourly']

      temperature = ROOT[0]['temp']
      # getting the pressure
      pressure = ROOT[0]['pressure']
      # getting the humidity
      humidity = ROOT[0]['humidity']
       # getting the Wind Speed  
      WindSpeed = ROOT[0]['wind_speed']
      #getting the time in UTC format
      UTC_FORMAT_TIME = TIME

      #getting time in 24 hours format
      TIME=arrow.get(UTC_FORMAT_TIME).to('local').strftime("%H:%M:%S")


      ##empty list to fecth the data and store in it to write it to the CSV file 
      empty=[]
      empty.append(INDEX)
      empty.append(DAY)
      empty.append(temperature)
      empty.append(pressure)
      empty.append(humidity)
      empty.append(WindSpeed)
      empty.append(TIME)
      textfile = open(f"{path}\\DATA.txt", "a+")
      textfile.write("\n")
      for element in empty:
        textfile.write(str(element) + ",")
      textfile.close()

   except:
      #printing error message
      print("Issue in fetching the request")


##function used to clense any unwanted characters from the csv file which is loaded
def ClenseCsvData(path):
    file=open(f"{path}\\DATA.txt",'r')
    target=open(f"{path}\\DATA.csv",'w')
    for line in file:
        target.write(line[:-1].rstrip(',') + "\n")

    file.close()
    target.close()

   ##removing of the unwanted or the intermediate files which are used for conversion
    if os.path.exists(f"{path}"):

       files_in_directory = os.listdir(f'{path}')
       filtered_files = [file for file in files_in_directory if file.endswith(".txt")]
       for file in filtered_files:
          path_to_file = os.path.join(f'{path}', file)
          os.remove(path_to_file)
         

##used to fetch for five days data hitting the API 
def LoopData(hour,days):
   Hours_perday=int(24/hour)
   for row in range(int(Hours_perday*days),0,-1):
       FINAL_TIME=int(TIMESTAMP_UTC)-((3600*hour)*row)
       INDEX=(int(row)-(int(Hours_perday*days)+1))*-1
       DAYS=int(((INDEX/Hours_perday)-0.01)+1)
       DumpData('12.972442','77.580643',API_KEY,FINAL_TIME,DAYS,INDEX)   


#function used to plot the data for different parameters with respect to time 
def PlotGraph(XaxixLabel,YaxixLabel,X_ROW_NUM,Y_ROW_NUM):
   path=os.getcwd()  
   x = []
   y = []
   
   with open(f"{path}\\DATA.csv",'r') as csvfile:
      lines = csv.reader(csvfile, delimiter=',')
      for row in lines:
         x.append(row[X_ROW_NUM])
         y.append(row[Y_ROW_NUM])


   x_0=x[1:]
   y_0=y[1:]

   #pixel variables for the visibility
   w = 20
   h = 7
   d = 70
   plt.figure(figsize=(w, h), dpi=d)
   
   plt.plot(x_0, y_0, color = 'g', linestyle = 'dashed',marker = 'o',label = f"{YaxixLabel} DATA")
   plt.xticks(rotation = 25)
   plt.xlabel(f'{XaxixLabel}')
   plt.ylabel(f'{YaxixLabel}')
   plt.title(f'WEATHER {YaxixLabel} REPORT', fontsize = 20)
   plt.grid()
   plt.legend()
   plt.savefig(f"{YaxixLabel}_VS_{XaxixLabel}.jpg")
 







if __name__=="__main__":

##to disable the certificate warnings with the unsecure http
    urllib3.disable_warnings()

    path=os.getcwd()

##calling the removeFiles function to remove un wanted old files     
    removeFiles(path)

##mentioning the city name
    CITY_NAME = "Bangalore"

##API key 
    API_KEY = "d8f3bfa3151b10c698317bce1eb515d8"
 
 ##getting the UTC unix timestamp
    DT_UTC=datetime.utcnow()

##converting it into the local time format    
    TIMESTAMP_UTC = int(DT_UTC.replace(tzinfo=timezone.utc).timestamp())

##calling function to display current data 
    Display_Data(CITY_NAME,API_KEY)

##calling the WriteHeader to write header to the CSV file
    WriteHeader(path)

 #for 5 days and with 3 hours interval
    LoopData(3,5)

##calling ClenseCsvData function to remove the unwanted special characters from the csv file 
    ClenseCsvData(path)

## calling PlotGraph function to plot the graphs for Temperature
    PlotGraph('INDEX','TEMPERATURE',0,2)
## calling PlotGraph function to plot the graphs for Pressure    
    PlotGraph('INDEX','PRESSURE',0,3)
## calling PlotGraph function to plot the graphs for Humidity    
    PlotGraph('INDEX','HUMIDITY',0,4)
## calling PlotGraph function to plot the graphs for Wind Speed    
    PlotGraph('INDEX','WIND_SPEED',0,5)


