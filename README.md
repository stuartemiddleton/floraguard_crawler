Ogie focussed crawler

# Running the crawler
Before you get to this step ensure that you have 

- Git installed
- Python 3.7
- Apache ant

First step is clone the repo then CD into the repo

```
git clone https://git.soton.ac.uk/ogie/focussed_crawler.git
cd focussed_crawler
```

Following this we set up our environment and activate it
```
# win10 powershell users only (allow scripts to run)
Set-ExecutionPolicy -Scope CurrentUser Unrestricted

# make a new env folder (to store downloaded libraries etc)
py -m venv env

# upgrade pip (needed for cryptography install)
py -m pip install --upgrade pip

# activate env
.\env\Scripts\activate

# install all prerequisites to env
py -m pip install -r requirements.txt
```

The configuration of the crawler is located in ```../web_directory``` ensure that the name is 'mocked'. If you want to add any further websites they should be placed in ```../web_directory/parser/custom_webpages```

Next we check website configuration is correct

```
ant test.config -Dpath=../../crawler/web_director/parser/custom_webpages/mock_site.json -Dthread_url=https://sohaibkarous.wixsite.com/mock-unicorn/forum/general-discussions/unicorns-and-unee-products-for-sale 
```
If we see a message saying 'Success on Thread' then we can begin crawling

```
ant crawl
```

Once the crawl is completed we parse data and then visualise

```
ant parse.crawled-data -Ddata=../../crawler/exported_users/interesting_users_mocked.json
ant viz.trial_1 -Dconfig=../../config/trial_1.ini -Ddata-graph=../../crawler/exported_users/parsed_data.json
```

# Configuration of visualization

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

# Data graph JSON structure

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

# execution

```
cd /projects-git-soton/ogie/focussed_crawler
ant test.intel_viz -Dconfig=../../config/example.ini -Ddata-graph=../../corpus/example/example_data_graph.json
```

# Configuration of crawler
```
{
  "name": "mocked",
  "type" : "forum",
  "depth": "100",
  "comment_model": "keyword",
  "thread_model": "all",
  "filter_comments" : true,
  "comment_length" : 0,
  "anonymous" : true,
  "use_comment_file" : true,
  "comment_keyword_names" : [
    "plants.txt",
    "trade_words.txt",
    "excluded_terms.txt"
  ],
  "thread_keyword": {}
}
```


- name - The website name you defined in the webpage configuration file 

- type - Whether that website is a forum or a marketplace 

- depth - How far you want the crawler to explore the website. The bigger the number the further it explores. (Note this expansion of the search is exponential e.g depth = 1 -> 30 pages, depth = 2 -> 800 pages, depth = 3 -> 30,000 pages) 

- Comment_model - The model needed for directing the crawler.  

- Thread_model - The model needed for directing the crawler.

- Filter_comments - False to take all comments or true to only interesting ones.

- Comment_length - How many comments are needed before exporting. 

- Anonymous - True if you want to anonymous crawl. This hashes the username of all the individuals 

- Use_comment_file - True to use lexicon files or false to create your own. 

- Comment_keyword_names - This is where you input the file names of the lexicons you’ve made 

- Thread_keyword - This is where you put the custom lexicon for thread titles.


# Detailed description of the crawler code can be found here
[PDF description](https://git.soton.ac.uk/ogie/focussed_crawler/-/blob/master/crawler/Project_ogie_code_description.pdf)
# admin

GitLab URI: https://git.soton.ac.uk/ogie/focussed_crawler.git


Contact: sem03@soton.ac.uk