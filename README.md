## FloraGuard crawler

The FloraGuard crawler is designed to crawl online discussion forums and marketplaces connected to the illegal wildlife trade (IWT). It is build on top of the DARPA MEMEX undercrawler software (https://github.com/TeamHG-Memex/undercrawler) and includes configuration to define relevance patterns to help focus posts crawled.

This work was funded by the ESRC FloraGuard project (ES/R003254/1) and DEFRA Illegal Wildlife Trade Challenge Fund project (https://iwt.challengefund.org.uk/project/XXIWT114/). This is a mixed IPR repository with software created by University of Southampton (individually from FloraGuard project), and jointly created by University of Southampton and Royal Botanic Gardens, Kew (Illegal Wildlife Trade Challenge Fund project). The software copyright headers contain more details.

This software is released royalty-free under a 4-clause BSD open source license included in this repository.

Training material for legitimate IWT stakeholders and researchers can be obtained for free via a registration process setup by Royal Botanic Gardens, Kew (email TODO EMAIL FOR REGISTRATION).

This work can be cited as:

Middleton, S.E. Lavorgna, L. Neumann, G. Whitehead, D. Information Extraction from the Long Tail: A Socio-Technical AI Approach for Criminology Investigations into the Online Illegal Plant Trade, In 12th ACM Conference on Web Science (WebSci ’20 Companion), July 6–10, 2020, Southampton, United Kingdom. ACM, New York, NY, USA, 7 pages. https://doi.org/10.1145/3394332.3402838

Whitehead, D. Cowell, C.R. Lavorgna, A. Middleton, S.E. Countering plant crime online: Cross-disciplinary collaboration in the FloraGuard study, Forensic Science International: Animals and Environments, Volume 1, Elsevier, 2021. https://doi.org/10.1016/j.fsiae.2021.100007

Crawler has been tested on Win 10 and Ubuntu 20.04 LTS

# Installation
## Step 1. Install the prerequisites *
- [Java SE Development Kit 18](https://www.oracle.com/java/technologies/downloads/#jdk18-windows)
- [Apache Ant 1.10.14](https://ant.apache.org/bindownload.cgi)
- [Git](https://github.com/git-guides/install-git)
- [Anaconda](https://www.anaconda.com/download)
- [Python - If python not available on your computer](https://www.python.org/)
  - The version of python is recommended to be the latest stable version. If in doubt, recommended version: **3.9+**.

### Quick Installation for prerequisites

1) Install java, git and python (if previously not installed) to default locations (they will setup environment variables automatically)
2) Install ant to a known location e.g. c:\ant
3) Install anaconda to a known location e.g. c:\conda
4) WIN10 powershell - set environment variables for Apache ant and Anaconda using following commands (avoiding need for admin rights)
```
[Environment]::SetEnvironmentVariable("PATH", "{c:\ant}\apache-ant-1.10.12\bin", "User")
[Environment]::SetEnvironmentVariable("PATH", "{c:\conda}\condabin", "User")
```
* where value enclosed in {} is path to respective installation locations for Apache ant and Anaconda
5) Re-start the powershell for conda command to now be on the path
6) To display paths in windows powershell, run following command:
```
Get-ChildItem Env:
```

#### FOR MORE INSTALLATION INFORMATION: Look inside guides folder

_*Make sure you have added Apache Ant, Java & Python to your PATH._
_*Step by Step instructions_
## Step 2. Clone the repository & CD into it
```
#
# win10 - create folder <base-dir> using File Explorer, then open PowerShell (as administrator if your user account does not have permissions to install code)
# Ubuntu - open teminal window (or SSH in), then mkdir <base-dir>
#

cd <base-dir>
git clone https://github.com/stuartemiddleton/floraguard_crawler.git
cd focussed_crawler
```

## Step 3. Set up the environment & activate it
```

#
# win10
#

#Anaconda Powershell
mkdir /conda/pkgs
conda config --prepend pkgs_dirs /conda/pkgs
conda config --prepend envs_dirs /conda/envs
conda config --show
conda init powershell
conda env create --name floraguard --file environment.yml
conda activate floraguard

# environment.yml found in cloned repository
# use 'deactivate' to leave conda environment

#
# Ubuntu
# technote: for Ubuntu 18 scikit learn 0.24.1 or higher is needed to avoid UTF-8 decode error
#           https://stackoverflow.com/questions/65682019/attributeerror-str-object-has-no-attribute-decode-in-fitting-logistic-regre
#           twisted-iocpsupport==1.0.4 fails to compile under Ubuntu but can be removed
#           environment_ubuntu.yml has these changes in
#

sudo apt install dos2unix
dos2unix environment.yml
conda env create --name floraguard --file environment.yml
conda activate floraguard


# OLD
sudo apt install python3.8-venv
py -m venv ./env
py -m pip install --upgrade pip
py -m pip install wheel
sudo apt-get install libfreetype-dev
chmod +x ./env/bin/activate
source ./env/bin/activate
py -m pip install -r requirements.txt

# use 'deactivate' to leave virtual environment


```

## Step 4. Testing the crawler is set up correctly

Crawler scripts are in ./crawler/scripts
Crawler configuration files are in ./resources

Next we check website configuration is correct using the mock unicorn website. The script is run from ./crawler/scripts so the path parameter needs to go back two directories using the ../.. to find the crawler dir.

```
ant test.config -Dpath=../../resources/custom_webpages/mock_site.json -Dthread_url=https://sohaibkarous.wixsite.com/mock-unicorn/forum/general-discussions/unicorns-and-unee-products-for-sale 
```
If we see a message saying 'BUILD SUCCESSFUL' then the crawler is working.

# Configuring the crawler
There are **two types of configs** we are going to be talking about. 

First is the **website config**.  (**There are also two types of such confirgs: Forum and Marketplace.**)  This is the config that tells the crawler 
how to "understand" the website you intend to crawl in the future. 
That is, where every interesting block of information is 
located on that website (e.g. title, price, location, comments).
They are stored in `focussed_crawler/resources/custom_webpages`.

Second is the **run_config** which tells the crawler which one of those website configs you will be using at that time, 
as well as other parameters regarding how the crawler is set up, such as whether to use anonymisation or not. 
This one is located in `focussed_crawler/resources/run_configs/run_config.json`.

However, before we get to the Configs, we need to develop a search lexicon (or use an existing one).

## Developing the Search Lexicon
Keywords of relevance to the species of interest are compiled to form a search lexicon split into several sections. These will direct the AI search tools, and should include:
- **Species lexicon**: Latin names, Latin synonyms, common names, trade names. This selection may be informed by prior knowledge, or preliminary online searches. The algorithm cannon account for misspellings, and so spellings should be carefully checked, with common misspellings of species names intentionally added to the lexicon.
- **Behavioural terms lexicon**: These are predicate terms and indicate certain behaviour of interest. For example, a plant trade lexicon would include the following terms: buy; buy online; web buy; internet buy; order; sale; selling; purchase; live plant; swap.
- **Excluded terms lexicon**: This enables certain terms to be excluded from the searches (e.g., the term “seeds” could be excluded, to focus the search on the trade in live plants). Terms to exclude may only become apparent after some preliminary searches have been performed and can be added to this lexicon to help screen out unwanted content that is appearing in the data set. 
- **Entities of Interest lexicon**: This section of the lexicon can be used to search for specific entities of interest that emerge from initial rounds of searching. For instance, adding a certain vendor or platform name of interest to this lexicon, enables the AI tools to search for this specific entity within further rounds of searching, in addition to any other search lexicon terms.

The search lexicons are dynamic tools, that can be searched in different combinations, and updated and refined ahead of each round of searching. Example lexicons can be found in ```focussed_crawler\resources\lexicon```.
Multiple species can be included in a single search lexicon. This broadens the search and enables links between species of interest to be found more easily. The optimum number of species depends on the amount of data each is likely to return, and the amount of time available to analyse the data. Search lexicons ranging from one to a dozen species are recommended as the most likely to produce manageable size data sets.

_TIP: Coupled words do not need a “+” between them (e.g., Internet+buy should be written as Internet buy)._



## Website Config [FORUM]
Forums are configured according to the following criteria:

| Parameter name | Description |
| :---   | :--- | 
| “name” |  This can be anything, but must match your .json configuration file name.|
| “type” | Here, enter: “forum”.|
| “root_page_url” |  This is the main URL of the website you are crawling.|
| “general_threads_page_url” |  This is the URL within the website, that takes you to the forum page.|
| “general_threads_url” |  This is the part of the URL link common to all forum threads within the forum. Open a few threads to identify this section of the URL. This is the start location for the crawler.|
| “general_profile_url” |  If you are able to access forum user profiles, this is the part of the URL that is common to all of them, when clicked on and opened.|
| “thread_name_regex” | Use the Selection tool to hover over the title of a thread. The HTML code representing the name and class_ that relates the thread (and is common to all of them), need to be added to the configuration. E.g. “name” “div” : “Class_” : “forum_thread”.|
| “block_regex” |  For this section, hover over the entire block of the thread. Look for code that repeats within the HTML code. Ed nter the name and class details into the configuration file. |
| “comment_regex” |  This is the raw text of the forum post. Again, find the name and class_ details within the HTTP file, and add these to the configuration.|
| “profile_regex” |  This is the forum user’s profile information. Use the selection tool to select the ENTIRE block, and enter the “name” and “class_” information into the config. file.|
| “profile_name_regex” |  Here, select just the name from within the user profile.|
| “profile_link_regex” |  If available, select the profile owner’s link. This is usually represented by an “a” tag within the HTML, which signifies a link.|
| “date_regex” |  The date that the post was created, can be selected as it’s own separate block, and added to the configuration. This may appears along the lines of “name” : “time”, “class_” “x_yz”, etc.|
| “attributes_regex” |  Additional bespoke features of the forum can be captured using this function.| 


## Website Config [Marketplace]
Marketplaces are configured according to the following HTML blocks:

| Parameter name | Description                                                                                                                                            |
| :---   |:-------------------------------------------------------------------------------------------------------------------------------------------------------| 
| “name” | This can be anything, but must match your .json configuration file name.                                                                               |
| “type” | Here, enter: “marketplace”.                                                                                                                            |
| “root_page_url” | This is the first URL of the website you are crawling.                                                                                                 |
| “general_items_url” | This is the area of the website that you want the crawler to start from, for instance a specific menu or part of the website.                          |
| “general_item_url” | This is the part of the URL that is common to all listings when you open them. Open a few to see what repeats, and add this to the configuration file. |
| “sale_item_name_regex” | Within the item listing, this is the item name, which can be selected using the selection tool.                                                        |
 | "sale_item_description_regex" | Within the item listing, this is the descriptive text about the item.                                                                                  |
| “seller_name_regex” | Here, select just the seller’s name.                                                                                                                   |
| “seller_url_regex” | Here, select just the seller’s URL link.                                                                                                               |
| “seller_description_regex” | Here, this is the descriptive text about the seller.                                                                                                   |
| “price_regex” | Here, select the price.                                                                                                                                |
| “date_regex” | If available, here select the date that the item was first posted.                                                                                     |
| "review_block_regex" | If available, much like "block_regex" in forum config, get the repeating HTML tags for blocks of reviews for the item                                  |
|"review_username_regex"| If available, this is ther username of the reviewer                                                                                                    |
|"review_date_regex"| If avaialble, this is the date the review posted                                                                                                       |
|"review_title_regex"| If avaialble, this is the title for the review (OPTIONAL)                                                                                              |
|"review_description_regex"| If avaialble, this is the comment made by the reviewer                                                                                                 |
|"review_link_regex"| In this case, like the "profile_link_regex", find the <a> tag by the username of the reviewer or the link to the reviewer's page                       |
| “attributes_regex” | Additional bespoke features of the forum can be captured using this function.                                                                          | 

## Website configuration Tips
| Parameter name | Description |
| :---   | :--- | 
| “ “ | All URL/HTML codes entered into the configuration file should be encoded within inverted commas. These also enclose all other parts of website code, such as “name” and “class_”.|
| : ‘ | Colons and commas are used within the configuration file to separate HTML code entries – e.g., “name” : “div”, “class_” : “profile_name”,|
| { } | Brackets must be in place on line 1 and the final line of each website configuration. HTML codes for blocks with “regex” in the name, must also be enclosed within brackets { }.|
|“name” | This name refers to the name of the website being crawled. You can enter any name here, including code names, although it may be best to ensure that this matches the name of the configuration file itself, to help avoid confusion. This name will also be used when preparing the crawler via the run_config file.|
| “class_” | When used within configuration files, the term “class_” requires an underscore at the end of the word, as this would otherwise clash with other software commands.| 
| spaces | If the crawler build fails and the crawler will not run, check for any odd spaces within the HTML code that has been captured in the configuration file, and close any spaces that look odd or out of place. | 
| colours |  When your configuration file is correctly set up, the configuration file text will turn purple, the colons orange, URL/HTML entries green, and the brackets yellow and white. If there is something missing from the config. file, such as brackets on the first and closing lines, the entire text will appear green, indicating that there is a problem. (This is for standard PyCharm syntax highlighting| 
|Missing information | If the website you are crawling does not contain fields to fill all of the “regex” entries within the configuration files, these can be skipped and left blank, with only the brackets {}, in place. |

## The "run_config.json" 

| Parameter name          | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
|:------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------| 
| “name”                  | This is the website name that you defined in the webpage configuration file.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| “type”                  | Whether that website is a forum or a marketplace.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| “depth”                 | How far you want the crawler to explore the website. The bigger the number the further it explores. Note this expansion of the search is exponential e.g., depth = 1 -> 30 pages, depth = 2 -> 800 pages, depth = 3 -> 30,000 pages. **For most websites, a search depth of 7 or 8 is recommended. For the mock forum, which contains a small amount of data, a depth search of 100 can be used.**                                                                                                                                                                                         |
| “comment_model”         | The model needed for directing the crawler. **Leave it as “keyword”.**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| “thread_model”          | The model needed for directing the crawler. **Leave it as “all”**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| “filter_comments”       | “false” to capture all comments, or “true” to capture only interesting ones that relate to the keywords. **Leave as “true”.**                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| "ignore_reviews"         | "false" to ignore reviews for Marketplace items. "true" to capture reviews and use AI tool on reviews to find interesting items.                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| “comment_length”        | How many comments are needed before exporting? **Leave as 0.**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| “anonymous”             | This “hashes” (replaces with a numerical code) the usernames of all the individuals identified in the crawl. This important function enables crawls to screen out people’s names from the data that is captured, in instances where this type of sensitive personal data is not required for data analysis. The entry here answers a question posed by the algorithm – should data be anonymous or not? Therefore, set to **true** if you want to capture anonymous data (i.e. personal data hashed), and set to **false** if you want the crawl to capture all personal data, unfiltered. |
| “use_comment_file”      | This directs the algorithm to use the search lexicon files. Set to true to use existing lexicon files, or false to create your own. **Leave as true.**                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| “comment_keyword_names” | This is where you **input the file names of the lexicons that you have created.** For instance, entering Unicorns.txt would direct the algorithm to make use of the search lexicon saved under this name. More than one lexicon can be entered, including those for excluded terms and lexicons containing additional information added after preliminary crawling and analysis.                                                                                                                                                                                                           |
| "thread_keyword"        | This is where a custom lexicon for searching forum thread titles only can be entered. **Leave as {}**.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| "timeout_hours"         | This is the specified timeout for the crawler. Advised to use this to run the crawler for a specific amount of hours. To run indefinetly, set to NONE or do not inclue.                                                                                                                                                                                                                                                                                                                                                                                                                    |

# Running the crawler
Once you set up the config for the website you want to crawl and updated the run_config and checked you are withing the environment we created earlier, 
running the crawler is as simple as running ``` ant crawl ``` in your terminal.

```
ant crawl
```

# Reviewing the captured data
Once the crawl has finished, two files will be saved to ```focussed_crawler\resources\exported_users``` (if anything of relevance to the keywords has been identified). These files are termed “interesting users_XXXX”, with the XXXX replaced with whatever name you gave the website in the configuration file.
One is an excel document (.csv) containing all the important information that was crawled from the website. The other is a .json file containing the crawled HTML data. 

The excel document displays key data from each online post captured by the crawler, such as online user identify (unless hashed), relevant comments, time, date etc. 

The .json file has columns representing which keyword from the lexicon it found in the comment to trigger the export. For instance, in the example below, the key words `Conophytum’ (from the `Plants’ lexicon) and `buy’ (from the `Trade Words’ lexicon).

