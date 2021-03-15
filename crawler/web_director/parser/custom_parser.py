from web_director.impl.CustomWebpage import CustomWebpage
from web_director.impl.reference.AllModel import AllModel
from web_director.impl.reference.ContainsKeywordModel import ContainsKeywordModel
from web_director.impl.reference.PositiveSentimentModel import CommentsPositiveSentiment
import os
import json
# //                          "2": ["buy",
# //                            "sell",
# //                            "seeds",
# //                            "sale",
# //                            "selling",
# //                            "purchase",
# //                            "live plant",
# //                            "swap"]

def read_config():
    path = r"..\crawler\web_director\run_config.json"
    with open(path) as f:
        data = json.load(f)
    return data


def create_custom_site(config):
    print("Searching for custom sites")
    name = config["name"]
    path = r"..\crawler\web_director\parser\custom_webpages"
    for file in os.listdir(path):
        with open(path + "\\" + file) as json_file:
            data = json.load(json_file)
            if data["name"] not in name:
                continue
            webpage = CustomWebpage(data["name"], config["anonymous"])
            webpage.root_page_url = data["root_page_url"]
            webpage.general_profile_url = data["general_profile_url"]
            webpage.general_threads_page_url = data["general_threads_page_url"]
            webpage.general_thread_url = data["general_thread_url"]
            webpage._thread_name_regex = data["thread_name_regex"]
            webpage._block_regex = data["block_regex"]
            webpage._comment_regex = data["comment_regex"]
            webpage._profile_regex = data["profile_regex"]
            webpage._profile_name_regex = data["profile_name_regex"]
            webpage._profile_link_regex = data["profile_link_regex"]
            webpage._attributes_regex = data["attributes_regex"]
            print("Created web_director, returning result")
            return webpage

    raise Exception("Cannot find custom site")


def get_comment_model(data):
    name = data["comment_model"]
    if name == "sentiment":
        print("Loaded " + name + " model")
        return CommentsPositiveSentiment()
    if name == "keyword":
        print("Loaded " + name + " model")
        print("Comment regex " + text_to_regex(data["comment_keyword"]))
        return ContainsKeywordModel(text_to_regex(data["comment_keyword"]))
    if name == "all":
        print("Loaded " + name + " model")
        return AllModel()
    else:
        raise Exception("Model not defined")


def get_thread_model(data):
    name = data["thread_model"]
    if name == "keyword":
        print("Loaded " + name + " model")
        print("Thread regex " + (data["thread_keyword"]))
        return ContainsKeywordModel(data["thread_keyword"])
    if name == "all":
        print("Loaded " + name + " model")
        return AllModel()
    else:
        raise Exception("Model not defined")

def text_to_regex(dict):
    regex = r"(?i).*"
    for _,v in dict.items():
        for i in range(0,len(v)):
            if i == 0:
                regex += r"( "+v[i]
            regex += r"| "+v[i]
        regex += r").*"
    return regex

