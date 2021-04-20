from summarization import getResults, init
from typing import List
from werkzeug.utils import secure_filename
import json
import os
script_path = os.path.dirname(os.path.abspath(__file__))
# run_path = os.path.dirname(os.getcwd())

class PolicySummarizer(object):
    def __init__(self):
        pass

    def summarize(self, policy: str, lines: int = 10) -> List[str]:
        from sumy.parsers.plaintext import PlaintextParser
        from sumy.nlp.tokenizers import Tokenizer
        from sumy.summarizers.lex_rank import LexRankSummarizer

        summarizer = LexRankSummarizer()
        parser = PlaintextParser.from_string(policy, Tokenizer("english"))
        summary = summarizer(parser.document, lines)
        return [str(s) for s in summary]


class QNA:
    def __init__(self, policy_path: str) -> None:
        self.ps = PolicySummarizer()
        init(policy_path)

    def get_answer(self, question: str) -> List[str]:
        answers = getResults([question], 3)[0]
        answer = ''
        for ans in answers:
            answer += ans + ' '
        # print(answer)
        summary = self.ps.summarize(answer, 3)
        return summary

def getData(f, saveDoc = True):
    name = f
    if saveDoc:
        d = f.save(secure_filename(f.filename))
        name = script_path + "/../../"+ secure_filename(f.filename)
    qna = QNA(name)
    question = ['how Is my data information (user history, location history, cookie profilling, etc) collected/stored by this app?',
                'Is my information or my data being shared to other products and services or with other third party services? If so, how is it being shared',
                'Is my data being used for Identity resolution, tracking me online or combines with data from other sources',
                'Is my data information being sold, re-packaged, commercialized',
                'Will my data information be retained. If so, for how long will this data be retained and for what purposes?'                
                ]
    data = dict()
    dataId = 0
    keys = ["Data that is being collected by the company",
            "Third Parties : Data being shared with third parties",
            "Tracking : Data being collected from other resources",
            "Protection assurance of the collected data",
            "Retention of data/personal information"
    ]
    for q in question:
        data[keys[dataId]] = qna.get_answer(q)
        dataId += 1
    return data

def getPolicyData(name):
    with open(script_path + '/data.txt') as json_file:
        data = json.load(json_file)
        return data[name]

if __name__ == '__main__':
    print('apple.txt')
    qna = QNA('apple.txt')
    question = ['how Is my data information collected or stored(user history, location history, cookie profilling, etc) by this app?',
                'Is my information or my data shared to third party services other products and services or with other third party services',
                'Is my data being tracked from other sources like cookies, pixel tags, websites third party information etc. or is my data being collected from cookies websites',
                "How do we use personal information information data collected what is the purpose of collecting data ",
                'Will my data or personal information be retained. If so, for how long will this data be retained and for what purposes?'                
                ]
    for q in question:
        print(qna.get_answer(q))