Both the .csv and .json files can be combined with other analysis tools for further exploration.

```
#
# win10
#

dir resources\exported_users
type resources\exported_users\interesting_users_mocked.json

#
# ubuntu
#

ls -la resources/exported_users
cat resources/exported_users/interesting_users_mocked.json
```

# Visualisation
Once the crawl is completed we parse data and then visualise

```
# parse and visualize mocked forum
ant parse.crawled-data -Ddata=../../resources/exported_users/interesting_users_mocked.json
cp resources/exported_users/parsed_data.json resources/exported_users/parsed_data_mocked.json
ls -la resources/exported_users/parsed_data_mocked.json

ant viz -Dconfig=../../config/viz_config.ini -Ddata-graph=../../resources/exported_users/parsed_data_mocked.json
cp build/bin/viz.png build/bin/viz_mocked.png
ls -la build/bin/viz_mocked.png

# parse and visualize ebay marketplace
ant parse.crawled-data -Ddata=../../resources/exported_users/interesting_users_ebay.json
cp resources/exported_users/parsed_data.json resources/exported_users/parsed_data_ebay.json
ls -la resources/exported_users/parsed_data_ebay.json

ant viz -Dconfig=../../config/viz_config.ini -Ddata-graph=../../resources/exported_users/parsed_data_ebay.json
cp build/bin/viz.png build/bin/viz_ebay.png
ls -la build/bin/viz_ebay.png
```

