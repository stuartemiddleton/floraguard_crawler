# !/usr/bin/env python
# -*- coding: utf-8 -*-

######################################################################
#
# (c) Copyright University of Southampton, 2022
# # Copyright in this software belongs to University of Southampton,
# Highfield, University Road, Southampton SO17 1BJ
#
# Created By : Sohaib Karous
# Created Date : 2022/08/18
# Project : FloraGuard
# ######################################################################

import os
from web_director.parser.custom_parser import create_custom_site, read_config, text_to_regex
def main():
    data = read_config()
    web = create_custom_site(data)
    os.system("python -m scrapy crawl undercrawler -a url=" + web.get_general_start_page_url() + " -s DEPTH_LIMIT=" + str(data["depth"]) )

if __name__ == '__main__':
    main()
