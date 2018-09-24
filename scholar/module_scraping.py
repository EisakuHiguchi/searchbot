#!/usr/bin/env python3

import requests
import bs4
import re
import json


import argparse

URL = "https://scholar.google.co.jp/scholar?start=10&hl=ja&as_sdt=2005&sciodt=0,5&cites=3982677450424843587&scipsc="
FILENAME = "Minimal solvers for generalized pose and scale estimation from two rays and one point2"

def get_soup():
  get_url_info = requests.get(URL)
  bs4Obj = bs4.BeautifulSoup(get_url_info.text, "lxml")
  return bs4Obj


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
  

def get_dict_data_sub(section):
  list_temp = get_link_data_subcore(section)
  dict_temp = {}
  dict_temp["title"] = list_temp[0]
  dict_temp["summary"] = list_temp[1].replace("\n", " ")
  dict_temp["tags"] = [""]
  dict_temp["year"] = list_temp[2]
  dict_temp["comment"] = ""
  return dict_temp


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


def savejson_dict(list_dict_results):
  print("saving data formatted json...")
  count = 1
  json_data_temp = {}
  for e in list_dict_results:
    json_data_temp["id_" + str(count)] = e
    count += 1
  
  f = open(FILENAME + ".json", "w", encoding="utf-8")
  json.dump(json_data_temp, f, ensure_ascii=False, indent=2, sort_keys=True, separators=(',', ': '))
  f.close()
  print("save done!")


# ---- ----
# main

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument('URL', metavar='URL', type=str, nargs='+',
    help='A Page URL in Google Sholar ')
  parser.add_argument('Filename', metavar='F', type=str, nargs='+',
    help='Filename for saving data')

  FILENAME = parser.Filename
  URL = parser.URL
  list_dict_result = []
  result = get_dict_link_data(list_dict_result)
  #print (result)
  savejson_dict(result)
