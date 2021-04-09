from web_director.impl.CustomWebpage import CustomWebpage
from web_director.impl.CustomMarketPlace import CustomMarketPlace

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
from web_director.web_handler.WebpageHandler import WebpageHandler


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
            if config["type"] == "forum":
                webpage = CustomWebpage(data["name"])
                webpage.root_page_url = data["root_page_url"]
                webpage.general_profile_url = data["general_profile_url"]
                webpage.general_start_page_url = data["general_threads_page_url"]
                webpage.general_thread_url = data["general_thread_url"]
                webpage._thread_name_regex = data["thread_name_regex"]
                webpage._block_regex = data["block_regex"]
                webpage._comment_regex = data["comment_regex"]
                webpage._profile_regex = data["profile_regex"]
                webpage._profile_name_regex = data["profile_name_regex"]
                webpage._profile_link_regex = data["profile_link_regex"]
                webpage._date_regex = data["date_regex"]
                webpage._attributes_regex = data["attributes_regex"]
                print("Created web_director, returning result")
                return webpage
            if config["type"] == "marketplace":
                webpage = CustomMarketPlace(data["name"])
                webpage.root_page_url = data["root_page_url"]
                webpage.general_start_page_url = data["general_items_url"]
                webpage.general_item_url = data["general_item_url"]
                webpage._sale_item_name_regex = data["sale_item_name_regex"]
                webpage._seller_name_regex = data["seller_name_regex"]
                webpage._seller_description_regex = data["seller_description_regex"]
                webpage._seller_url_regex = data["seller_url_regex"]
                webpage._date_regex = data["date_regex"]
                webpage._price_regex = data["price_regex"]
                webpage._seller_block_regex = data["seller_block_regex"]
                webpage._attributes_regex = data["attributes_regex"]
                print("Created web_director, returning result")
                return webpage

    raise Exception("Cannot find custom site")


def get_comment_model(data):
    name = data["comment_model"]
    if name == "sentiment":
        print("Loaded " + name + " model")
        return CommentsPositiveSentiment(comment_length=1)
    if name == "keyword":
        print("Loaded " + name + " model")
        if data['use_comment_file']:
            # print("Comment regex " + read_txt(data["comment_keyword_names"]))
            return ContainsKeywordModel(read_txt(data["comment_keyword_names"]), comment_length=data["comment_length"])
        else:
            # print("Comment regex " + text_to_regex(data["comment_keyword"]))
            return ContainsKeywordModel(text_to_regex(data["comment_keyword"]), comment_length=data["comment_length"])
    if name == "all":
        print("Loaded " + name + " model")
        return AllModel()
    else:
        raise Exception("Model not defined")


def get_thread_model(data):
    name = data["thread_model"]
    if name == "keyword":
        print("Loaded " + name + " model")
        # print("Thread regex " + text_to_regex(data["thread_keyword"]))
        return ContainsKeywordModel(text_to_regex(data["thread_keyword"]), comment_length=data["comment_length"])
    if name == "all":
        print("Loaded " + name + " model")
        return AllModel()
    else:
        raise Exception("Model not defined")


def create_webpage_handler():
    data = read_config()
    webpage_handler = WebpageHandler(create_custom_site(data),
                                     get_thread_model(data),
                                     get_comment_model(data),
                                     data["filter_comments"], data["anonymous"])
    return webpage_handler


def text_to_regex(dict):
    regex = r"(?i)"
    for _, v in dict.items():
        for i in range(0, len(v)):
            if i == 0:
                regex += r"(?=.*\b" + v[i]
            regex += r"|.*\b" + v[i]
        regex += r").*"
    return str(regex.encode("utf-8"))


def read_txt(paths):
    regex = r"(?i)"
    for path in paths:
        with open("../crawler/web_director/lexicon/" + path, encoding='utf-8') as f:
            lines = f.readlines()
            if "excluded_terms" in path:
                print("Excluding words in " + str(path))
                for i in range(0, len(lines)):
                    if i == 0:
                        regex += r"(?!^.*\b" + lines[i].strip() + r"\b"
                    else:
                        regex += r"|^.*\b" + lines[i].strip() + r"\b"
                regex += r")"
            else:
                for i in range(0, len(lines)):
                    if i == 0:
                        regex += r"(?=^.*\b" + lines[i].strip() + r"\b"
                    else:
                        regex += r"|^.*\b" + lines[i].strip() + r"\b"
                regex += r")"
    regex += r".*"
    return regex.encode("utf-8").decode()