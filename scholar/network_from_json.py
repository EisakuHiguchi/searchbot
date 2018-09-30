# -*- coding: utf-8 -*-

import os
import json
import collections
import itertools
import networkx as nx
import matplotlib.pyplot as plt
from datetime import datetime
import argparse

import format_json


def get_filename_savefig(filename_json):
  nowtime = datetime.now().strftime("%Y-%m-%d_%H%M%S")
  return nowtime + "_" + os.path.basename(filename_json).split(".")[0]

def all_tags_list(filename_json):
  taglist = []
  jsonData = format_json.loadjson(filename_json)
  for key in jsonData.keys():
    taglist.append(jsonData[key]["tags"])
  tag_count = collections.Counter(itertools.chain.from_iterable(taglist))
  tag_most = tag_count.most_common()
  
  result = []
  for e in tag_most:
    result.append(e[0]) 
  return result

def add_edges(G, taglist):
  for tags in taglist:
    for tag0, tag1 in itertools.combinations(tags, 2):
      if not G.has_node(tag0) or not G.has_node(tag1):
        continue
      if G.has_edge(tag0, tag1):
        G[tag0][tag1]["weight"] += 1
      else:
        G.add_edge(tag0, tag1, weight=1)
  return G

def define_plt_pram(G):
  plt.figure(figsize=(15,15))
  pos = nx.spring_layout(G, k=1.5)

  node_size = [ d['count']*50 for (n,d) in G.nodes(data=True)]
  nx.draw_networkx_nodes(G, pos, node_color='b', alpha=0.2, node_size=node_size, font_weight="bold", font_family='VL Gothic')
  nx.draw_networkx_labels(G, pos, fontsize=14)

  edge_width = [ d['weight']*0.5 for (u,v,d) in G.edges(data=True)]
  nx.draw_networkx_edges(G, pos, alpha=0.4, edge_color='r', width=edge_width)


def plot_save_nx(G, filename_plot):
  plt.axis('off')
  plt.savefig(filename_plot)
  #plt.show()
  plt.close()
  G.clear()

def create_tag_cloud(prm, filename_json):
  jsonData = format_json.loadjson(filename_json)
  taglist = [] 
  for key in jsonData.keys():
    taglist.append(jsonData[key]["tags"])
  tag_count = collections.Counter(itertools.chain.from_iterable(taglist))
  deltemp = tag_count.most_common(1)
  tag_count.pop(deltemp[0][0])

  G = nx.Graph()
  if prm == 0:
    G.add_nodes_from([(tag, {"count":count}) for tag, count in tag_count.most_common()])
  else:
    G.add_nodes_from([(tag, {"count":count}) for tag, count in tag_count.most_common(prm)])
  G = add_edges(G, taglist)
  define_plt_pram(G)

  filename_plot = get_filename_savefig(filename_json) + "_CLOUD"
  plot_save_nx(G, filename_plot)

def remove_lesswords(listdata):
  temp = []
  for e in listdata:
      if len(e) > 3:
        temp.append(e.lower().replace(",","").replace(".",""))
  return temp

def create_text_cloud(prm, filename_json, prm_least_flag = False):
  jsonData = format_json.loadjson(filename_json)
  taglist = [] 
  
  for key in jsonData.keys():
    taglist.append(remove_lesswords(jsonData[key]["summary"].split(" ")))
    taglist.append(remove_lesswords(jsonData[key]["title"].split(" ")))
    taglist.append(jsonData[key]["tags"][1:])
  
  tag_count = collections.Counter(itertools.chain.from_iterable(taglist))
  G = nx.Graph()
  listlen = len(tag_count.most_common())
  
  if prm_least_flag:
    G.add_nodes_from([(tag, {"count":count}) for tag, count in tag_count.most_common()[-prm:]])
  else:
    G.add_nodes_from([(tag, {"count":count}) for tag, count in tag_count.most_common(prm)])
  
  G = add_edges(G, taglist)
  define_plt_pram(G)

  filename_plot = get_filename_savefig(filename_json) + "_WORDS_CLOUD"
  plot_save_nx(G, filename_plot)


def create_year_map(filename_json):
  jsonData = format_json.loadjson(filename_json)
  taglist = []
  for key in jsonData.keys():
    temp = jsonData[key]["tags"]
    year = jsonData[key]["year"][-4:]
    if year != "None":
      temp.append(int(year))
      taglist.append(temp)
    
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
    if min_year > e[-1]:
      min_year = e[-1]

  tag_count = collections.Counter(itertools.chain.from_iterable(taglist))
  main_tag = tag_count.most_common(2)[1][0]

  G = nx.Graph()

  all_tags = all_tags_list(filename_json)
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
  
  nx.draw_networkx_edges(G, pos, alpha=0.4, edge_color='r', width=2)
  filename_plot = get_filename_savefig(filename_json)
  plot_save_nx(G, filename_plot)
  

# ---- ----
# main

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument('Filename', metavar='F', type=str, nargs='+',help='Filename for saving data')
  parser.add_argument("-w", "--words", type=bool, default=False)
  parser.add_argument("-wp", "--wordprm", type=int, default=15)
  parser.add_argument("-t", "--tags", type=bool, default=True)
  parser.add_argument("-tp", "--tagprm", type=int, default=0)
  parser.add_argument("-y", "--years", type=bool, default=False)
  args = parser.parse_args()

  filename_json = args.Filename[0]

  if args.words:
    print("create words_cloud:" + str(args.wordprm))
    create_text_cloud(args.wordprm, filename_json)
  if args.tags:
    if args.tagprm == 0:
      print("create tag_cloud: all")
    else:
      print("create tag_cloud:" + str(args.tagprm))
    
    create_tag_cloud(args.tagprm, filename_json)
  if args.years:
    print("create year_map")
    create_year_map(filename_json)
