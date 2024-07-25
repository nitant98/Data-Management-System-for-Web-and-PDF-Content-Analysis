from Validation import Topic
from unittest import TestCase
from pydantic import ValidationError

class TestTopic(TestCase):
    def test_topic_success(self):
        # Test case where all fields are valid
        try:
            data1 = Topic(Name_of_the_topic="Topic 1", Year=2020, Level="CFA ProgramLevel 1",
                          Introduction_Summary="Summary", Learning_Outcomes="Outcomes",
                          Link_to_the_Summary_Page="https://example.com/summary", 
                          Link_to_the_PDF_File="https://example.com/file.pdf")
        except ValidationError as e:
            self.fail("Validation error raised unexpectedly")

    def test_default_success(self):
        # Test case where optional fields are not provided (set to default)
        try:
            data2 = Topic(Name_of_the_topic="Topic 2")
        except ValidationError as e:
            self.fail("Validation error raised unexpectedly")

    def test_year_success(self):
        # Test case where Year is set to a valid value
        try:
            data3 = Topic(Name_of_the_topic="Topic 3", Year="2021")
        except ValidationError as e:
            self.fail("Validation error raised unexpectedly")

    def test_link_success(self):
        # Test case where PDF link is valid
        try:
            data4 = Topic(Name_of_the_topic="Topic 4", Link_to_the_PDF_File="https://www.oracle.com/a/ocom/docs/what-is-big-data-ebook-4421383.pdf")
        except ValidationError as e:
            self.fail("Validation error raised unexpectedly")

    def test_level_success(self):
        # Test case where Level is "N/A"
        try:
            data5 = Topic(Name_of_the_topic="Topic 5", Level="CFA ProgramLevel I")
        except ValidationError as e:
            self.fail("Validation error raised unexpectedly")

    def test_year_failure(self):
        # Test case where Year is not a 4-digit number
        with self.assertRaises(ValidationError):
            data6 = Topic(Name_of_the_topic="Topic 6", Year=99)

    def test_year_link_failure(self):
        # Test case where Year is not within the specified range
        with self.assertRaises(ValidationError):
            data7 = Topic(Name_of_the_topic="Topic 7", Link_to_the_PDF_File="https://www.oracle.com/a/ocom/docs/what-is-big-data-ebook-4421383.pdf",Year=2026)

    def test_level_failure(self):
        # Test case where Level format is incorrect
        with self.assertRaises(ValidationError):
            data8 = Topic(Name_of_the_topic="Topic 8", Level="Program Level 1")

    def test_link_failure(self):
        # Test case where PDF link does not end with '.pdf'
        with self.assertRaises(ValidationError):
            data9 = Topic(Name_of_the_topic="Topic 9", Link_to_the_PDF_File="https://example.com/not_pdf")

    def test_linkna_failure(self):
        # Test case where PDF link is invalid (starts with 'n/A')
        with self.assertRaises(ValidationError):
            data10 = Topic(Name_of_the_topic="Topic 10", Link_to_the_PDF_File="n/A")

