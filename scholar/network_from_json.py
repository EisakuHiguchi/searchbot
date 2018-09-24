# -*- coding: utf-8 -*-

import os
import json
import collections
import itertools
import networkx as nx
import matplotlib.pyplot as plt

from datetime import datetime
nowtime = datetime.now().strftime("%Y-%m-%d_%H%M%S")

FILENAME_JSON = input("Filename:")
#FILENAME_JSON = os.path.basename(FILENAME_JSON)

#FILENAME_JSON = "SEARCH_BOT_for_scholar_groebner computer graphics.json"
FILENAME_SAVEFIG = nowtime + "_" + os.path.basename(FILENAME_JSON).split("SEARCH_BOT_for_scholar_")[1].split(".")[0]
FILENAME_SAVEFIG_CLOUD = FILENAME_SAVEFIG + "_CLOUD"
FILENAME_SAVEFIG_CLOUD2 = FILENAME_SAVEFIG + "_WORDS_CLOUD"

def loadjson():
  f = open(FILENAME_JSON, "r", encoding="utf-8")
  jsonData = json.load(f)
  f.close()
  return jsonData

def all_tags_list():
  taglist = []
  jsonData = loadjson()
  for key in jsonData.keys():
    taglist.append(jsonData[key]["tags"])
  tag_count = collections.Counter(itertools.chain.from_iterable(taglist))
  tag_most = tag_count.most_common()
  
  result = []
  for e in tag_most:
    result.append(e[0]) 
  return result


def create_tag_cloud():
  jsonData = loadjson()
  taglist = [] 
  for key in jsonData.keys():
    taglist.append(jsonData[key]["tags"])
  tag_count = collections.Counter(itertools.chain.from_iterable(taglist))
  deltemp = tag_count.most_common(1)
  tag_count.pop(deltemp[0][0])


  G = nx.Graph()
  G.add_nodes_from([(tag, {"count":count}) for tag, count in tag_count.most_common()])
              
  for tags in taglist:
    for tag0, tag1 in itertools.combinations(tags, 2):
      if not G.has_node(tag0) or not G.has_node(tag1):
        continue
      if G.has_edge(tag0, tag1):
        G[tag0][tag1]["weight"] += 1
      else:
        G.add_edge(tag0, tag1, weight=1)

  plt.figure(figsize=(15,15)) # グラフのサイズを定義
  pos = nx.spring_layout(G, k=1.5) # ノード間の反発力を定義。値が小さいほど密集する

  node_size = [ d['count']*50 for (n,d) in G.nodes(data=True)] # ノードの大きさを調整
  nx.draw_networkx_nodes(G, pos, node_color='b', alpha=0.2, node_size=node_size, font_weight="bold", font_family='VL Gothic') # ノードのスタイルを定義
  nx.draw_networkx_labels(G, pos, fontsize=14)

  edge_width = [ d['weight']*0.5 for (u,v,d) in G.edges(data=True)] # エッジの太さを調整
  nx.draw_networkx_edges(G, pos, alpha=0.4, edge_color='r', width=edge_width) # エッジのスタイルを定義

  plt.axis('off')
  plt.savefig(FILENAME_SAVEFIG_CLOUD)
  #plt.show()
  plt.close()
  G.clear()

def remove_lesswords(listdata):
  temp = []
  for e in listdata:
      if len(e) > 3:
        temp.append(e.lower().replace(",","").replace(".",""))
  return temp

