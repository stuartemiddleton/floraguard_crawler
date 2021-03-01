from bs4 import BeautifulSoup
import re
import xlwt
import pandas as pd


# Global mappings
user_to_all_comments = {}
bias_to_comment={}

"""

Takes the URL body and parses for commenter and comment
Made specifically for debate politics

TODO generalise this

"""
def extract_data_debatepolitics(html):
    soup = BeautifulSoup(html,'html.parser')
    # Extracts all comment blocks and usernames
    for x in soup.find_all('div',class_="message-userContent lbContainer js-lbContainer"):
        # Extracts usernames
        user_name = x.get("data-lb-caption-desc").split("·")[0].rstrip()


        # Extracting comments
        # Filters out unimportant information
        remove_expand = str(x.find('div',class_="bbCodeBlock-expandContent"))
        remove_link = str(x.find('div',class_="bbCodeBlock-expandLink"))
        remove_title = str(x.find('div',class_="bbCodeBlock-title"))
        comment = str(x.find('div', class_="bbWrapper")).replace(remove_expand, "").replace(remove_link,"").replace(remove_title,"")

        # Converts to raw string
        comment = pretty(BeautifulSoup(comment, 'html.parser'))

        if user_name not in user_to_all_comments:
            user_to_all_comments[user_name] = [None,[comment]]
        else:
            if comment not in user_to_all_comments[user_name][1]:
                user_to_all_comments[user_name][1].append(comment)

    # Extracting any contextual info that can be useful
    for x in soup.find_all('section',class_="message-user"):
        contextual_info = x.find_all('dd')
        # Tag for political leaning
        user_name = pretty(x.find("h4",class_="message-name"))
        political_leaning = pretty(contextual_info[len(contextual_info)-1])
        user_to_all_comments[user_name][0] = political_leaning

def pretty(string):
    return re.sub(' +',' ',string.get_text().replace('\n', ' ').replace('\r', '').replace('\t','')).rstrip().lstrip()


def extract():
    for user_name,political_and_comments in user_to_all_comments.items():
        if political_and_comments[0] not in bias_to_comment:
            bias_to_comment[political_and_comments[0]] = political_and_comments[1]
        else:
            bias_to_comment[political_and_comments[0]] += political_and_comments[1]

    pd.DataFrame.from_dict(user_to_all_comments).to_csv(r'C:\\Users\\Sohaib Karous\\Desktop\\University of SOTON Course\\Comp sci notes\\Diss\\crawlers\\undercrawler\\extracted_data\\users_comments_big_clean.csv',index = False)
    pd.DataFrame(dict([ (k,pd.Series(v)) for k,v in bias_to_comment.items() ])).to_csv(r'C:\\Users\\Sohaib Karous\\Desktop\\University of SOTON Course\\Comp sci notes\\Diss\\crawlers\\undercrawler\\extracted_data\\bias_comments_big_clean.csv',index = False)
