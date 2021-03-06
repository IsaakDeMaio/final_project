from bs4 import BeautifulSoup as BS

def is_new_question(tag, tokens=None):
    if tokens == None:
        tokens = tag.get_text().split(' ')
    return tag.name == 'p' and starts_with_number(tag, tokens) and not is_new_answer(tag, tokens)

def starts_with_number(tag, tokens=None):
    if tokens == None:
        tokens = tag.get_text().split(' ')
    return tokens and tokens[0].isdigit()

def is_new_answer(tag, tokens=None):
    if tokens == None:
        tokens = tag.get_text().split(' ')
    return len(tokens) >= 2 and starts_with_number(tag, tokens) and tokens[1] == "ANS:"

def is_choices(tag):
    return tag.name == "table"

def parse_choices(tag):
    choices = []
    for choice in tag.tbody.find_all('tr'):
        label, choice_text = choice.find_all('td')
        choices.append({
            "label": label.get_text(),
            "choice": str(choice_text),
        })
    return choices

def parse_question(tag):
    tokens = tag.get_text().split(' ')
    for img in tag.find_all('img'):
        del img['style']
    return {
        "index": int(tokens[0]),
        "question": str(tag),
    }

def parse_answer(tag):
    tokens = tag.get_text().split(' ')
    answer = str(tag)
    return int(tokens[0]), answer

def parse_reference(ref):
    "Parses a reference string, returning a dict. NOT DONE."
    month_names = {
        "01": "January",
        "06": "June",
        "08": "August",
        "spr": "Spring",
    }
    course_names = {
        "ai": "Algebra I",
        "aii": "Algebra II",
        "geo": "Geometry",
    }
    month = month_names[ref[0:2]]
    year = int(ref[2:4]) + 2000
    question_number = int(ref[4:6])
    course = course_names[ref[6:]]
    
    return {
        "month": month,
        "year": year,
        "question": question_number,
        "course": course
    }

def get_labeled_question_parts(html):
    """Breaks html up into (label, chunk) pieces of questions.
    Each chunk is a BeautifulSoup HTML document containing a single div
    whose class is "question", "choices", or "answer." For example:

        <html>
            <body>
                <div class="question">
                    ...
                </div>
            </body>
        </html>

    Yield is lke return, but the function keeps going. The effect
    is that the function spits out a bunch of values one by one, 
    as if you were iterating through a list.
    """
    chunk = None
    label = "QUESTION"
    for tag in html.body.contents:
        if chunk is None: # This will only be true for the first tag.
            chunk = tag.extract()
        elif is_new_question(tag):
            yield label, chunk
            chunk = BS('<div class="question"></div>', 'lxml')
            chunk.append(tag.extract())
            label = "QUESTION"
        elif is_choices(tag):
            yield label, chunk
            label = "CHOICES"
            chunk = BS('<div class="choices"></div>', 'lxml')
            chunk.append(tag.extract())
        elif is_new_answer(tag):
            yield label, chunk
            label = "ANSWER"
            chunk = BS('<div class="answer"></div>', 'lxml')
            chunk.append(tag.extract())
        else:
            chunk.body.div.append(tag.extract())
    yield label, chunk # ER
        
def html_to_questions(html):
    "Parses test questions from html string"
    if isinstance(html, BS):
        document = html
    else:
        document = BS(html, 'lxml')

    questions = {}

    for label, chunk in get_labeled_question_parts(html):
        # WHAT SHOULD WE DO HERE?

    # ===== OLD CODE =======
    question = None
    for tag in document.body.contents:
        if is_new_question(tag):
            if question:
                questions[question['index']] = question
            question = parse_question(tag)
        elif is_choices(tag):
            question["choices"] = parse_choices(tag)
        elif is_answer(tag):
            continue
            index, answer = parse_answer(tag)
            questions[index]["answer"] = answer
        else:
            question["question"] += str(tag)
    return questions
