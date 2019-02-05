from urllib.request import urlopen
from urllib.request import Request
from bs4 import BeautifulSoup
from datetime import datetime, timezone
from random import choice
import os
import time
import re
import csv
import requests

# Get a random proxy
def getProxy():
     url = 'https://www.sslproxies.org'
     r = requests.get(url)
     soup = BeautifulSoup(r.content, 'html5lib')
     return {'https': choice(list(map(lambda x:x[0]+':'+x[1], 
                             list(zip(map(lambda x:x.text, soup.findAll('td')[::8]),
                             map(lambda x:x.text, soup.findAll('td')[1::8]))))))}

# Get site using proxy
def proxyRequest(requestType, url, **kwargs):
     while 1:
          try:
               proxy = getProxy()
               r = requests.request(requestType, url, proxies=proxy, timeout=5, **kwargs)
               break
          except:
               pass
     return r

# Get AIS Type
def AISType(searchPat, searchTerm, advancedData):
     variable = re.split(searchPat,searchTerm)
     if re.search(searchPat, searchTerm):     
          advancedData.insert(0, variable[1].strip())

# Get flag
def flag(searchPat, searchTerm, advancedData):
     variable = re.split(searchPat,searchTerm)
     if re.search(searchPat, searchTerm):     
          if variable[1].strip() != "-":
               advancedData.insert(1, variable[1].strip())                                        

# Get destination
def destination(searchPat, searchTerm, advancedData):
     variable = re.split(searchPat,searchTerm)
     if re.search(searchPat, searchTerm):     
          if variable[1].strip() != "-":
               advancedData.insert(2, variable[1].strip())

# Get ETA
def ETA(searchPat, searchTerm, advancedData):
     variable = re.split(searchPat,searchTerm)
     if re.search(searchPat, searchTerm):     
          if variable[1].strip() != "-":
               advancedData.insert(3, variable[1].strip())

# Get IMO / MMSI
def IMOMMSI(searchPat, searchTerm, advancedData):
     variable = re.split(searchPat,searchTerm)
     if re.search(searchPat, searchTerm):     
          advancedData.insert(4, variable[1].strip())
     
# Get callsign
def callsign(searchPat, searchTerm, advancedData):
     variable = re.split(searchPat,searchTerm)
     if re.search(searchPat, searchTerm):     
          if variable[1].strip() != "-":
               advancedData.insert(5, variable[1].strip())
     
# Get length
def length(searchPat, searchTerm, advancedData):
     variable = re.split(searchPat,searchTerm)
     lengthShipPat = re.compile(r' \/ \d* m$')
     if re.search(searchPat, searchTerm):     
          if variable[1].strip() != "-":
               lengthSearchTerm = variable[1].strip()
               lengthVar = re.split(lengthShipPat, lengthSearchTerm)
               advancedData.insert(6, lengthVar[0].strip())
          
def beam(searchPat, searchTerm, advancedData):
     variable = re.split(searchPat,searchTerm)
     beamShipPat = re.compile(r'^\d* / ')
     metersPat = re.compile(r' m$')
     if re.search(searchPat, searchTerm):     
          if variable[1].strip() != "-":
               beamSearchTerm = variable[1].strip()
               beamVar = re.split(beamShipPat, beamSearchTerm)
               beamVar = re.split(metersPat, beamVar[1].strip())
               advancedData.insert(7, beamVar[0].strip())

# Get current draught
def currentDraught(searchPat, searchTerm, advancedData):
     variable = re.split(searchPat,searchTerm)
     metersPat = re.compile(r' m$')
     if re.search(searchPat, searchTerm):
          if variable[1].strip() != "-":
               currentDraughtVar = re.split(metersPat, variable[1].strip())
               advancedData.insert(8, currentDraughtVar[0])

