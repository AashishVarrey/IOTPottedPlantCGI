#!/usr/bin/python37all

#necessary modules
import json
import requests
import cgi
import cgitb
cgitb.enable() 

#dict which will store data from thingspeak
a = {}
url= {1:"https://api.thingspeak.com/channels/1587925/fields/1/last.json",
      2:"https://api.thingspeak.com/channels/1587925/fields/2/last.json",
      3:"https://api.thingspeak.com/channels/1587925/fields/3/last.json"}

#pull data from thingspeak for each field 
for key in url:
  request = requests.get(url[key]).text
  a[key] = json.loads(request)

temp = int(a[1]['field1'])
humidity = int(a[2]['field2'])
light = int(a[3]['field3'])

#get data from html form 
data = cgi.FieldStorage()
s1 = data.getvalue('temp') #value is typed in 
s2 = data.getvalue('humidity') #value is typed in 
s3 = data.getvalue('light') #value is typed in 
s4 = data.getvalue('plantneeds') #value is submit
#s5 = data.getvalue('refresh') #value is refresh
s5 = data.getvalue('water') #value is water

#write if plant needs to be manually watered to text file
with open('IOTFinal','w') as f:
  json.dump(s5,f)

#generate html webpage
print('Content-type: text/html\n\n')
print("""
<html>
<head>
<title> IOT Potted Plant Interface </title>
<style> 
/*adjust body font, color, and overall background here */
body {
font-family:Arial;
color:white;
background-color:darkseagreen
}
/*to center image*/
img {
display: block;
margin-top: auto;
margin-left: auto;
margin-right: auto;
width: 35%;
height: 70%
}
h3 {
text-shadow: -1px 0 black, 0 1px black, 1px 0 black, 0 -1px black;
}
</style>
</head>
<body>
<div style = "width:100%">
<div style = "width:100%; text-align:center;text-shadow: 2px 2px 4px #000000;">
<h1> Real Time Plant Monitoring System </h1>
</div> 
""")

#temp range +- 10 degrees celcius you're fine, else warning
if isinstance(s1,int) and (temp > (s1+10) or temp < (s1-10)):
  print("""
  <div style = "width:50%;height:300px; float:left; background-color:darkseagreen; text-align:center">
  <h3> Temperature </h3>
  <h4 style ="color:red"> WARNING </h4>
  <!-- Add following line in cgi code if necessary
  <p style="color:red"> WARNING </p> -->
  <iframe height="230" style="border: 10px solid DarkGreen;width:75%" src="https://thingspeak.com/channels/1587925/widgets/388191"></iframe>
  </div> 
  """)
else:
  print("""
  <div style = "width:50%;height:300px; float:left; background-color:darkseagreen; text-align:center">
  <h3> Temperature </h3>
  <!-- Add following line in cgi code if necessary
  <p style="color:red"> WARNING </p> -->
  <iframe height="230" style="border: 10px solid DarkGreen;width:75%" src="https://thingspeak.com/channels/1587925/widgets/388191"></iframe>
  </div> 
  """)

print("""
<div style = "width:50%; height:300px; float:right;background-color:darkseagreen; text-align:center">
<h3> A Healthy Plant is a Happy Plant! </h3> 
<img src="https://www.freepnglogos.com/uploads/plant-png/plant-png-capital-harvest-17.png" alt="plant png capital harvest">
</div> 
""")

#humidity range +- 20% you're fine, else warning
if isinstance(s2,int) and (humidity > (s2+20) or humidity < (s2-20)):
  print("""
  <div style = "width:50%;height:300px; float:left; background-color:darkseagreen; text-align:center;padding-top:50px">
  <h3> Humidity </h3>
  <h4 style ="color:red"> WARNING </h4>      
  <!-- Add following line in cgi code if necessary 
  <p style="color:red"> WARNING </p> -->
  <iframe height="230" style="border: 10px solid DarkGreen;width:75%" src="https://thingspeak.com/channels/1587925/widgets/388202"></iframe>
  </div>
  """)
