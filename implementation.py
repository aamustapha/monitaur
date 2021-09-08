from bs4 import BeautifulSoup
from random import randint
import re
from requests import get as httpGet

from stackapi import StackAPI

stack = StackAPI(name='stackoverflow')


def findImplementations() -> list:
    """
    This function queries the stackexchange API for a list of bubblesort implementation solution
    and returns the list of questions which are tagged python
    """
    questions = stack.fetch('search', intitle='bubble sort implementation', tagged='python')
    return list(filter(lambda question: question['is_answered'], questions['items']))


def loadRandomImplementation(questions: list) -> str:
    """
    This function takes the list of all questions and picks a random question, it fetches the link
    of the question and returns the html block
    """
    randomIndex = randint(1, len(questions))  - 1
    question = questions[randomIndex]
    answers = stack.fetch('questions/{id}/answers', id=question['question_id'])
    # answers = {'backoff': 0, 'has_more': False, 'page': 1, 'quota_max': 300, 'quota_remaining': 213, 'total': 0, 'items': [{'owner': {'reputation': 1242, 'user_id': 9524896, 'user_type': 'registered', 'profile_image': 'https://i.stack.imgur.com/6OnAN.jpg?s=128&g=1', 'display_name': 'Haris Nadeem', 'link': 'https://stackoverflow.com/users/9524896/haris-nadeem'}, 'is_accepted': False, 'score': 1, 'last_activity_date': 1522553278, 'creation_date': 1522553278, 'answer_id': 49594516, 'question_id': 49594218, 'content_license': 'CC BY-SA 3.0'}, {'owner': {'reputation': 827, 'user_id': 3245114, 'user_type': 'registered', 'profile_image': 'https://www.gravatar.com/avatar/8b550b8e747a12bcce2387d8d1f6d8e9?s=128&d=identicon&r=PG', 'display_name': 'Jordan Shurmer', 'link': 'https://stackoverflow.com/users/3245114/jordan-shurmer'}, 'is_accepted': False, 'score': 1, 'last_activity_date': 1522551657, 'creation_date': 1522551657, 'answer_id': 49594385, 'question_id': 49594218, 'content_license': 'CC BY-SA 3.0'}]}

    return question['link'], answers



def pickAnswer(questionUrl: str, answer):
    """
    This would either pick the the correct answer,  first answer or a random answer with atleast 0 upvotes
    eliminate answers with negative upvotes
    """

    def isValidAnswer(answerBlock):
        """
        An answer is valid for us if it uses a function
        :param answerBlocks:
        :return:
        """
        for codeBlock in answerBlock.find_all('code'):
            if codeBlock.text.__contains__('def '):
                return True
        return False

    questionPage = BeautifulSoup(httpGet(questionUrl).text, 'html.parser')
    answerBlocks = questionPage.find_all('div', attrs={'class': 'answer'})
    validAnswers = list(filter(isValidAnswer, answerBlocks))
    randomAnswer = randint(1, len(validAnswers)) - 1
    return validAnswers[randomAnswer]


def getCode(answerHTMLBlock) -> str:
    """
    Using beautifulSoup, navigate the html and find the <pre> with the code block and return only the content
    """
    for codeBlock in answerHTMLBlock.find_all('code'):
        if codeBlock.text.__contains__('def '): # return the first function
            return codeBlock.text


def executeCodeBlock(code):
    functionName = re.search('def \w+', code).group(0)[4:]

    exec(code)
    return functionName


if __name__ == '__main__':

    # implementation = [{'tags': ['python', 'pseudocode', 'bubble-sort'], 'owner': {'reputation': 41, 'user_id': 8776545, 'user_type': 'registered', 'profile_image': 'https://www.gravatar.com/avatar/8e8140a62ff124d230409c7fb74b1b2e?s=128&d=identicon&r=PG&f=1', 'display_name': 'CareFace', 'link': 'https://stackoverflow.com/users/8776545/careface'}, 'is_answered': True, 'view_count': 449, 'answer_count': 2, 'score': 0, 'last_activity_date': 1522553278, 'creation_date': 1522549344, 'last_edit_date': 1522552834, 'question_id': 49594218, 'content_license': 'CC BY-SA 3.0', 'link': 'https://stackoverflow.com/questions/49594218/bubble-sort-implementation-from-pseudocode', 'title': 'Bubble sort implementation from Pseudocode'}, {'tags': ['python', 'algorithm'], 'owner': {'reputation': 23, 'user_id': 7153157, 'user_type': 'registered', 'profile_image': 'https://i.stack.imgur.com/qHalP.jpg?s=128&g=1', 'display_name': 'allan e', 'link': 'https://stackoverflow.com/users/7153157/allan-e'}, 'is_answered': True, 'view_count': 114, 'closed_date': 1513526458, 'answer_count': 1, 'score': -1, 'last_activity_date': 1512857977, 'creation_date': 1512856499, 'last_edit_date': 1512857977, 'question_id': 47733606, 'link': 'https://stackoverflow.com/questions/47733606/bubble-sort-implementation-not-working', 'closed_reason': 'Not suitable for this site', 'title': 'Bubble sort implementation not working'}]

    implementation = findImplementations()
    # print(implementation)
    questionUrl, answerList = loadRandomImplementation(implementation)
    answer = pickAnswer(questionUrl, answerList)
    code = getCode(answer)
    func = executeCodeBlock(code)

    integers = input("Hello! Please provide a list of integers.")