def create_text_cloud(prm):
  prm_mostcommon = prm # prm_mostcommon = 20
  prm_least_flag = False

  jsonData = loadjson()
  taglist = [] 
  
  for key in jsonData.keys():
    taglist.append(remove_lesswords(jsonData[key]["summary"].split(" ")))
    taglist.append(remove_lesswords(jsonData[key]["title"].split(" ")))
    taglist.append(jsonData[key]["tags"][1:])
  
  tag_count = collections.Counter(itertools.chain.from_iterable(taglist))
  G = nx.Graph()
  listlen = len(tag_count.most_common())
  
  if prm_least_flag:
    G.add_nodes_from([(tag, {"count":count}) for tag, count in tag_count.most_common()[-prm_mostcommon:]])
  else:
    G.add_nodes_from([(tag, {"count":count}) for tag, count in tag_count.most_common(prm_mostcommon)])
              
  for tags in taglist:
    for tag0, tag1 in itertools.combinations(tags, 2):
      if not G.has_node(tag0) or not G.has_node(tag1):
        continue
      if G.has_edge(tag0, tag1):
        G[tag0][tag1]["weight"] += 1
      else:
        G.add_edge(tag0, tag1, weight=1)

  plt.figure(figsize=(15,15)) # グラフのサイズを定義
  pos = nx.spring_layout(G, k=1.5) # ノード間の反発力を定義。値が小さいほど密集する

  node_size = [ d['count']*50 for (n,d) in G.nodes(data=True)] # ノードの大きさを調整
  nx.draw_networkx_nodes(G, pos, node_color='b', alpha=0.2, node_size=node_size, font_weight="bold", font_family='VL Gothic') # ノードのスタイルを定義
  nx.draw_networkx_labels(G, pos, fontsize=14)

  edge_width = [ d['weight']*0.5 for (u,v,d) in G.edges(data=True)] # エッジの太さを調整
  nx.draw_networkx_edges(G, pos, alpha=0.4, edge_color='r', width=edge_width) # エッジのスタイルを定義

  plt.axis('off')
  plt.savefig(FILENAME_SAVEFIG_CLOUD2)
  #plt.show()
  plt.close()
  G.clear()


def create_year_map():
  jsonData = loadjson()
  taglist = []
  for key in jsonData.keys():
    temp = jsonData[key]["tags"]
    year = jsonData[key]["year"][-4:]
    if year != "None":
      temp.append(int(year))
      taglist.append(temp)
    
  max_year = 0
  min_year = 3000
  dict_taglist = {}
  for e in taglist:
    if e[-1] in dict_taglist.keys():
      temp = dict_taglist[e[-1]]
      set_temp = set(e[1:-1])
      temp = temp | set_temp
      dict_taglist[e[-1]] = temp
    else:
      temp = set(e[1:-1])
      dict_taglist[e[-1]] = temp
    
    if max_year < e[-1]:
      max_year = e[-1]    
    if min_year > e[-1]:
      min_year = e[-1]

  tag_count = collections.Counter(itertools.chain.from_iterable(taglist))
  main_tag = tag_count.most_common(2)[1][0]

  G = nx.Graph()

  all_tags = all_tags_list()
  temp = []
  for e in dict_taglist.keys():
    tags = dict_taglist[e]
    for t in tags:
      temp.append((str(e)+"_"+t,{"year":e, "tag":t}))
  G.add_nodes_from(temp)
  plt.figure(figsize=(50,50))
  #pos = nx.spring_layout(G, k=1.5)

  pos = {}
  for e in temp:
    pos[e[0]] = ((e[1]["year"] - min_year)*1000, all_tags.index(e[1]["tag"])*100)

  nx.draw_networkx_nodes(G, pos, node_color='b', alpha=0.2, node_size=30, font_weight="bold", font_family='VL Gothic')
  nx.draw_networkx_labels(G, pos, fontsize=9)

  keys = list(dict_taglist.keys())
  b_tags = dict_taglist[keys[0]]
  for i in range(1,len(keys)):
    a_tags = dict_taglist[keys[i]]
    same_tags = b_tags & a_tags
    for s in same_tags:
      G.add_edge(str(keys[i-1])+"_"+s, str(keys[i])+"_"+s, weight=1)
    b_tags = a_tags

  print("debug")
  nx.draw_networkx_edges(G, pos, alpha=0.4, edge_color='r', width=2)
  plt.axis('off')
  plt.savefig(FILENAME_SAVEFIG)
  #plt.show()
  plt.close()



option = input("option:")

# words, tag, year
Flags = [False, False, False]

if option == "a":
  Flags = [True, True, True]
if option == "w":
  Flags[0] = True
elif option == "t":
  Flags[1] = True
elif option == "y":
  Flags[2] = True

if Flags[0]:
  print("create words_cloud")
  create_text_cloud(15)
if Flags[1]:
  print("create tag_cloud")
  create_tag_cloud()
if Flags[2]:
  print("create year_map")
  create_year_map()
