# coding: utf-8
import nltk
import argparse

import format_json


symbols = ["'", '"', "`", ".", ",", "-", "|", "?", ":", ";", "(", ")", '“', '”', '…']
exclude_list = ["IN", "RB"]
stopwords = nltk.corpus.stopwords.words("english")


def auto_tagging(jsondata):
    for key in jsondata.keys():
        sentence = jsondata[key]["summary"]
        token = nltk.word_tokenize(sentence)
        text = nltk.Text(token)
        fdist = nltk.FreqDist(w.lower() for w in text if w.lower() not in stopwords + symbols)
        tagged = nltk.pos_tag(fdist)
        temp = [w[0] for w in tagged if w[1] not in exclude_list]
        jsondata[key]["tags"] = temp
    return jsondata


# ---- ----
# main

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('Filename', metavar='F', type=str, nargs='+',help='Filename for saving data')
    args = parser.parse_args()

    FILENAME_JSON = args.Filename[0]
    jsondata = format_json.loadjson(FILENAME_JSON)

    jsondata = auto_tagging(jsondata)
    format_json.savejson_dict(jsondata, FILENAME_JSON)
