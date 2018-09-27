#!/usr/bin/env python3

import requests
import bs4
import json

import format_json

import argparse



# following values(URL,FILENAME) are dummy and sample values
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
  args = parser.parse_args()

  FILENAME = args.Filename[0]
  URL = args.URL[0]
  list_dict_result = []
  result = get_dict_link_data(list_dict_result)
  #print (result)
  savejson_dict(result)
