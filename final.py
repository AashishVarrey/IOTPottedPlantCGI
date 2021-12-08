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


temp = float(a[1]['field1']) 
humidity = float(a[2]['field2'])
light = float(a[3]['field3'])


#get data from html form 
data = cgi.FieldStorage()
try:
    s1 = float(data.getvalue('temp')) #value is typed in 
except:
    s1 = None
try:
    s2 = float(data.getvalue('humidity')) #value is typed in
except:
    s2 = None
try:
    s3 = float(data.getvalue('light')) #value is typed in 
except:
    s3 = None
try:
    s4 = data.getvalue('plantneeds') #value is submit
except:
    s4 = None
try:
    s5 = data.getvalue('water') #value is water
except:
    s5 = "notwater"
#write if plant needs to be manually watered to text file
with open('water.txt','w') as f:
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
background-color: darkseagreen
}
/*to center image*/
img {
display: block;
margin-top: auto;
margin-left: auto;
margin-right: auto;
width: 200px;
height: 80%
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
if isinstance(s1,float) and (temp > (s1+10) or temp < (s1-10)):
  print("""
  <div style = "width:50%;height:300px; float:left; background-color:darkseagreen; text-align:center">
  <h3> Temperature </h3>
  <h4 style ="color:red"> WARNING </h4>
  <iframe width="300" height="230" style="border: 10px solid DarkGreen;" src="https://thingspeak.com/channels/1587925/widgets/388191"></iframe>
  </div>  
  """)
else:
  print("""
  <div style = "width:50%;height:300px; float:left; background-color:darkseagreen; text-align:center">
  <h3> Temperature </h3>
  <!--<h4 style ="color:red"> WARNING </h4> -->
  <iframe width="300" height="230" style="border: 10px solid DarkGreen;" src="https://thingspeak.com/channels/1587925/widgets/388191"></iframe>
  </div> 
  """)

print("""
<div style = "width:50%; height:300px; float:right;background-color:darkseagreen; text-align:center">
<h3> A Healthy Plant is a Happy Plant! </h3> 
<img src="https://www.freepnglogos.com/uploads/plant-png/plant-png-capital-harvest-17.png" alt="plant png capital harvest">
</div> 
""")

#humidity range +- 10% you're fine, else warning
if isinstance(s2,float) and (humidity > (s2+10) or humidity < (s2-10)):
  print("""
  <div style = "width:50%;height:300px; float:left; background-color:darkseagreen; text-align:center;padding-top:50px">
  <h3> Humidity </h3>
  <h4 style ="color:red"> WARNING </h4>  
  <iframe width="300" height="230" style="border: 10px solid DarkGreen;" src="https://thingspeak.com/channels/1587925/widgets/388202"></iframe>  
  </div>
  """)
else:
  print("""
  <div style = "width:50%;height:300px; float:left; background-color:darkseagreen; text-align:center;padding-top:50px">
  <h3> Humidity </h3>
  <!--<h4 style ="color:red"> WARNING </h4>   -->
  <iframe width="300" height="230" style="border: 10px solid DarkGreen;" src="https://thingspeak.com/channels/1587925/widgets/388202"></iframe>  
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

#light range >= to requirements you're fine, else warning
if isinstance(s3,float) and (light < s3):
  print("""
  <div style = "width:50%;height:300px; float:left; background-color:darkseagreen; text-align:center;padding-top:50px">
  <h3> Light Recieved </h3>
  <h4 style ="color:red"> WARNING </h4>
  <iframe width="300" height="230" style="border: 10px solid DarkGreen;" src="https://thingspeak.com/channels/1587925/widgets/391046"></iframe>
  </div>
  """)
else:
  print("""
  <div style = "width:50%;height:300px; float:left; background-color:darkseagreen; text-align:center;padding-top:50px">
  <h3> Light Recieved </h3>
  <!--<h4 style ="color:red"> WARNING </h4>-->
  <iframe width="300" height="230" style="border: 10px solid DarkGreen;" src="https://thingspeak.com/channels/1587925/widgets/391046"></iframe>
  </div>
  """)  

print("""
<div style = "width:50%;height:300px;float:left; background-color:darkseagreen; text-align:center;padding-top:50px">
<h3> Press to Water Plant </h3>
<form action = "/cgi-bin/final.py" method="POST">
<input type="submit" name="water" value = "1" style="padding: 30px 45px; background-color:MidnightBlue; color:MidnightBlue">
</form>
</div>

<div style = "width:100%; float:left; background-color:darkseagreen; text-align:center;padding-top:70px">
<iframe width="450" height="260" style="border: 10px solid DarkGreen;" src="https://thingspeak.com/channels/1587925/charts/1?bgcolor=%23ffffff&color=%23d62020&dynamic=true&results=60&title=Temp+Over+Time&type=line&xaxis=Time&yaxis=%C2%B0Celsius"></iframe>
</div>

<div style = "width:100%; float:left; background-color:darkseagreen; text-align:center;padding-top:10px">
<iframe width="450" height="260" style="border: 10px solid DarkGreen;" src="https://thingspeak.com/channels/1587925/charts/2?bgcolor=%23ffffff&color=%23d62020&dynamic=true&results=60&title=Humidity+over+Time&type=line&xaxis=Time&yaxis=%25+Humidity"></iframe>
</div>

<div style = "width:100%; float:left; background-color:darkseagreen; text-align:center;padding-top:10px">
<iframe width="450" height="260" style="border: 10px solid DarkGreen;" src="https://thingspeak.com/channels/1587925/charts/3?bgcolor=%23ffffff&color=%23d62020&dynamic=true&results=60&title=Light+Over+Time&type=line&xaxis=Time&yaxis=Light+Received+in+Hours"></iframe>
</div>

</div>
</body>
</html>
""")