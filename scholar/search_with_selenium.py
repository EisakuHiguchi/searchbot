# -*- coding: utf-8 -*-

from selenium import webdriver
from argparse import ArgumentParser
import sys
from time import sleep
from bs4 import BeautifulSoup
import json
import re

import random


print("Now loading Selenium. Please wait while standing up Webbrowser.")
driver = webdriver.Edge("MicrosoftWebDriver.exe")
driver.get("https://scholar.google.co.jp/")
driver.set_window_size(1000, 1000)

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

def extractdata_finded_list(list_data):
  if len(list_data) < 1:
    return "None"
  else:
    return list_data[0].text

def get_link_data_subcore(section):
  temp_title = section.find_all("h3")
  temp_summary = section.find_all("div", attrs={"class": "gs_rs"})
  temp_year = section.find_all("div", attrs={"class": "gs_a"})

  str_title = extractdata_finded_list(temp_title)
  str_summary = extractdata_finded_list(temp_summary)
  str_year = extractdata_finded_list(temp_year)
  str_year = re.sub(r"\D", "", str_year)
  str_year = str_year[-4:]
  if len(str_year) < 4:
    str_year = "None"

  return [str_title, str_summary, str_year]
  
def get_link_data_sub(section):
  list_temp = get_link_data_subcore(section)
  str_temp = list_temp[0] + "\n  " + list_temp[1] + "\n" + list_temp[2] + "\n\n"
  return str_temp

def get_dict_data_sub(section):
  list_temp = get_link_data_subcore(section)
  dict_temp = {}
  dict_temp["title"] = list_temp[0]
  dict_temp["summary"] = list_temp[1].replace("\n", " ")
  dict_temp["tags"] = [SEARCH_KEY, ""]
  dict_temp["year"] = list_temp[2]
  return dict_temp


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
    dict_temp = get_dict_data_sub(e)
    if not dict_temp in list_dict_result:
      list_dict_result.append(dict_temp)
    else:
      print("same page")
  
  return list_dict_result


def save(str_result):
  print("saving data...")
  f = open("SEARCH_BOT_for_scholar_" + SEARCH_KEY + ".md", "w", encoding="utf-8")
  f.write(str_result)
  f.close()
  print("save done!")

def savejson_dict(list_dict_results):
  print("saving data formatted json...")
  count = 1
  json_data_temp = {}
  for e in list_dict_results:
    json_data_temp["id_" + str(count)] = e
    count += 1
  
  f = open("SEARCH_BOT_for_scholar_" + SEARCH_KEY.replace(" ", "_") + ".json", "w", encoding="utf-8")
  json.dump(json_data_temp, f, ensure_ascii=False, indent=2, sort_keys=True, separators=(',', ': '))
  f.close()
  print("save done!")

def loadjson(filename):
  f = open(filename, "r", encoding="utf-8")
  jsonData = json.load(f)
  f.close()
  return jsonData
# ---- ---- ---- ----
# main

argparser = ArgumentParser()
argparser.add_argument("-d", "--debug", type=bool, default=False)
args = argparser.parse_args()

DEBUG = args.debug
list_dict_results = []


command = input("SEARCH_KEY:")

if command == "continue":
  filename = input("FILEPATH:")
  dict_json = loadjson(filename)
  if dict_json == -1:
    driver.close()
    sys.exit()
  for key in dict_json.keys():
    list_dict_results.append(dict_json[key])
  command = input("SEACH_KEY:")
  #start_search(command)
  SEARCH_KEY = command
else:
  #str_result = "# " + command + " :: SEARCH_BOT for scholar\n"
  #str_result += "----\n\n"
  #str_result = get_link_data(str_result)
  start_search(command)
  SEARCH_KEY = command
  print("getting first page data...")
  list_dict_results = get_dict_link_data(list_dict_results)



count = 0
count_end = 0

if DEBUG:
  print("debug mode")
else:
  while command != "end":
    if count == 0:
      command = input(">>> ")
    else:
      click_next()
      list_dict_results = get_dict_link_data(list_dict_results)
      sleeping = random.uniform(0.5,3)
      print("count:" + str(count) + " sleep:" + str(sleeping))
      sleep(sleeping)
      count += 1

    if command == "next":
      click_next()
      #str_result = get_link_data(str_result)
      list_dict_results = get_dict_link_data(list_dict_results)
    if command == "reload":
      #str_result = get_link_data(str_result)
      list_dict_results = get_dict_link_data(list_dict_results)
    if "count" in command:
      count = 1
      count_end = int(input("count(int)= ")) + 1
      command = "none"


    if count == count_end:
      count = 0

  #save(str_result)
  savejson_dict(list_dict_results)
  driver.close()
  print("done!")

