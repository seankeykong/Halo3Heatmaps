from bs4 import BeautifulSoup
import requests
import os

gamertag = raw_input("Enter Gamertag: ")
url = "http://halo.bungie.net/stats/halo3/heatmapstats.aspx?player="+gamertag
page = requests.get(url)
soup = BeautifulSoup(page.content,"html.parser")

base_dir = "D:/Halo3Heatmaps/"


# get all parameters for heatmap endpoint
# dd1-select is the class for all the heatmap options
# the heatmap endpoint uses the map, weapon, and influence parameters to query the data
maps = []
weapons = []
influence = []

selects = soup.find_all("div",{"class":"ddl-select"})

for i, val in enumerate(selects):
    option = val.find_all("option")
    for j in option:
        if i == 0: # Maps
            map_dict = {"name":j.contents[0],"value":str(j["value"])}
            maps.append(map_dict)
        elif i == 1: # Weapons
            kill_dict = {"name":j.contents[0],"value":str(j["value"])}
            death_dict = {"name":j.contents[0],"value":str(int(j["value"])+128)} # wpn for Deaths is just weapon number plus 128
            weapons.append(kill_dict)
            weapons.append(death_dict)
        # index 2 is just Kills/Deaths with the value of each being 0 and 128
        # if you select Deaths for the heatmap, it takes the current selected weapon and adds 128
        # leaving only 3 paramters needed to query for the heatmap
        elif i == 3: # Influence
            inf_dict = {"name":j.contents[0],"value":str(j["value"])}
            influence.append(inf_dict)

# def create folder
def create_folder(dir):  
    if not os.path.exists(dir):
        os.makedirs(dir)

# create base folder
create_folder(base_dir)

# http://halo.bungie.net/stats/Halo3/HeatMap.ashx?player=XXXXX&map=XXX&wep=XXX&inf=X
# Get each influence intensity for each weapon, both kills and deaths, for each map
# Should yield 24,480 heatmap images
# at around 32Kb each, that's ~1.78 GB
for i in maps:
    map_folder = base_dir+i["name"]+"/"
    create_folder(map_folder)
    for j in weapons:
        weapon_folder = map_folder+j["name"]+"/"
        create_folder(weapon_folder)
        for k in influence:
            print "http://halo.bungie.net/stats/Halo3/HeatMap.ashx?player=%s&map=%s&wep=%s&inf=%s" % (gamertag, i["value"], j["value"], k["name"])