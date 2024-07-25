from unittest import TestCase
from pydantic import ValidationError
import sys
from pathlib import Path

root_dir = str(Path(__file__).resolve().parent.parent)
sys.path.append(root_dir)
from Validation import Content

class TestContent(TestCase):
    #Success
    def test_content_valid(self):
        # Test case where all fields are valid
        try:
            data1 = Content(Title="Data1", Subtitle="Test Subtitle", Content="Test Content")
        except ValidationError as e:
            self.fail("Validation error raised unexpectedly")
        
    def test_content_alphanumeric(self):
        # Test case where title and content contain alphanumeric characters
        try:
            data2 = Content(Title="Title123", Subtitle="Subtitle", Content="Content123")
        except ValidationError as e:
            self.fail("Validation error raised unexpectedly")

    def test_content_not_specialchar(self):
        # Test case where title and content contain special characters
        try:
            data3 = Content(Title="Title110", Subtitle="Subtitle", Content="Content without special characters")
        except ValidationError as e:
            self.fail("Validation error raised unexpectedly")

    def test_title_alphanumeric(self):
        # Test case where title and content contain special characters
        try:
            data4 = Content(Title="Title", Subtitle="Subtitle", Content="Content with special characters: ?&$%")
        except ValidationError as e:
            self.fail("Validation error raised unexpectedly")

    def test_title_notblank(self):
        # Test case where title and content are not blank
        try:
            data5 = Content(Title="Very Long Title with Many Characters", Subtitle="Subtitle", Content="Very Long Content with Many Characters")
        except ValidationError as e:
            self.fail("Validation error raised unexpectedly")

    ## Failed
    def test_content_specialchar(self):
        # Test case where title is blank
        with self.assertRaises(ValidationError):
            data6 = Content(Title="", Subtitle="Subtitle", Content="Content with special characters: @#")

    def test_content_blank(self):
        # Test case where content is blank
        with self.assertRaises(ValidationError):
            data7 = Content(Title="Title", Subtitle="Subtitle", Content="")

    def test_title_specialchar(self):       
        # Test case where title contains special characters
        with self.assertRaises(ValidationError):
            data8 = Content(Title="Title$", Subtitle="Subtitle", Content="Content")

    def test_content_specialchar(self):  
        # Test case where content contains special characters
        with self.assertRaises(ValidationError):
            data9 = Content(Title="Title", Subtitle="Subtitle", Content="Content with special character: □")

    def test_title_blank(self):  
        # Test case where title and content are both blank
        with self.assertRaises(ValidationError):
            data10 = Content(Title="", Subtitle="Subtitle", Content="")
            
