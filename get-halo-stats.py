from bs4 import BeautifulSoup
import requests

gamertag = raw_input("Enter Gamertag: ")
url = "http://halo.bungie.net/stats/halo3/heatmapstats.aspx?player="+gamertag
page = requests.get(url)
soup = BeautifulSoup(page.content,"html.parser")


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