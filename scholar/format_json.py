
import re
import json

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
  
def format_dict_data(title, tags, summary="", year="none", comment=""):
  dict_temp = {}
  dict_temp["title"] = title
  dict_temp["summary"] = summary
  dict_temp["tags"] = tags
  dict_temp["year"] = year
  dict_temp["comment"] = comment
  return dict_temp

def get_dict_data_sub(section):
  list_temp = get_link_data_subcore(section)

  title = list_temp[0]
  summary = list_temp[1].replace("\n", " ")
  tags = [""]
  year = list_temp[2]
  comment = ""

  return format_dict_data(title, summary, tags, year=year, comment=comment)


def savejson_dict(json_data_temp, filename):
  print("saving data formatted json...")
  f = open(filename, "w", encoding="utf-8")
  json.dump(json_data_temp, f, ensure_ascii=False, indent=2, sort_keys=True, separators=(',', ': '))
  f.close()
  print("save done!")

def loadjson(filename):
  try:
    f = open(filename, "r", encoding="utf-8")
    jsonData = json.load(f)
    f.close()
    return jsonData
  except:
    print("error: format_json.loadjson")
    print(filename)
    return -1
