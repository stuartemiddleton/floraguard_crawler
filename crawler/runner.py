import os
from web_director.parser.custom_parser import create_custom_site, read_config, text_to_regex
def main():
    data = read_config()
    web = create_custom_site(data)
    os.system("py -m scrapy crawl undercrawler -a url=" + web.get_general_start_page_url() + " -s DEPTH_LIMIT=" + str(data["depth"]))


if __name__ == '__main__':
    main()
