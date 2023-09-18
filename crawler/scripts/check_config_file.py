"""
    Script used to test whether the specified tags return correct values
    arg[1] = name of website
    arg[2] = link to thread
    arg[3] = link to profile
"""
import sys
import requests
from bs4 import BeautifulSoup
import random
import json


def create_custom_site(path):
    with open(path) as json_file:
        data = json.load(json_file)
        return data

if __name__ == '__main__':
    if len(sys.argv) < 3:
        raise Exception("Please input parameters\n1 - Path to config\n2 - Link to thread")
    path = sys.argv[1]
    thread_url = sys.argv[2]
    print(thread_url)
    # Creating object based on config
    site = create_custom_site(path)
    print("===================Testing configuration on thread===================")
    people = []
    page = requests.get(thread_url).text
    #soup = BeautifulSoup(page, 'html.parser',from_encoding='utf-8')
    soup = BeautifulSoup(page, 'html.parser')
    block_list = soup.find_all(**site['block_regex'])
    print("Identified " + str(len(block_list)) + " blocks ")
    for block in block_list:
        print("Identified block " + repr(block.name) + " with class " + repr(block['class']))

        user_name = None
        user_link = None

        for profile in block.find_all(**site['profile_regex']):
            print("Identified profile " + repr(profile.name) + " with class " + repr(profile['class']))

            user_name = profile.find(**site['profile_name_regex'])
            user_link = profile.find(**site['profile_link_regex'])
            if user_name and user_link is not None:
                break
        comment = block.find(**site['comment_regex']).get_text()
        if user_name is not None and user_link is not None:
            people.append((user_name,user_link,comment))
    random.shuffle(people)
    print("Identified",len(people),"comments")

    if len(block_list) > 0:
        print("Found blocks ok")
    else:
        print("Check tags, seemed to found no blocks")
        print("===================FAILURE ON THREAD===================")
        quit()
    if len(people) > 0:
        print("Found people ok")
        print("Example name:", people[0][0].text)
        print("Example link:", people[0][1]['href'])
        print("Example comments:", people[0][2].strip())
        print("===================SUCCESS ON THREAD===================")
    else:
        print("Check tags, seemed to found no people")
        print("===================FAILURE ON THREAD===================")
        quit()