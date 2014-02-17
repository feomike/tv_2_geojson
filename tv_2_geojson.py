### ---------------------------------------------------------------------------
###   VERSION 0.1
### tv_2_geojson.py
### Created on: Thurs Feb 13 2014
### Created by: Michael Byrne
### Federal Communications Commission 
### ---------------------------------------------------------------------------
###	translates tv service contour data points file extracts from this location
###	http://www.fcc.gov/encyclopedia/tv-service-contour-data-points
###	into geojson format
### ---------------------------------------------------------------------------

inFile = 'TV_service_contour_current.txt'
out_pnt_file = 'tv_point.geojson'
out_ply_file = 'tv_contour.geojson'

# Import system modules
import sys, string, os
import time
from datetime import date
today = date.today()
from numpy import genfromtxt

###value[0] of the FILE is column 1 to 10
###value[0] is the application ID number of the CDBS/TV Query record.
###value[1] of the FILE is column 11 to  13
###value[1] is the service of the station
###value[2] of the FILE is column 14 to 50
###value[2] is  station's description is listed in the next field; 
###		(call sign and application file number) in effect at the time 
###		the service contour data was initially generated.
###		- the call sign is from 14 to 19
###		- the application number is 20 to 49
###value[3] is the NAD83 coordinates |latitude, longitude| of the station's or 
###		application's transmitter site. 
###value[4] through value[364] is atitude, longitude| pairs, with the first 
###		coordinate pair corresponding to the contour location at 0 degrees 
###		(true north) from the transmitter site, and continuing clockwise at 1 
###		degree intervals to 359 degrees.  


###ISSUES:
### - appID might not be unique.  no idea why this is
### - service has values of CA, DC, DD, DM, DN, DR, DS, DT, DX, LD, TV, TX
###		these values are not decoded presently
###	- the call sign isn't being pulled cleanly out of the description.  it could use
###		some work to get the clean call sign.  sometimes this is a 4 digit number, 
###		sometimes it is a 5 digit, sometimes it is a 4 + 2 digit w/ a '-' in between
###	- rather than reading and writing lines, it might be better to read the file in as
###		a csv file or an array and grab data elements out as array elements.
###		to do this w/ python, one would use the genfromtxt command, but i struggled 
###		with it.  below is some skeleton code to do this
###			myData = genfromtxt('new.txt', delimiter="|", na_values=["nan"])
###			print int(myData[0][0])
###			print str(myData[0][1])


#this function sets up the properties of each feature
def getProperties(mycnt, myLn):
	#print myLn[0:10].strip() #is the application ID number of the CDBS/TV Query record.
	#print myLn[11:13].strip() #is the state
	#print myLn[14:19].strip() #is the call sign
	#print myLn[20:49].strip() #is the app num
	myStr = '{ "type": "Feature", "id": ' + str(mycnt) + ', "properties": { '
	myStr = myStr + '"app_id": '+ line[0:10].strip() + ', ' 
	myStr = myStr + '"service": "' + line[11:13].strip() + '", '
	myStr = myStr + '"call_sign": "' + line[14:19].strip() + '", '
	myStr = myStr + '"app_num": "' + line[20:49].strip() + '"}, '
	return(myStr)

#this function sets up the transmitter on its own
def getTransmitter(myLn):
	#print myLn[50:70].strip() #center
	myStr = '"geometry": {"type": "Point", "Coordinates": ['
	myStr = myStr + myLn[60:70].strip() + ',' + myLn[50:58].strip() + ']'
	myStr = myStr + '}}'
	return(myStr)

#this function sets up the contour on its own
def	getContour(myLn):
	#pt 1 is
	#	print line[71:91].strip() #degree 1
	myStr = '"geometry": {"type": "Polygon", "Coordinates": ['
	myStr = myStr + '[[' + myLn[81:91].strip() + ',' + myLn[71:79].strip() + '],'
	#print line[92:112].strip() #degree 2
	i = 92
	while i < 7631:
		myStr = myStr + '[' + myLn[i+10:i+19].strip() + ',' + myLn[i:i+8].strip() + '],'
		i = i + 21
	myStr = myStr + '[' + myLn[81:91].strip() + ',' + myLn[71:79].strip() + ']]]}}'
	return(myStr)
	

#find out how big the file is so you can deal w/ the separating comma's well	
f = open(inFile, 'r')
tcnt = 0
for line in f:
	tcnt = tcnt + 1
f.close()

#set up the transmitter (eg point) output
ptFile = open(out_pnt_file, 'w')
ptFile.write("{" + '\n')
ptFile.write('"type": "FeatureCollection",' + '\n')
ptFile.write('"features": [' + '\n')

#set up the contour (eg polygon) output
pyFile = open(out_ply_file, 'w')
pyFile.write("{" + '\n')
pyFile.write('"type": "FeatureCollection",' + '\n')
pyFile.write('"features": [' + '\n')

f = open(inFile, 'r')
cnt = 1
for line in f:
	theStr = getProperties(cnt, line)
	theFeat = getTransmitter(line)
	if cnt < tcnt:
		theFeat = theFeat + ', '
	ptFile.write(theStr + theFeat + '\n')
	thePoly = getContour(line)
	if cnt < tcnt:
		thePoly = thePoly + ', ' 
	pyFile.write(theStr + thePoly + '\n')	
	cnt = cnt + 1
f.close()
ptFile.write(']}' + '\n')
pyFile.write(']}' + '\n')
ptFile.close()
pyFile.close()
