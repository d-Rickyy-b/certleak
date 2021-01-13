# -*- coding: utf-8 -*-

import json
import pathlib
import unittest
from unittest.mock import Mock

from certpwn.util.templatingengine import TemplatingEngine


class TestTemplatingEngine(unittest.TestCase):

    def setUp(self):
        """Sets up the test case"""
        self.update = Mock()
        self.update.to_dict = Mock()
        test_file = pathlib.Path(__file__).parent.absolute() / "test.json"
        with open(test_file, "r", encoding="utf-8") as f:
            self.update.to_dict.return_value = json.load(f)

    def test_fill_template(self):
        """Checks if templating engine inserts cert data correctly into the template"""
        analyzer_name = "TestAnalyzer"
        template = "New update matched by analyzer '${analyzer_name}' - Domains: ${data.leaf_cert.subject.CN}\n\nMatches:\n${matches}"
        expected = "New update matched by analyzer '{0}' - Domains: {1}\n\nMatches:\n{2}".format(analyzer_name, "www.mail.casamarket.ro", "")

        result = TemplatingEngine.fill_template(update=self.update, analyzer_name=analyzer_name, template_string=template)

        self.assertEqual(expected, result, msg="Filled template string is not the same as the expected result!")

    def test__normalize_placeholders_no_placeholder(self):
        """Check if '_normalize_placeholders' works for strings without placeholders"""
        template_string = "This is a test template with no placeholder"
        expected = "This is a test template with no placeholder"
        result = TemplatingEngine._normalize_placeholders(template_string)
        self.assertEqual(expected, result, msg="Filled template string is not the same as the expected result!")

    def test__normalize_placeholders_two_placeholders(self):
        """Check if '_normalize_placeholders' works for strings with two placeholders"""
        template_string = "This is a ${analyzer_name} test template with ${data.leaf_cert} two placeholders"
        expected = "This is a ${analyzer_name} test template with ${data__leaf_cert} two placeholders"
        result = TemplatingEngine._normalize_placeholders(template_string)
        self.assertEqual(expected, result, msg="Filled template string is not the same as the expected result!")

    def test__normalize_placeholders_two_placeholders_decoy(self):
        """Check if '_normalize_placeholders' works for strings with two placeholders and some decoy placeholder"""
        template_string = "This is a ${analyzer_name} test template with ${data.leaf_cert} two placeholders and data.leaf_cert some decoy data."
        expected = "This is a ${analyzer_name} test template with ${data__leaf_cert} two placeholders and data.leaf_cert some decoy data."
        result = TemplatingEngine._normalize_placeholders(template_string)
        self.assertEqual(expected, result, msg="Filled template string is not the same as the expected result!")

    def test__normalize_placeholders_separator(self):
        """Check if '_normalize_placeholders' works with any separator"""
        template_string = "This is a ${analyzer_name} test template with ${data.leaf_cert} two placeholders and data.leaf_cert some decoy data."
        expected = "This is a ${analyzer_name} test template with ${data###leaf_cert} two placeholders and data.leaf_cert some decoy data."
        separator = "###"
        result = TemplatingEngine._normalize_placeholders(template_string, sep=separator)
        self.assertEqual(expected, result, msg="Filled template string is not the same as the expected result!")

    def test__flatten_update_dict(self):
        """Check if flattening dicts works as intended"""
        d = {"test": "asdf",
             "nested": {"inner": "content", "another": "other content"},
             "double_nested": {"inside_double_nested": {"totally_inner": "final"}},
             "outer": "yes"
             }
        new_d = TemplatingEngine._flatten_update_dict(d, parent_key="", sep="__")

        # Make sure new_d contains 5 elements on the root level
        self.assertEqual(len(new_d), 5)

        # Check if combined keys are contained in the dict
        self.assertIn("test", new_d)
        self.assertIn("nested__inner", new_d)
        self.assertIn("nested__another", new_d)
        self.assertIn("double_nested__inside_double_nested__totally_inner", new_d)
        self.assertIn("outer", new_d)

        # Make sure that "nested" doesn't exist anymore
        nested = new_d.get("nested")
        self.assertIsNone(nested)

        # Check if nested elements have been pulled up correctly
        nested_inner = new_d.get("nested__inner")
        self.assertEqual(nested_inner, "content")

        # Check for double nested content
        double_nested_inner = new_d.get("double_nested__inside_double_nested__totally_inner")
        self.assertEqual(double_nested_inner, "final")

    def test__flatten_update_dict_separator(self):
        """Check if changing separators works as intended"""
        d = {"test": "asdf",
             "nested": {"inner": "content", "another": "other content"},
             "double_nested": {"inside_double_nested": {"totally_inner": "final"}},
             "outer": "yes"
             }
        new_d = TemplatingEngine._flatten_update_dict(d, parent_key="", sep="###")

        # Make sure new_d contains 5 elements on the root level
        self.assertEqual(len(new_d), 5)

        # Check if changing separators works as intended
        self.assertIn("test", new_d)
        self.assertIn("nested###inner", new_d)
        self.assertIn("nested###another", new_d)
        self.assertIn("double_nested###inside_double_nested###totally_inner", new_d)
        self.assertIn("outer", new_d)


if __name__ == "__main__":
    unittest.main()
