import sys,os
import json
import random
import stanza
import re
def read_txt(path):
    regex = r"(?i).*"
    with open(path, encoding='utf-8') as f:
        lines = f.readlines()
        for i in range(0, len(lines)):
            if i == 0:
                regex += r"(\b" + lines[i].strip()+r"\b"
            else:
                regex += r"|\b" + lines[i].strip()+r"\b"
        regex += r").*"
    return regex


if __name__ == '__main__':
    parsed = {}
    print(sys.argv)
    for i in range(1, len(sys.argv)):
        file_path = sys.argv[i]

        with open(file_path, encoding='utf8') as f:
            parsed.update(json.load(f))

    stanza.download('en')  # download English model
    nlp = stanza.Pipeline('en')  # initialize English neural pipeline

    new_dict = {}
    for k, v in dict(parsed).items():
        for a, b in v["comments"].items():
            if a not in new_dict:
                new_dict[a] = [k]
            else:
                new_dict[a] += [k]

    i = 0
    final_dict = {}
    for k, v in new_dict.items():
        # < website > _thread_ < thread_id > _post_ < post_id >
        for person in v:
            og = k
            _id = k.rsplit('/',1)[1] + "_thread_" + str(hash(k.rsplit('/',1)[1])% (10 ** 8))+"_post_"+str(random.randint(1, 10000))
            final_dict[_id] = {
                "author": person,
                "page_url": og
            }
            for comment in parsed[person]['comments'][og]:
                ner_tags = []
                processed = nlp(comment["comment"]).sentences
                for sentence in processed:
                    for word in sentence.to_dict():
                        if word['ner'] != 'O':
                            ner_tags.append(word['ner'] + ":" + word['text'])

                ######### CUSTOM NERS ##########
                import os
                path = '..' + os.sep + 'web_director' + os.sep + 'lexicon'
                for file in os.listdir(path):
                    regex = read_txt(path + os.sep + file)
                    for words in re.findall(regex,comment["comment"]):
                        res = file.replace(".txt","").replace("_", " ").title().replace(" ", "")
                        ner_tags.append("NER-"+res+":"+words)
                ################################
                final_dict[_id][str(i)] = [{"entity": ner_tags}]
                i += 1

    for file in os.listdir(path):
        res = file.replace(".txt","").replace("_", " ").title().replace(" ", "")
        print("CUSTOM NER: " + "NER-" + res)

    with open('..' + os.sep + 'exported_users' + os.sep + 'parsed_data.json', 'w') as fp:
        json.dump(final_dict, fp)

