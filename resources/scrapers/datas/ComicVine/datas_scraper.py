# -*- coding: UTF-8 -*-

import re
import os
import urllib
import simplejson

comicvine_api_key = "a1aaa516eaf233abf29c8aefaa46dc39cc0f0873"
comicvine_api_url = "http://beta.comicvine.com/api"

def _get_games_list(search):
    results = []
    display = []
    try:
        f = urllib.urlopen('http://www.comicvine.com/search/?indices[0]=cv_issue&q="'+urllib.quote(search.lower())+'"')
        page = f.read().replace('\r\n', '').replace('\n', '').strip('\t')
        issues = re.findall('/4000-(.*?)/">        <div class="img imgflare">                      <img src="(.*?)" alt="(.*?)">                  </div>        <h3 class="title">          (.*?)        </h3>        <p class="specs icon icon-tags">          <span class="type"><span class="search-company">(.*?)</span> <span class="search-type">issue</span> <span class="search-publish-date">\((.*?)\)</span>', page)
        for issue in issues:
            comic = {}
            comic["id"] = issue[0]
            comic["title"] = unescape(issue[2])
            comic["studio"] = issue[4]
            comic["release"] = issue[5][-4:]
            comic["order"] = 1
            comic_volume = comic["title"].split(' - ')
            if ( comic_volume[0].lower() == search.lower() ):
                comic["order"] += 1
            if ( comic["title"].lower() == search.lower() ):
                comic["order"] += 1
            if ( comic["title"].lower().find(search.lower()) != -1 ):
                comic["order"] += 1
            results.append(comic)
        results.sort(key=lambda result: result["order"], reverse=True)
        for result in results:
            display.append(result["title"].encode('utf-8','ignore')+' ('+result["studio"].encode('utf-8','ignore')+' / '+result["release"].encode('utf-8','ignore')+')')
        return results,display
    except:
        return results,display
        
# Return 1st Comic search
def _get_first_game(search,gamesys):
    results,display = _get_games_list(search)
    return results

# Return Comic data
def _get_game_data(comic_id):
    comicdata = {}
    comicdata["genre"] = "Comic"
    comicdata["release"] = ""
    comicdata["studio"] = ""
    comicdata["plot"] = ""
    try:
        f = urllib.urlopen(comicvine_api_url+'/issue/'+comic_id+'/?api_key='+comicvine_api_key+'&format=json&field_list=cover_date,description,volume,name,issue_number')
        json = simplejson.loads(f.read())
        f.close()
        if ( json['results']['cover_date'] ):
            comicdata["release"] = str(json['results']['cover_date'])[0:4]
        if ( json['results']['description'] ):
            p = re.compile(r'<.*?>')
            comicdata["plot"] = p.sub('', unescape(json['results']['description'].encode('utf-8','ignore')))
        if ( json['results']['volume'] ):
            f = urllib.urlopen(comicvine_api_url+'/volume/'+str(json['results']['volume']['id'])+'/?api_key='+comicvine_api_key+'&format=json&field_list=publisher')
            json2 = simplejson.loads(f.read())
            f.close()
            if ( json2['results']['publisher'] ):
                comicdata["studio"] = str(json2['results']['publisher']['name']).encode('utf-8','ignore')
        return comicdata
    except:
        return comicdata

def unescape(s):
    s = s.replace('</p>',' ')
    s = s.replace('<br />',' ')
    s = s.replace("&lt;", "<")
    s = s.replace("&gt;", ">")
    s = s.replace("&amp;", "&")
    s = s.replace("&#039;","'")
    s = s.replace('<br />',' ')
    s = s.replace('&quot;','"')
    s = s.replace('&nbsp;',' ')
    s = s.replace('&#x26;','&')
    s = s.replace('&#x27;',"'")
    s = s.replace('&#xB0;',"°")
    return s
