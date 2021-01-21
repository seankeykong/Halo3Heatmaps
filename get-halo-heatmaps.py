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
    # create base map folders
    map_folder = base_dir+i["name"]+"/"
    create_folder(map_folder)
    for j in weapons:
        # create base weapon sub-folders
        weapon_folder = map_folder+j["name"]+"/"
        create_folder(weapon_folder)
        # create Kills and Deaths sub-folders based on weapon number
        if int(j["value"]) > 127:
            create_folder(weapon_folder+"Deaths/")
        else:
            create_folder(weapon_folder+"Kills/")
        for k in influence:
            # heatmap url
            heatmap_url = "http://halo.bungie.net/stats/Halo3/HeatMap.ashx?player=%s&map=%s&wep=%s&inf=%s" \
            % (gamertag, i["value"], j["value"], k["name"])

            # e.g. Assembly-All-Weapons-Influence-6.jpg
            # or The Pit-Battle Rifle-Influence-4.jpg
            filename = i["name"]+"-"+j["name"]+"-"+"Influence-"+k["name"]+".jpg"

            # determine hwether to put into Kills or Deaths Folder
            file_destination = weapon_folder
            if int(j["value"]) > 127:
                file_destination = file_destination+"Deaths/"+filename
            else:
                file_destination = file_destination+"Kills/"+filename

            # get heatmap and write to specified location
            heatmap = requests.get(heatmap_url).content
            with open(file_destination, 'wb') as handler:
                handler.write(heatmap)
            handler.close()

            print file_destination

