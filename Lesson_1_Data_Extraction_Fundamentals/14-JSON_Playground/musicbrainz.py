# To experiment with this code freely you will have to run this code locally.
# We have provided an example json output here for you to look at, 
# but you will not be able to run any queries through our UI. 
import json
import requests


BASE_URL = "http://musicbrainz.org/ws/2/"
ARTIST_URL = BASE_URL + "artist/"

query_type = {  "simple": {}, 
                "atr": {"inc": "aliases+tags+ratings"},
                "aliases": {"inc": "aliases"},
                "releases": {"inc": "releases"}}


def query_site(url, params, uid="", fmt="json"):
    params["fmt"] = fmt 
    r = requests.get(url + uid, params=params)
    print "requesting", r.url

    if r.status_code == requests.codes.ok:
        return r.json()
    else:
        r.raise_for_status()


def query_by_name(url, params, name):
    params["query"] = "artist:" + name
    return query_site(url, params)


def pretty_print(data, indent=4):
    if type(data) == dict:
        print json.dumps(data, indent=indent, sort_keys=True)
    else:
        print data


def main():
    # Question 1: HOW MANY BANDS NAMED "FIRST AID KIT"?
    print("Question 1") 
    results = query_by_name(ARTIST_URL, query_type["simple"], "FIRST AID KIT")
    count = 0 
    for artist in results["artists"]:
        if artist["name"].upper() == "FIRST AID KIT":
            count += 1
    print "Question: How many bands named FIRST AID KIT? Answer: %i.\n" % count

    # Question 2: BEGIN-AREA NAME FOR QUEEN?
    print("Question 2") 
    results = query_by_name(ARTIST_URL, query_type["simple"], "QUEEN")
    for artist in results["artists"]:
        if artist["name"].upper() == "QUEEN":
            begin_area_name = artist["begin-area"]["name"]
            break
    print "Question: BEGIN-AREA NAME FOR QUEEN? Answer: %s.\n" % begin_area_name

    # Question 3: SPANISH ALIAS FOR BEATTLES?
    print("Question 3") 
    results = query_by_name(ARTIST_URL, query_type["simple"], "BEATLES")
    for artist in results["artists"]:
        if artist["name"].upper() == "THE BEATLES":
            for alias in artist["aliases"]:
                if alias["locale"] == "es":
		    spanish_name = alias["name"]
		    break
            break
    print "Question: SPANISH ALIAS FOR BEATLES? Answer: %s.\n" % spanish_name

    # Question 4: NIRUANA DISAMBIGUATION?
    print("Question 4") 
    results = query_by_name(ARTIST_URL, query_type["simple"], "NIRVANA")
    for artist in results["artists"]:
        if artist["name"].upper() == "NIRVANA":
	    disambiguation = artist["disambiguation"]
            break
    print "Question: BEGIN-AREA NAME FOR QUEEN? Answer: %s.\n" % disambiguation


    # Question 5: WHEN WAS ONE DIRECTION FORMED?
    print("Question 5") 
    results = query_by_name(ARTIST_URL, query_type["simple"], "ONE DIRECTION")
    for artist in results["artists"]:
        if artist["name"].upper() == "ONE DIRECTION":
	    year = artist["life-span"]["begin"]
            break
    print "Question: BEGIN-AREA NAME FOR QUEEN? Answer: %s.\n" % year


if __name__ == '__main__':
    main()
