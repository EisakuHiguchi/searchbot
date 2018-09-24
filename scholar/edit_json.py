# -*- coding: utf-8 -*-

from argparse import ArgumentParser
import json

FILENAME_JSON = "dummy.json"

def savejson_dict(json_data_temp, filename):
  print("saving data formatted json...")
  f = open(filename, "w", encoding="utf-8")
  json.dump(json_data_temp, f, ensure_ascii=False, indent=2, sort_keys=True, separators=(',', ': '))
  f.close()
  print("save done!")

def loadjson():
  f = open(FILENAME_JSON, "r", encoding="utf-8")
  jsonData = json.load(f)
  f.close()
  return jsonData

def add_tag_sub(keyword):
  for key in jsonData.keys():
    summary_temp = jsonData[key]["summary"]
    title_temp = jsonData[key]["title"]
    if (keyword.lower() in summary_temp.lower()) or (keyword.lower() in title_temp.lower()):
      jsonData[key]["tags"].append(keyword)
      if "" in jsonData[key]["tags"]:
        index = jsonData[key]["tags"].index("")
        jsonData[key]["tags"].pop(index)

def add_tag(keyword):
  hitcount = 0
  for key in jsonData.keys():
    summary_temp = jsonData[key]["summary"]
    title_temp = jsonData[key]["title"]
    if (keyword.lower() in summary_temp.lower()) or (keyword.lower() in title_temp.lower()):
      hitcount += 1
  print("HIT: " + str(hitcount))

  if hitcount > 9:
    command = input("Do you replace this keyword? (y/n default N): ")
    if "y" in command:
      add_tag_sub(keyword)
    else:
      print("Not replace")
  else:
    add_tag_sub(keyword)
 

def reflesh_tag():
  for key in jsonData.keys():
    if "" in jsonData[key]["tags"]:
      index = jsonData[key]["tags"].index("")
      jsonData[key]["tags"].pop(index)
    if len(jsonData[key]["tags"]) == 1:
      jsonData[key]["tags"].append("unknown")
    else:
      if "unkown" in jsonData[key]["tags"]:
        index = jsonData[key]["tags"].index("unkown")
        jsonData[key]["tags"].pop(index)

# ---- ---- ---- ---- ----
# main

command = input("FILENAME: ")
FILENAME_JSON = command
jsonData = loadjson()
# copy
savejson_dict(jsonData, FILENAME_JSON+".copy")

while command != "end":
  command = input(">>> ")
  if command == "end":
    break
  elif command == "reflesh":
    reflesh_tag()
  else:
    add_tag(command)
    savejson_dict(jsonData, FILENAME_JSON)
    

print("done!")


