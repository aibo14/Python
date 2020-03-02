from urllib.request import urlretrieve
import os
import re
import collections 

months_count ={
  "Jan": 0,
  "Feb": 0,
  "Mar": 0,
  "Apr": 0,
  "May": 0,
  "Jun": 0,
  "Jul": 0,
  "Aug": 0,
  "Sep": 0,
  "Oct": 0,
  "Nov": 0,
  "Dec": 0
}

janlogs=open("january.txt", "a+"); feblogs=open("february.txt", "a+"); marlogs=open("march.txt", "a+"); 
aprlogs=open("april.txt", "a+"); maylogs=open("may.txt", "a+"); junlogs=open("june.txt", "a+");
jullogs=open("july.txt", "a+"); auglogs=open("august.txt", "a+"); seplogs=open("september.txt", "a+")
octlogs=open("octlogs.txt", "a+"); novlogs=open("november.txt", "a+"); declogs=open("december.txt", "a+")   

i=0

redirectCounter = 0
errorCounter = 0

data = 'https://s3.amazonaws.com/tcmg476/http_access_log'

savelog = 'http_access_log'

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
		print("Most commonly requested file: {} with {} requests.".format(str(count[0]), str(count[1])))
	for count in counter.most_common():					
		if str(count[1]) == '1':
			leastcommon.append(count[0])
	if leastcommon:										#there are MANY file requests that only occur once in the string though. Print all? 													
		response = input("Looks like there were {} file(s) that were requested only once, show all? (y/n)".format(len(leastcommon)))
		if response == 'y' or response == 'Y':
			for file in leastcommon:
				print(file)

if not os.path.isfile(savelog):

    urlretrieve(data, savelog)


# Our regex pattern to use later
pattern = r'(.*?) - (.*) \[(.*?)\] \"(.*?) (.*?)\"? (.+?) (.+) (.+)'

# Create a list with each line from the file
lines = open(savelog, 'r').readlines()

# Iterate over the lines (the important part, almost everything is done in this block)
for line in lines:
    # Match our pattern to the line
    match = re.match(pattern, line)

    # If there wasn't a match (error with regex), continue with iteration, skip this loop
    if not match:
        continue

    # You can get all the info you need from the match groups we created a second ago
    # Example:
    match.group(0) # The original line
    match.group(3) # The timestamp
    timestamp = match.group(3)
    month = timestamp[3:6]
    months_count[month] += 1
    match.group(7) # The status codes
    
    if (match.group(7)[0] == "3"):
        redirectCounter += 1
    elif (match.group(7)[0] == "4"):
        errorCounter += 1
    if (month == "Jan"): 
        janlogs.write(line)
    elif (month == "Feb"): 
        feblogs.write(line)
    elif (month == "Mar"): 
        marlogs.write(line)
    elif (month == "Apr"): 
        aprlogs.write(line)
    elif (month == "May"): 
        maylogs.write(line)
    elif (month == "Jun"): 
        junlogs.write(line)
    elif (month == "Jul"): 
        jullogs.write(line)
    elif (month == "Aug"): 
        auglogs.write(line)
    elif (month == "Sep"): 
        seplogs.write(line)
    elif (month == "Oct"): 
        octlogs.write(line)
    elif (month == "Nov"): 
        novlogs.write(line)
    elif (month == "Dec"): 
        declogs.write(line)
    
    else:
        continue
print("Request Made")
print(file_len(savelog))
totalResponses = file_len(savelog)
print("Average monthly request:", round(totalResponses/12,2))
print("Average weekly request: ",round(totalResponses/52,2))
print("Average daily request: ", round(totalResponses/365,2))
print("Months:", (months_count)
print("Total Redirects:",(redirectCounter))
print("Percentage of all requests that were redirects:",(redirectCounter/totalResponses))
print("Total Errors:",(errorCounter)
print("Percentage of client error:",(errorCounter/totalResponses))	
fileCount()
