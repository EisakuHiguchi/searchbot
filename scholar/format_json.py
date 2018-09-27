
import re

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
