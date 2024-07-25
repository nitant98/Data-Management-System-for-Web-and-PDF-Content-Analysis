from Validation import Metadata
from unittest import TestCase
from pydantic import ValidationError


class TestMetadata(TestCase):

    # Pass
    def test_metadata_success(self):
        # Test case where all fields are valid
        try:
            data1 = Metadata(Title="Title", Publisher="Publisher", AvailabilityStatus="available",
                             AppInfoDescription="Description", Abstract="Abstract")
        except ValidationError as e:
            self.fail("Validation error raised unexpectedly")

    def test_reference_none(self):
        # Test case where BiblicalReference is None
        try:
            data2 = Metadata(Title="Title", Publisher="Publisher", AvailabilityStatus="available",
                             AppInfoDescription="Description", Abstract="Abstract", BiblicalReference=None)
        except ValidationError as e:
            self.fail("Validation error raised unexpectedly")

    def test_abstract_nospecialchar(self):
        # Test case where all fields are valid with special characters in Abstract
        try:
            data3 = Metadata(Title="Title", Publisher="Publisher", AvailabilityStatus="unavailable",
                             AppInfoDescription="Description", Abstract="Abstract with special character:")
        except ValidationError as e:
            self.fail("Validation error raised unexpectedly")

    def test_title_nospecialchar(self):
        # Test case where BiblicalReference is valid
        try:
            data4 = Metadata(Title="Title", Publisher="Publisher", AvailabilityStatus="unknown",
                             AppInfoDescription="Description", Abstract="Abstract", BiblicalReference="John 3:16")
        except ValidationError as e:
            self.fail("Validation error raised unexpectedly")

    def test_availability(self):
        # Test case where AvailabilityStatus is valid 
        try:
            data5 = Metadata(Title="Title", Publisher="Publisher", AvailabilityStatus="available",
                             AppInfoDescription="Description", Abstract="Abstract", BiblicalReference="")
        except ValidationError as e:
            self.fail("Validation error raised unexpectedly")


    # Fail

    def test_title_failure(self):
        # Test case where Title contains special characters
        with self.assertRaises(ValidationError):
            data6 = Metadata(Title="Title:$", Publisher="Publisher", AvailabilityStatus="available",
                             AppInfoDescription="Description", Abstract="Abstract",BiblicalReference="")

    def test_publisher_failure(self):
        # Test case where Publisher contains special characters
        with self.assertRaises(ValidationError):
            data7 = Metadata(Title="Title", Publisher="Publisher#", AvailabilityStatus="available",
                             AppInfoDescription="Description", Abstract="Abstract",BiblicalReference="")

    def test_availability_failure(self):
        # Test case where AvailabilityStatus is invalid
        with self.assertRaises(ValidationError):
            data8 = Metadata(Title="Title", Publisher="Publisher", AvailabilityStatus="invalid",
                             AppInfoDescription="Description", Abstract="Abstract",BiblicalReference="")

    def test_abstract_failure(self):
        # Test case where Abstract contains special characters
        with self.assertRaises(ValidationError):
            data9 = Metadata(Title="Title", Publisher="Publisher", AvailabilityStatus="available",
                             AppInfoDescription="Description", Abstract="Abstract with special character: □$%")

    def test_reference_failure(self):
        # Test case where AvailabilityStatus is missing
        with self.assertRaises(ValidationError):
            data10 = Metadata(Title="Title", Publisher="Publisher", AppInfoDescription="Description", Abstract="Abstract",BiblicalReference="@#$%")