# Get current course
def currentCourse(searchPat, searchTerm, advancedData):
     variable = re.split(searchPat,searchTerm)
     coursePat = re.compile(r'° \/ \d*\.?\d*')
     dashPat = re.compile(r'^-')
     if re.search(searchPat, searchTerm):     
          courseSpeedSearchTerm = variable[1].strip()
          courseVar = re.split(coursePat, courseSpeedSearchTerm)
          if courseVar[0].strip() != "-": 
               if not (re.search(dashPat, courseSpeedSearchTerm)):
                    advancedData.insert(9, courseVar[0].strip())

# Get current speed
def currentSpeed(searchPat, searchTerm, advancedData):
     variable = re.split(searchPat,searchTerm)
     speedPat = re.compile(r'^\d*\.?\d*° \/ |^- \/')
     knPat = re.compile(r' kn$')
     if re.search(searchPat, searchTerm):     
          courseSpeedSearchTerm = variable[1].strip()
          speedVar = re.split(speedPat, courseSpeedSearchTerm)
          speedSearchTerm = speedVar[1]
          knVar = re.split(knPat, speedSearchTerm)
          if knVar[0].strip() != "-":
               advancedData.insert(10, knVar[0].strip())

# Get latitude
def latitude(searchPat, searchTerm, advancedData):
     variable = re.split(searchPat,searchTerm)
     latPat = re.compile(r'\/\d*\.?\d* (E|W)$')
     if re.search(searchPat, searchTerm):
          latLongSearchTerm = variable[1].strip()
          latVar = re.split(latPat, latLongSearchTerm)
          if latVar[0].strip() != "-": 
               advancedData.insert(11, latVar[0].strip())


# Get longitude
def longitude(searchPat, searchTerm, advancedData):
     variable = re.split(searchPat,searchTerm)
     longPat = re.compile(r'^\d*\.?\d* (N|S)\/')
     if re.search(searchPat, searchTerm):     
          latLongSearchTerm = variable[1].strip()
          longVar = re.split(longPat, latLongSearchTerm)
          if longVar[2].strip() != "-":
               advancedData.insert(12, longVar[2].strip())

# Get last report
def lastReport(searchPat, searchTerm, advancedData):
     variable = re.split(searchPat,searchTerm)
     UTCPat = re.compile(r' UTC$')
     if re.search(searchPat, searchTerm):     
          lastReportSearchTerm = variable[1].strip()
          lastReportVar = re.split(UTCPat, lastReportSearchTerm)
          advancedData.insert(13, lastReportVar[0])


# Get IMO number
def IMONumber(searchPat, searchTerm, advancedData):
     variable = re.split(searchPat,searchTerm)
     if re.search(searchPat, searchTerm):
          if variable[1].strip() != "-":
               advancedData.insert(14, variable[1].strip())

# Get vessel name
def vesselName(searchPat, searchTerm, advancedData):
     variable = re.split(searchPat,searchTerm)
     if re.search(searchPat, searchTerm):
          if variable[1].strip() != "-":
               advancedData.insert(15, variable[1].strip())

# Get ship type
def shipTypeMaster(searchPat, searchTerm, advancedData):
     variable = re.split(searchPat,searchTerm)
     if re.search(searchPat, searchTerm):     
          if variable[1].strip() != "-":
               advancedData.insert(16, variable[1].strip())

# Get flag
def flagMaster(searchPat, searchTerm, advancedData):
     variable = re.split(searchPat,searchTerm)
     if re.search(searchPat, searchTerm):     
          if variable[1].strip() != "-":
               advancedData.insert(17, variable[1].strip())

# Get homeport
def homeport(searchPat, searchTerm, advancedData):
     variable = re.split(searchPat,searchTerm)
     if re.search(searchPat, searchTerm):     
          if variable[1].strip() != "-":
               advancedData.insert(18, variable[1].strip())

# Get gross tonnage
def grossTonnage(searchPat, searchTerm, advancedData):
     variable = re.split(searchPat,searchTerm)
     if re.search(searchPat, searchTerm):     
          if variable[1].strip() != "-":
               advancedData.insert(19, variable[1].strip())

