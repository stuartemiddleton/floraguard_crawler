import sys
import json
import random
import stanza

if __name__ == '__main__':
    file_path = sys.argv[1]
    stanza.download('en')  # download English model
    nlp = stanza.Pipeline('en')  # initialize English neural pipeline

    with open(file_path, encoding='utf8') as f:
        parsed = json.load(f)

    new_dict = {}
    for k, v in dict(parsed).items():
        for a, b in v["comments"].items():
            if a not in new_dict:
                new_dict[a] = [k]
            else:
                new_dict[a] += [k]

    final_dict = {}
    i = 0
    for k, v in new_dict.items():
        for person in v:
            og = k
            _id = k.replace(" ", "") + "" + str(random.randint(1, 1000))
            final_dict[_id] = {
                "author": person,
                "page_url": og
            }
            for comment in parsed[person]['comments'][og]:
                ner_tags = []
                processed = nlp(comment).sentences
                for sentence in processed:
                    for word in sentence.to_dict():
                        if word['ner'] != 'O':
                            ner_tags.append(word['ner'] + ":" + word['text'])

                final_dict[_id][str(i)] = [{"entity": ner_tags}]
                i += 1

    with open(r'../exported_users/parsed_data.json', 'w') as fp:
        json.dump(final_dict, fp)