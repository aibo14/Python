from urllib.request import urlretrieve
import os
import re
import collections

months = {
  "January": 0,
  "February": 0,
  "March": 0,
  "April": 0,
  "May": 0,
  "June": 0,
  "July": 0,
  "August": 0,
  "September": 0,
  "October": 0,
  "November": 0,
  "December": 0
}

janlogs=open("january.txt", "a+"); feblogs=open("february.txt", "a+"); marlogs=open("march.txt", "a+");
aprlogs=open("april.txt", "a+"); maylogs=open("may.txt", "a+"); junlogs=open("june.txt", "a+");
jullogs=open("july.txt", "a+"); auglogs=open("august.txt", "a+"); seplogs=open("september.txt", "a+");
octlogs=open("october.txt", "a+"); novlogs=open("november.txt", "a+"); declogs=open("december.txt", "a+");   

i=0

countRedirects = 0
countErrors = 0

data = 'https://s3.amazonaws.com/tcmg476/http_access_log'
savelog = open('http_access_log', "a+")

def file_len(savelog):
  with open (savelog) as f:
    for i, l in enumerate (f):
      pass
  return i + 1

def fileCount():
  filelog = []
  leastcommon = []
  with open(savelog) as logs:
	  for line in logs:
		  try:
			  filelog.append(line[line.index("GET")+4:line.index("HTTP")])	
		  except:
			  pass
  counter = collections.Counter(filelog)
  for count in counter.most_common(1):
	  print("Top request: {} with {} requests.".format(str(count[0]), str(count[1])))
  for count in counter.most_common():
	  if str(count[1]) == '1':
	    leastcommon.append(count[0])
	
  if leastcommon:																	
	  response = input("There are {} file(s) with low request frequency, show all? (y/n)".format(len(leastcommon)))
	  if response == 'y':
		  for file in leastcommon:
			  print(file)
  if not os.path.isfile(savelog):
    urlretrieve(data, savelog)

regex = r'(.*?) - (.*) \[(.*?)\] \"(.*?) (.*?)\"? (.+?) (.+) (.+)'

lines = open(savelog, 'r').readlines()

for line in lines:
  match = re.match(regex, line)
  if not match:
    continue

  original = match.group(0)
  timestamp = match.group(3)
  month = timestamp[3:6]
  months[month] += 1
  status = match.group(7)
    
  if (status[0] == "3"):
    countRedirects += 1
  elif (status[0] == "4"):
    countErrors += 1

  if (month == "January"): 
    janlogs.write(line)
  elif (month == "February"): 
    feblogs.write(line)
  elif (month == "March"): 
    marlogs.write(line)
  elif (month == "April"): 
    aprlogs.write(line)
  elif (month == "May"): 
    maylogs.write(line)
  elif (month == "June"): 
    junlogs.write(line)
  elif (month == "July"): 
    jullogs.write(line)
  elif (month == "August"): 
    auglogs.write(line)
  elif (month == "September"): 
    seplogs.write(line)
  elif (month == "October"): 
    octlogs.write(line)
  elif (month == "November"): 
    novlogs.write(line)
  elif (month == "December"): 
    declogs.write(line)
  else: 
    continue

print("Request Made")
print(file_len(savelog))
totalResponses = file_len(savelog)

print("Average number for month:", round(totalResponses/12,2))

print("Average number for week: ",round(totalResponses/52,2))

print("Average number for day: ", round(totalResponses/365,2))

print("Months:", months)

print("Total redirects:",countRedirects)

print("Redirected requests (3xx):".format(countRedirects/totalResponses))

print("Total number of Errors:",countErrors)

print("Unsuccessful (4xx) requests: ".format(countErrors/totalResponses))	
fileCount()
