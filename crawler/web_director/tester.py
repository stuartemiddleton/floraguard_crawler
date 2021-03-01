import requests
from bs4 import BeautifulSoup
from crawler.web_director.parser import custom_parser
class MockPredict:

    def predict(self, a):
        return True


#wp = StackOverFlowWebpage(MockPredict())
# wp = custom_parser.create_custom_site("liberalforum.json")
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

soup = BeautifulSoup(requests.get("https://debatepolitics.com/members/ouch.37040/#recent-content",headers = headers).text, 'html.parser')
print(requests.get("https://debatepolitics.com/members/ouch.37040/#recent-content").text)

# blocks = soup.find_all(**wp.block_regex())

# print(blocks[0])
# for block in blocks:
#     user_name = None
#     user_link = None
#     for profile in block.find_all(**wp.profile_regex()):
#         user_name = profile.find(**wp.profile_name_regex())
#         user_link = profile.find(**wp.profile_link_regex())
#         if user_name and user_link is not None:
#             break
#     comment = block.find(**wp.comment_regex()).get_text()
#     print(comment)
#     print(user_name.get_text())
#     print(user_link['href'])

# soup = BeautifulSoup('<a class="username" href="./memberlist.php?mode=viewprofile&amp;u=23903">Unthinking Majority</a>','html.parser')
# user_link = soup.find('a')
# print(user_link)
# print(user_link['href'])

# Extracts all comment blocks and usernames
# soup = BeautifulSoup(requests.get("https://debatepolitics.com/members/nickyjo.28954/").text, 'html.parser')
#
# print(soup.find_all('span', class_= 'userTitle'))
#soup = BeautifulSoup(requests.get("https://debatepolitics.com/members/callen.36935/#about").text, 'html.parser')
# Extracts all comment blocks and usernames
# print(requests.get("https://debatepolitics.com/members/callen.36935/#about").text)
# print(soup.find_all('li', class_='is-active'))
# for x in soup.find_all('li', class_='is-active'):
#     print(x.get_text())
#print(soup.find_all('div', class_='grid--cell fl1'))
#print(soup.find_all('div', class_="user-details")[0].find('a' , href = True)['href'])

#
# x = WebpageHandler(1)
# x.process(requests.get("https://politics.stackexchange.com/users/35613/hamish-gibson").text, "https://politics.stackexchange.com/users/35613/hamish-gibson")