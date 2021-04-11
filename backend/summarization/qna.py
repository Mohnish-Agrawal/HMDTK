from summarization import getResults, init
from typing import List


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
        print(answer)
        summary = self.ps.summarize(answer, 3)
        return summary


if __name__ == '__main__':
    print('apple.txt')
    qna = QNA('apple.txt')
    question = ['how Is my data information (user history, location history, cookie profilling, etc) collected/stored by this app?',
                'Is my information or my data being shared to other products and services or with other third party services? If so, how is it being shared',
                'Is my data being used for Identity resolution, tracking me online or combines with data from other sources',
                'Is my data information being sold, re-packaged, commercialized',
                'Will my data information be retained. If so, for how long will this data be retained and for what purposes?'                
                ]
    for q in question:
        print(qna.get_answer(q))