# Get summer deadweight
def summerDeadweight(searchPat, searchTerm, advancedData):
     variable = re.split(searchPat,searchTerm)
     if re.search(searchPat, searchTerm):     
          if variable[1].strip() != "-":
               advancedData.insert(20, variable[1].strip())
     
# Get length overall
def lengthOverall(searchPat, searchTerm, advancedData):
     variable = re.split(searchPat,searchTerm)
     if re.search(searchPat, searchTerm):     
          if variable[1].strip() != "-":
               advancedData.insert(21, variable[1].strip())

# Get beam
def breadth(searchPat, searchTerm, advancedData):
     variable = re.split(searchPat,searchTerm)
     if re.search(searchPat, searchTerm):     
          if variable[1].strip() != "-":
               advancedData.insert(22, variable[1].strip())

# Get draught
def draught(searchPat, searchTerm, advancedData):
     variable = re.split(searchPat,searchTerm)
     if re.search(searchPat, searchTerm):     
          if variable[1].strip() != "-":
               advancedData.insert(23, variable[1].strip())

# Get year of built
def yearOfBuilt(searchPat, searchTerm, advancedData):
     variable = re.split(searchPat,searchTerm)
     if re.search(searchPat, searchTerm):     
          if variable[1].strip() != "-":
               advancedData.insert(24, variable[1].strip())
     
# Get builder
def builder(searchPat, searchTerm, advancedData):
     variable = re.split(searchPat,searchTerm)
     if re.search(searchPat, searchTerm):     
          if variable[1].strip() != "-":
               advancedData.insert(25, variable[1].strip())

# Get place of built
def placeOfBuilt(searchPat, searchTerm, advancedData):
     variable = re.split(searchPat,searchTerm)
     if re.search(searchPat, searchTerm):     
          if variable[1].strip() != "-":
               advancedData.insert(26, variable[1].strip())

# Get yard
def yard(searchPat, searchTerm, advancedData):
     variable = re.split(searchPat,searchTerm)
     if re.search(searchPat, searchTerm):     
          if variable[1].strip() != "-":
               advancedData.insert(27, variable[1].strip())

# Get TEU
def TEU(searchPat, searchTerm, advancedData):
     variable = re.split(searchPat,searchTerm)
     if re.search(searchPat, searchTerm):     
          if variable[1].strip() != "-":
               advancedData.insert(28, variable[1].strip())

# Get crude
def crude(searchPat, searchTerm, advancedData):
     variable = re.split(searchPat,searchTerm)
     if re.search(searchPat, searchTerm):     
          if variable[1].strip() != "-":
               advancedData.insert(29, variable[1].strip())

# Get grain
def grain(searchPat, searchTerm, advancedData):
     variable = re.split(searchPat,searchTerm)
     if re.search(searchPat, searchTerm):     
          if variable[1].strip() != "-":
               advancedData.insert(30, variable[1].strip())

# Get bale
def bale(searchPat, searchTerm, advancedData):
     variable = re.split(searchPat,searchTerm)
     if re.search(searchPat, searchTerm):     
          if variable[1].strip() != "-":
               advancedData.insert(31, variable[1].strip())

# Get registered owner
def registeredOwner(searchPat, searchTerm, advancedData):
     variable = re.split(searchPat,searchTerm)
     if re.search(searchPat, searchTerm):     
          if variable[1].strip() != "-":
               advancedData.insert(32, variable[1].strip())

# Get manager
def manager(searchPat, searchTerm, advancedData):
     variable = re.split(searchPat,searchTerm)
     if re.search(searchPat, searchTerm):     
          if variable[1].strip() != "-":
               advancedData.insert(33, variable[1].strip())

