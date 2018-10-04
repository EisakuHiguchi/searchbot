# -*- coding: utf-8 -*-

from selenium import webdriver
from argparse import ArgumentParser
import sys
from time import sleep
from bs4 import BeautifulSoup
import json
from datetime import datetime

import format_json


print("Now loading Selenium. Please wait while standing up Webbrowser.")
driver = webdriver.Edge("MicrosoftWebDriver.exe")
driver.get("https://scholar.google.co.jp/")
#driver.set_window_size(500, 500)

def start_search(KEYWORD):
  driver.find_element_by_id("gs_hdr_tsi").send_keys(KEYWORD)
  driver.find_element_by_name("btnG").click()

def click_next():
  driver.find_element_by_class_name("gs_btnPR gs_in_ib gs_btn_lrge gs_btn_half gs_btn_lsu").click()

def get_source():
  for i in range(0,3):
    print(str(3-i) + "...")
    sleep(1)

  return driver.page_source

def get_soup():
  source = get_source()
  return BeautifulSoup(source, "lxml")

def get_link_section(soup):
  temp = soup.find_all("div", attrs={"class": "gs_ri"})
  list_section = []
  for e in temp:
    list_section.append(e)
  return list_section

def get_link_data(str_result):
  soup = get_soup()
  list_section = get_link_section(soup)
  for e in list_section:
    str_result += get_link_data_sub(e)
  str_result += "----\n"
  return str_result

def get_dict_link_data(list_dict_result):
  soup = get_soup()
  list_section = get_link_section(soup)
  for e in list_section:
    dict_temp = format_json.get_dict_data_sub(e)
    if not dict_temp in list_dict_result:
      list_dict_result.append(dict_temp)
    else:
      print("same page")
  
  return list_dict_result

def savejson(list_dict_results, filename):
  count = 1
  json_data_temp = {}
  for i in range(0,len(list_dict_results)):
    e = list_dict_results[i]
    if "__metadata__" in e["tags"]:
      json_data_temp["id_0"] = e
    else:
      json_data_temp["id_" + str(count)] = e
      count += 1
  format_json.savejson_dict(json_data_temp, filename)
  
def loadjson(filename):
  list_dict_results = []
  dict_json = format_json.loadjson(filename)
  if dict_json == -1:
    print("error: Not Found file. Create new file")
    if ".json" not in filename:
      filename += ".json"
    savejson(list_dict_results, filename)
  else:
    for key in dict_json.keys():
      list_dict_results.append(dict_json[key])
  return list_dict_results

def initialize_json(filename):
  list_dict_results = loadjson(filename)

  dict_metadata = {}
  for i in range(0,len(list_dict_results)):
    if "__metadata__" in list_dict_results[i]["tags"]:
      dict_metadata = list_dict_results.pop(i)
      break
  if len(dict_metadata) == 0:
    title = "__metadata__"
    tags = ["__metadata__", nowtime]
    dict_metadata = format_json.format_dict_data(title, tags)
  else:
    dict_metadata["tags"].append(nowtime)
  list_dict_results.insert(0, dict_metadata)
  savejson(list_dict_results, filename)

  return list_dict_results



# ---- ---- ---- ----
# main

argparser = ArgumentParser()
argparser.add_argument("-d", "--debug", type=bool, default=False)
args = argparser.parse_args()

DEBUG = args.debug
nowtime = datetime.now().strftime("%Y-%m-%d_%H%M%S")

filename = input("FILEPATH:")
if ".json" not in filename:
      filename += ".json"
list_dict_results = initialize_json(filename)

command = "continue"
if DEBUG:
  print("debug mode")
else:
  while command != "end":
    command = input(">>> ")
    list_dict_results = loadjson(filename)
    
    if command == "next":
      click_next()
      list_dict_results = get_dict_link_data(list_dict_results)
      savejson(list_dict_results, filename)
    if command == "reload":
      list_dict_results = get_dict_link_data(list_dict_results)
      savejson(list_dict_results, filename)
    

  savejson(list_dict_results, filename)
  driver.close()
  print("done!")

