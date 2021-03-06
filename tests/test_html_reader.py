# This file contains tests for the reader. 
# Keep adding tests as we write more and more functions.
# you can run these with `python tests.py`.

from unittest import TestCase
from tests.test_case_extended import TestCaseExtended
from pathlib import Path
from bs4 import BeautifulSoup as BS
import sys

# Make it possible to import modules from "src"
sys.path.insert(0, "src")

from html_reader import (
    is_choices,
    parse_choices,
    parse_reference,
    html_to_questions,
)

class TestParseReference(TestCaseExtended):
    sample_references = {
        "061423ai": {
            "year": 2014,
            "month": "June",
            "question": 23,
            "course": "Algebra I"
        },
        "011832aii": {
            "year": 2018,
            "month": "January",
            "question": 32,
            "course": "Algebra II"
        },
        "011832geo": {
            "year": 2018,
            "month": "January",
            "question": 32,
            "course": "Geometry"
        }
    }
    def test_parses_reference_correctly(self):
        for ref, expected in self.sample_references.items():
            observed = parse_reference(ref)
            self.assertDictsAreEqual(expected, observed)

class TestIsChoices(TestCaseExtended):
    samples = [
        "question_text.html",
        "choices_text.html",
        "choices_images.html",
    ]
    expected = [
        False,
        True,
        True,
    ]
    def test_determines_if_is_choices(self):
        for doc, expected in zip(self.sample_docs, self.expected):
            self.assertEqual(is_choices(doc), expected)

class TestParseChoices(TestCaseExtended):
    samples = [
        "choices_text.html",
        "choices_images.html"
    ]
    def test_finds_four_choices(self):
        for doc in self.sample_docs:
            self.assertEqual(len(parse_choices(doc)), 4)

class TestHTMLtoQuestions(TestCaseExtended):
    def test_parses_all_questions(self):
        samples = (
            ("data/html/A.APR.A.1.OperationswithPolynomials1a.html", 15),
        )
        for filepath, expected_questions in samples:
            question_html = BS(Path(filepath).read_text(), 'lxml')
            print(type(question_html))
            questions = html_to_questions(question_html)
            self.assertEqual(expected_questions, len(questions))