def getAISData(link):

     with open('vesselData.csv','a', newline='') as csv_file:
          csv_writer = csv.writer(csv_file, delimiter="\t")

          try:

               # Construct URL
               baseURL = "https://www.vesselfinder.com"
               shipLink = link
               url = baseURL + shipLink

               # Open and parse requested URL
               webpage = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:63.0) Gecko/20100101 Firefox/63.0'})
               if webpage.status_code == 200:
                    bsObj = BeautifulSoup(webpage.content, "html.parser")

                    # Find the table containg the AIS Data
                    vesselTables = bsObj.find_all("table", class_="tparams")

                    advancedData = [""] * 35
                    jj = 0

                    AISTypePat = re.compile(r'^AIS Type')
                    flagPat = re.compile(r'^Flag')
                    destinationPat = re.compile(r'^Destination')
                    ETAPat = re.compile(r'^ETA')
                    IMOMMSIPat = re.compile(r'^IMO \/ MMSI')
                    callsignPat = re.compile(r'^Callsign')
                    lengthBeamPat = re.compile(r'^Length \/ Beam')
                    currentDraughtPat = re.compile(r'^Current draught')
                    courseSpeedPat = re.compile(r'^Course \/ Speed')
                    coordinatesPat = re.compile(r'^Coordinates')
                    lastReportPat = re.compile(r'^Last report  ')
                    IMOPat = re.compile(r'^IMO number')
                    vesselNamePat = re.compile(r'^Vessel Name')
                    shipTypeMasterPat = re.compile(r'^Ship type')
                    homeportPat = re.compile(r'^Homeport')
                    grossTonnagePat = re.compile(r'^Gross Tonnage')
                    summerDeadweightPat = re.compile(r'^Summer Deadweight \(t\)')
                    lengthPat = re.compile(r'^Length Overall \(m\)')
                    beamPat = re.compile(r'^Beam \(m\)')
                    draughtPat = re.compile(r'^Draught \(m\)')
                    yearOfBuiltPat = re.compile(r'Year of Built')
                    builderPat = re.compile(r'^Builder')
                    placeOfBuiltPat = re.compile(r'^Place of Built')
                    yardPat = re.compile(r'^Yard')
                    teuPAT = re.compile(r'^TEU')
                    crudePat = re.compile(r'^Crude')
                    grainPat = re.compile(r'^Grain')
                    balePat = re.compile(r'^Bale')
                    registeredOwnerPat = re.compile(r'^Registered Owner')
                    managerPat = re.compile(r'^Manager')               

                    for vesselTable in vesselTables:
                         vesselRows = vesselTable.find_all("tr")
                    
                         for vesselRow in vesselRows:
                              
                              searchTerm = vesselRow.text

                              if jj == 0:
                                   AISType(AISTypePat, searchTerm, advancedData)
                              elif jj == 1:
                                   flag(flagPat, searchTerm, advancedData)
                              elif jj == 2:
                                   destination(destinationPat, searchTerm, advancedData)
                              elif jj == 3:
                                   ETA(ETAPat, searchTerm, advancedData)
                              elif jj == 4:
                                   IMOMMSI(IMOMMSIPat, searchTerm, advancedData)
                              elif jj == 5:
                                   callsign(callsignPat, searchTerm, advancedData)
                              elif jj == 6:
                                   length(lengthBeamPat, searchTerm, advancedData)
                                   beam(lengthBeamPat, searchTerm, advancedData)
                              elif jj == 7:
                                   currentDraught(currentDraughtPat, searchTerm, advancedData)
                              elif jj == 8:
                                   currentCourse(courseSpeedPat, searchTerm, advancedData)
                                   currentSpeed(courseSpeedPat, searchTerm, advancedData)
                              elif jj == 9:
                                   latitude(coordinatesPat, searchTerm, advancedData)
                                   longitude(coordinatesPat, searchTerm, advancedData)
                              elif jj == 10:
                                   lastReport(lastReportPat, searchTerm, advancedData)
                              elif jj == 11:
                                   IMONumber(IMOPat, searchTerm, advancedData)
                              elif jj == 12:
                                   vesselName(vesselNamePat, searchTerm, advancedData)
                              elif jj == 13:
                                   shipTypeMaster(shipTypeMasterPat, searchTerm, advancedData)
                              elif jj == 14:
                                   flagMaster(flagPat, searchTerm, advancedData)
                              elif jj == 15:
                                   homeport(homeportPat, searchTerm, advancedData)
                              elif jj == 16:
                                   grossTonnage(grossTonnagePat, searchTerm, advancedData)
                              elif jj == 17:
                                   summerDeadweight(summerDeadweightPat, searchTerm, advancedData)
                              elif jj == 18:
                                   lengthOverall(lengthPat, searchTerm, advancedData)
                              elif jj == 19:
                                   breadth(beamPat, searchTerm, advancedData)
                              elif jj == 20:
                                   draught(draughtPat, searchTerm, advancedData)
                              elif jj == 21:
                                   yearOfBuilt(yearOfBuiltPat, searchTerm, advancedData)
                              elif jj == 22:
                                   builder(builderPat, searchTerm, advancedData)
                              elif jj == 23:
                                   placeOfBuilt(placeOfBuiltPat, searchTerm, advancedData)
                              elif jj == 24:
                                   yard(yardPat, searchTerm, advancedData)
                              elif jj == 25:
                                   TEU(teuPAT, searchTerm, advancedData)
                              elif jj == 26:
                                   crude(crudePat, searchTerm, advancedData)
                              elif jj == 27:
                                   grain(grainPat, searchTerm, advancedData)
                              elif jj == 28:
                                   bale(balePat, searchTerm, advancedData)
                              elif jj == 29:
                                   registeredOwner(registeredOwnerPat, searchTerm, advancedData)
                              elif jj == 30:
                                   manager(managerPat, searchTerm, advancedData)

                              if searchTerm != 'Newer position via Satellite ':
                                   if searchTerm != 'Last Port CallActual time of Arrival (UTC)':
                                        jj = jj + 1
                    
                    timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
                    advancedData.insert(34, timestamp)
                    del advancedData[35:]
                    csv_writer.writerow(advancedData)
               
               else:
                    print(link, webpage.status_code)
          
          except Exception as error:
               print(link, error)
               if error == "HTTP Error 404: Not Found":
                    print(link, error)
               elif error == "HTTP Error 502: Proxy Error":
                    print(link, error)
               else:
                    raise

