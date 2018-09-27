# searchbot
support searching tasks

----

## scholar

### module_scraping.py

This program is using for scraping data that research paper informations of a Google Scholar page.
The difference of *search_with_slenium.py* is that this program can scrape one Google Scholar page result.
For example, when you want to get scraping data that a now opened page, you use this programm.

#### requires

+ requests
+ beautifulsoup4
+ **lxml**

```
pip install request beautifulsoup4 lxml
```

#### usage

Require 2 arguments -Filename, URL-.
For example...

```
python module_scraing.py "http://sample...." "samplefile" 
```

May require to use double quote depending on CLI.

If you execute above command, geting a file that is named sample.json.
This file is formatted by same format that program *search_with_selenium.py*.

So, you can append this data created by *module_scraping.py* to existing data. 


### re_index.py

This program replaces same ids to sanity ids.
If you want to marge other scraping data, you can use this program.

#### usage

Require one argument Filename. The filename is json foramt, so filename is like "hogehoge.json".
For example...

```
python re_index.py "hogehoge.json"
```

NOTE: This progam makes temp file that is named *temp_reindex.json*. This file is gavege. 


----

