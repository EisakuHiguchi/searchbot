import format_json
import argparse

def convert_sameid(filename):
    f = open(filename, "r")
    str_temp = f.read()
    f.close()

    tar_s = "\"id_"
    tar_e = "\""
    indexer = 1
    r_index = 1
    while True:
        cnt_same = str_temp.count("\"id_" + str(indexer) + "\"")
        if cnt_same < 1:
            print("same id nothing?")
            break
        elif cnt_same == 1:
            # next index
            indexer += 1
        else:
            target = tar_s + str(indexer) + tar_e
            idx_replace = str_temp.rindex(target)
            str_temp = str_temp[:idx_replace+1] + "id_r" + str(r_index) + str_temp[idx_replace+len(target)-1:]
            r_index += 1
    return str_temp



# ---- ----
# main

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('Filename', metavar='F', type=str, nargs='+',help='Filename for saving data')
    args = parser.parse_args()

FILENAME = args.Filename[0]

str_temp = convert_sameid(FILENAME)
f = open("temp_reindex.json", "w")
f.write(str_temp)
f.close()

jsonData = format_json.loadjson("temp_reindex.json")
dict_temp = {}
re_id = 1
for key in jsonData.keys():
    dict_temp["id_" + str(re_id)] = jsonData[key]
    re_id += 1

format_json.savejson_dict(dict_temp, FILENAME)