# Start timer
start = time.time()

# Construct URL
baseURL = "https://www.vesselfinder.com/vessels?page="
typeURL = ""
i = 8741
url = baseURL + str(i) + typeURL

# Open and parse requested URL
webpage = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:63.0) Gecko/20100101 Firefox/63.0'})
if webpage.status_code == 200:
     bsObj = BeautifulSoup(webpage.content, "html.parser")
else:
     print(url, webpage.status_code)

# Find the maximum number of pages
maxNoPages = bsObj.find_all("span")
maxNoPagesPat = re.compile(r'\d\d\D\d\d\d$') # The Pattern needs attention
maxNoPages = re.search(maxNoPagesPat,maxNoPages[4].text)
maxNoPages = maxNoPages.group()
commaPat = re.compile(r'\D')
maxNoPages = re.split(commaPat,maxNoPages)
maxNoPages = maxNoPages[0]+maxNoPages[1]

# Open a CSV file to save scrape data into
file = open(os.path.expanduser("vesselFinderTest.csv"),"ab")

while True:

     # Break when maximum number of pages is reached
     if i > int(maxNoPages):
          break
     
     # Open and parse requested URL
     if webpage.status_code == 200:
          bsObj = BeautifulSoup(webpage.content, "html.parser")

          # Find the table containg the results 
          table = bsObj.find("table", class_="results")
          rows = table.find_all("tr")

          # Define a pattern to extract ship type out of the ship name
          shipTypePat = re.compile(r'Asphalt\/Bitumen Tanker|Anchor Handling Vessel|Anchor Hoy|Attack Vessel, Naval|Aircraft Carrier|Air Cushion Vehicle \(Hovercraft\)|Buoy \& Lighthouse Tender|Bulk/Oil Carrier|Buoy Tender|Bulk Dry|Barge Carrier|Bulk Cement Barge, non propelled|Corvette|Chemical Tanker|Chemical/Products Tank Barge, non propelled|Aggregates Carrier|Anti-polution|Buoy\/Lighthouse Vessel|Bulk Carrier|Bunkering Tanker|Cable Layer|Crew Boat|Cargo ship|Cruiser|Cement Carrier|Chemical/Oil Products Tanker|Container Ship|Crude Oil Tanker|Crane Ship|Destroyer|Drilling Rig, semi submersible|Deck Cargo Ship|Dredger|Diving ops|Dredging or UW ops|Diving Support Vessel|Drilling Ship|Exhibition Vessel|Fish Factory Ship|Fish Carrier|Fishing Vessel|Fishing vessel|Fire Fighting Vessel|Frigate|FSO \(Floating, Storage, Offloading\)|FPSO \(Floating, Production, Storage, Offloading\)|Fruite Juice Tanker|Fishing Support Vessel|Floating Dock|General Cargo|General Cargo Ship|Hospital Vessel|Heavy Load Carrier|Hopper Dredger|Hopper Barge, non propelled|HSC|HSC \(HAZ-A\)|Icebreaker|Inland Waterways Tanker|Inland Waterways Passenger|Landing Craft|Local type|Leisure Vessels|Law enforcment|Liquefied Gas|Livestock Carrier|LNG Tanker|Limestone Carrier|LPG Tanker|Landing Ship \(Dock Type\)|Minehunter|Mining Vessel|Munitions Carrier|Minesweeper|Mooring Vessel|Medical|Military ops|Motor Hopper|Netlayer|Nuclear Fuel Carrier|Naval\/Naval Auxiliary|Non Propelled Barge|Non Merchant Ships|Oil Products Tanker|Offshore Support Vessel|Offshore Tug\/Supply Ship|Other type|Other Non Merchant Ships|Ore\/Oil Carrier|Ore/Bulk/Products Carrier|Ore Carrier|Platform|Passenger|Passenger Ship|Ro-Ro Cargo|Restaurant Vessel, Stationary|Passenger/Ro-Ro Cargo Ship|Passenger ship|Passenger \(Cruise\) Ship|Patrol Vessel|Pipe Burying Vessel|Pipe Layer|Pilot|Pleasure craft|Pontoon|Powder Carrier|Palletised Cargo Ship|Pollution Control Vessel|Production Testing Vessel|Port tender|Pusher Tug|Pipe Carrier|Power Station Vessel|Research Survey Vessel|Ro-Ro Cargo Ship|Refrigerated Cargo|Refrigerated Cargo Ship|Resolution 18 ship|Refined Sugar Carrier|Research Vessel|Self Discharging Bulk Carrier|Standby Safety Vessel|Seal Catcher|Sailing vessel|Sailing Vessel|Search & Rescue Vessel|SAR|Supply Tender|Salvage Ship|Submarine|Tanker|Trans Shipment Vessel|Tank Cleaning Vessel|Training Ship|Towing vessel|Trawler|Tug|Torpedo Recovery Vessel|Trenching Support Vessel|Urea Carrier|Unknown|Utility Vessel|Vehicles Carrier|Vessel \(function unknown\)|Yacht|Vegetable Oil Tanker|Work\/Repair Vessel|Wood Chips Carrier|Waste Disposal Vessel|Well Stimulation Vessel|WIG \(HAZ-A\)|WIG \(HAZ-B\)|WIG \(HAZ-C\)|WIG \(HAZ-D\)|Whale Catcher|WIG$')
          
          shipIMOPat = re.compile(r'-IMO-[0-9]*')
          shipIMOPatString = re.compile(r'IMO-')
          shipMMSIPat = re.compile(r'-MMSI-')
          shipNamePat = re.compile(r'/vessels/')

          # Gather all different data
          shipLink = bsObj.find_all("a", class_="ship-link")
          shipName = bsObj.find_all("td", class_="v2")
          builtYear = bsObj.find_all("td", class_="v3")
          shipGrossTonnage = bsObj.find_all("td", class_="v4")
          shipDWT = bsObj.find_all("td", class_="v5")
          shipSize = bsObj.find_all("td", class_="v6")
     
          # Rows counter
          j = 0

          for row in rows:
               if j < len(rows) - 1:

                    # Find and separate IMO number and MMSI from ship link
                    shipLinkSearch = shipLink[j].get("href")
                    shipIMOVar = re.search(shipIMOPat,shipLinkSearch)                             
                    shipVAR = re.split(shipIMOPat,shipLinkSearch)
                    shipNameSearch = shipVAR[0]
                    shipIMOSearch = shipIMOVar.group()
                    shipMMSISearch = shipVAR[1]

                    getAISData(shipLinkSearch)

                    shipIMOVar = re.split(shipIMOPatString,shipIMOSearch)
                    shipIMO = shipIMOVar[1]
                    if shipIMO == "0":
                         shipIMO = ""

                    shipMMSIVar = re.split(shipMMSIPat,shipMMSISearch)
                    shipMMSI = shipMMSIVar[1]
                    if shipMMSI == "0":
                         shipMMSI = ""
                    
                    shipNameVar = re.split(shipNamePat,shipNameSearch)
                    shipNameExtr = shipNameVar[1]
                    shipNameExtr = re.sub("---", "-", shipNameExtr)
                    shipNameExtr = re.sub("--", "-", shipNameExtr)
                    shipNameExtr = re.sub("-", " ", shipNameExtr)

                    shipTypeSearch = shipName[j].text.strip()

                    # Find and seperate actual ship name and ship type out of scraped ship name
                    shipTypeSearch = re.sub("-KVB-", "KVB", shipTypeSearch)
                    shipTypeSearch = re.sub("   ", " ", shipTypeSearch)
                    shipTypeSearch = re.sub("  ", " ", shipTypeSearch)
                    shipTypeSearch = re.sub("---", "-", shipTypeSearch)
                    shipTypeSearch = re.sub("--", "-", shipTypeSearch)
                    shipTypeSearch = re.sub(" - ", " ", shipTypeSearch)
                    shipTypeSearch = re.sub(" -", " ", shipTypeSearch)
                    shipTypeSearch = re.sub("- ", " ", shipTypeSearch)
                    shipTypeSearch = re.sub("-", " ", shipTypeSearch)
                    shipTypeVar = re.search(shipNameExtr,shipTypeSearch)
                    shipNameVar = re.split(shipNameExtr.strip(),shipTypeSearch)
                    shipType = shipNameVar[1].strip()

                    year = builtYear[j].text
                    if year == "-":
                         year = ""
                    
                    gt = shipGrossTonnage[j].text
                    if gt == "-":
                         gt = ""

                    dwt = shipDWT[j].text
                    if dwt == "-":
                         dwt = ""

                    size = shipSize[j].text
                    if size == "-":
                         size = ""

                    link = shipLink[j].get("href")

                    statsSaved = shipIMO + "\t" + shipMMSI + "\t" + shipNameExtr + "\t" + shipType + "\t" + year + "\t" + gt + "\t" + dwt + "\t" + size + "\t" + link + "\t" + str(i) + "\n"
                    j = j + 1    
               else:
                    break
               
               # Write all scraped data in the CSV file
               file.write(bytes(statsSaved, encoding="ascii", errors="ignore"))
          
          else:
               print(url, webpage.status_code)
     
     #Change the URL
     url = baseURL + str(i) + typeURL
     webpage = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:63.0) Gecko/20100101 Firefox/63.0'})
     
     #Print elapsed time and page number
     step = time.time()
     print(step-start, i, i/int(maxNoPages)*100, "%")

     i = i + 1

#Print elapsed time and page number
end = time.time()
print("Scraping Done - Time Elapsed:",end-start, "seconds - Pages Retrived:", i)