## Configuration of visualization

The configuration is contained in an INI file whose location is passed as a command line parameter. Hyperparameters described below.

```
search_depth = graph depth of connection to display e.g. 2

list_direction = list of allowed directions of graph walk e.g. ['forward','backward']

layout_name = networkx layout type e.g. spring, random, spectral or shell

max_nodes = limit for number of nodes in visual graphs to avoid long render times e.g. 500

filter_post_freq = optional minimum post/thread frequency count for nodes (can be None) e.g. None

colour_map = dict of node category and node colour

entity_prefix_map = dict of entity prefixes to identify node category

list_pseudonymization = list of entity types that should be pseudonymized e.g. []
```

Within the configuration INI file there are entity pattern specs to allow selection of
(a) graph root nodes (b) nodes to belong to a cluster (c) nodes to allow in the graph.
These all use the entity pattern spec structure described below. For (a) and (b) matching nodes
will be included in the root or cluster node list. For (c) matching nodes will be included in
a filter list and removed from the graph.

```
{
	# positive entity pattern to match a set of nodes
	'match' : {
			# list of entity prefixes in format of <type>:<name>.
			# <type> can be '?' to allow any type. <type> and <name> can include a wildcard '*' at the start or end of a partial string to be matched.
			'entity' : [ 'NER-*' ],

			# min and max entity connection freq within entity index. note this is the global connection freq before the target node graph walk.
			# If entity freq is > max or < min then pattern is not matched. Default is None.
			'entity_freq_range' : { 'max' : 100, 'min' : 30 },
		},

	# negative entity pattern to ensure some nodes are never matched
	'avoid' : {
			# list of entity prefixes in format of <type>:<name>.
			# <type> can be '?' to allow any type. <type> and <name> can include a wildcard '*' at the start or end of a partial string to be matched.
			'entity' : [ 'NER-PERSON:*', 'NER-PLANT:*', 'NER-LOCATION:*', 'NER-CITY:*', 'NER-STATE_OR_PROVINCE:*', 'NER-COUNTRY:*', 'NER-NATIONALITY:*', 'NER-ORGANIZATION:*'],

			# min and max entity connection freq within entity index. note this is the global connection freq before the target node graph walk.
			# If entity freq is > max or < min then pattern is not matched. Default is None.
			'entity_freq_range' : None,
		},
}
```

