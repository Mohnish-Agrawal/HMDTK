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
        answers = getResults([question], 5)[0]
        answer = ''
        for ans in answers:
            answer += ans + ' '
        summary = self.ps.summarize(answer, 3)
        return summary


if __name__ == '__main__':
    qna = QNA('./whatsapp.txt')
    question = 'how Is my data information (user history, location history, cookies, etc) collected/stored by this app?'
    print(qna.get_answer(question))
