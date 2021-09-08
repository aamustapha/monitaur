"""
This function queries the stackexchange API for a list of bubblesort implementation solution
and returns the list of questions which are tagged python
"""
def findImplementations() -> list:
    pass

"""
This function takes the list of all questions and picks a random question, it fetches the link
of the question and returns the html block
"""
def loadRandomImplementation(questions: list) -> str:
    pass

"""
This would either pick the the correct answer,  first answer or a random answer with atleast 0 upvotes 
eliminate answers with negative upvotes
"""
def pickAnswer(questionUrl: str):
    pass

"""
Using beautifulSoup, navigate the html and find the <pre> with the code block and return only the content
"""
def returnCodeBlock(answerHTMLBlock) -> str:
    pass

"""
Use eval to execute function, return the function name
"""
def executeCodeBlock(code):
    pass