else:
  print("""
  <div style = "width:50%;height:300px; float:left; background-color:darkseagreen; text-align:center;padding-top:50px">
  <h3> Humidity </h3>      
  <!-- Add following line in cgi code if necessary 
  <p style="color:red"> WARNING </p> -->
  <iframe height="230" style="border: 10px solid DarkGreen;width:75%" src="https://thingspeak.com/channels/1587925/widgets/388202"></iframe>
  </div>
  """)

print("""
<div style = "width:50%; height:300px; float:right;background-color:darkseagreen; text-align:center;padding-top:50px">
<h3> Enter Your Plants Needs </h3>
<form action = "/cgi-bin/final.py" method="POST">
Ideal Temperature in Degrees Celcius: <br>
<input type="text" name = "temp"> <br>
Ideal Humidity in Percent Humidity: <br>
<input type="text" name="humidity"> <br>
Number of Hours of Sunlight Per Day: <br>
<input type="text" name="light"> <br> 
<input type="submit" name="plantneeds" value="submit">
</form>
</div>
""")

#humidity range +-2 hours ou're fine, else warning
if isinstance(s3,int) and (humidity > (s3+2) or humidity < (s3-2)):
  print("""
  <div style = "width:50%;height:300px; float:left; background-color:darkseagreen; text-align:center;padding-top:50px">
  <h3> Light Recieved </h3>
  <h4 style ="color:red"> WARNING </h4> 
  <!-- Add following line in cgi code if necessary 
  <p style="color:red"> WARNING </p> -->
  <iframe height="230" style="border:10px solid DarkGreen;width:75%" src="https://thingspeak.com/channels/1587925/widgets/391046"></iframe>
  </div>
  """)
else:
  print("""
  <div style = "width:50%;height:300px; float:left; background-color:darkseagreen; text-align:center;padding-top:50px">
  <h3> Light Recieved </h3>
  <!-- Add following line in cgi code if necessary 
  <p style="color:red"> WARNING </p> -->
  <iframe height="230" style="border:10px solid DarkGreen;width:75%" src="https://thingspeak.com/channels/1587925/widgets/391046"></iframe>
  </div>
  """)  

print("""
<div style = "width:50%;height:300px;float:left; background-color:darkseagreen; text-align:center;padding-top:50px">
<h3> Press to Water Plant </h3>
<form action = "/cgi-bin/final.py" method="POST">
<input type="image"
src="https://www.freepnglogos.com/uploads/water-drop-png/water-drop-png-image-water-droplet-pin-club-penguin-wiki-fandom-21.png"alt="submit" name="water" value="water" style="height:150px;width:75px;transform: translateY(30%)">
</form>
</div>

<div style = "width:100%; float:left; background-color:darkseagreen; text-align:center;padding-top:70px">
<iframe height="260" style="border: 10px solid DarkGreen;;width:50%" src="https://thingspeak.com/channels/1587925/charts/1?bgcolor=%23ffffff&color=%23d62020&dynamic=true&results=60&title=Temp+Over+Time&type=line"></iframe>
</div>

<div style = "width:100%; float:left; background-color:darkseagreen; text-align:center;padding-top:10px">
<iframe height="260" style="border: 10px solid DarkGreen; width:50%"src="https://thingspeak.com/channels/1587925/charts/2?bgcolor=%23ffffff&color=%23d62020&dynamic=true&results=60&title=Humidity+over+Time&type=line"></iframe>
</div>

<div style = "width:100%; float:left; background-color:darkseagreen; text-align:center;padding-top:10px">
<iframe height="260" style="border: 1px solid #cccccc;width:50%;border: 10px solid DarkGreen;" src="https://thingspeak.com/channels/1587925/charts/3?bgcolor=%23ffffff&color=%23d62020&dynamic=true&results=60&title=Light+Over+Time&type=line"></iframe>
</div>

</div>
</body>
</html>
""")