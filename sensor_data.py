import http.client as httplib
import urllib.request
import time
import random
import json
import threading

if __name__ == '__main__':
  sex=["Female", "Male", "Female", "Male"]
  age=[20,30,45,50]
  header1='&field1={}&field2={}&field8={}'.format(sex[0],age[0],"normal")
  header2='&field1={}&field2={}&field8={}'.format(sex[1],age[1],"normal")
  header3='&field1={}&field2={}&field8={}'.format(sex[2],age[2],"normal")
  header4='&field1={}&field2={}&field8={}'.format(sex[3],age[3],"normal")
  
  BaseURL3="https://api.thingspeak.com/update?api_key=BF4BHD99ZGN9HKSY"
  BaseURL1="https://api.thingspeak.com/update?api_key=6ZZYUJ8TF9D14S1I"
  BaseURL2="https://api.thingspeak.com/update?api_key=8ZLQ2HSYHOL7B6OR"
  BaseURL4="https://api.thingspeak.com/update?api_key=7PNU50AIBEZCXRRT"

  new_url=BaseURL1+header1
  new_url2=BaseURL2+header2
  new_url3=BaseURL3+header3
  new_url4=BaseURL4+header4
  conn = urllib.request.urlopen(new_url)
  conn = urllib.request.urlopen(new_url2)
  conn = urllib.request.urlopen(new_url3)
  conn = urllib.request.urlopen(new_url4)

  i=1
  while i < 20: 
    heart=[random.uniform(50,130) for _ in range(4)]
    oxy=[random.uniform(80,100) for _ in range(4)]
    temp=[random.uniform(95,104) for _ in range(4)]
    ecg=[random.uniform(95,104) for _ in range(4)]
    pers=[random.uniform(95,104) for _ in range(4)]
    header1='&field3={}&field4={}&field5={}&field6={}&field7={}'.format(temp[1],oxy[1],heart[1],ecg[1],pers[1])
    header2='&field3={}&field4={}&field5={}&field6={}&field7={}'.format(temp[0],oxy[0],heart[0],ecg[0],pers[0])
    header3='&field3={}&field4={}&field5={}&field6={}&field7={}'.format(temp[2],oxy[2],heart[2],ecg[2],pers[2])
    header4='&field3={}&field4={}&field5={}&field6={}&field7={}'.format(temp[3],oxy[3],heart[3],ecg[2],pers[2])

    new_url=BaseURL1+header1
    new_url2=BaseURL2+header2
    new_url3=BaseURL3+header3
    new_url4=BaseURL4+header4
    conn = urllib.request.urlopen(new_url)
    conn = urllib.request.urlopen(new_url2)
    conn = urllib.request.urlopen(new_url3)
    conn = urllib.request.urlopen(new_url4)
    conn.close

    i=i+1
   
 