## Data graph JSON structure

The intelligence graph visualization expects a data graph in the following format. This will usually be
programmatically generated from a combination of a [web crawler](https://github.com/darpa-i2o/memex-program-index), [parser](https://docs.python.org/3/library/html.parser.html)
and named entity tagger such as [Stanford CoreNLP](https://stanfordnlp.github.io/CoreNLP/).

```
{
  <website>_thread_<thread_id>_post_<post_id>: {
    "author": <author_name>,
    "page_url": <post_uri>,
    <sentence_index>: [
      {
        "entity": [
          <NER-label>:<phrase>,
          <NER-label>:<phrase>,
          ...
        ]
      }
    ],
    <sentence_index>: [
      {
        "entity": [
          <NER-label>:<phrase>,
          <NER-label>:<phrase>,
          ...
        ]
      }
    ],
    ...
  },
  <website>_thread_<thread_id>_post_<post_id>: {
    "author": <author_name>,
    "page_url": <post_uri>,
    <sentence_index>: [ ... ],
    ...
  }
}

The post identifier uses the naming convention of "<website>_thread_<thread_id>_post_<post_id>". The thread
and post identifier will be parsed from this name pattern and used to provide conversation post/thread nodes
in the final visualization.

The <sentence_index> is a global index used to tie entities to a specific conversational context. This
avoids graphs connecting named entity mentions using the same term in an unrelated conversational context.

The <NER-label> will be generated by the NER tagger. For Stanford CoreNLP named entity tags include
NER-PERSON, NER-LOCATION, NER-CITY, NER-STATE_OR_PROVINCE, NER-COUNTRY, NER-NATIONALITY,
NER-ORGANIZATION etc.

```

