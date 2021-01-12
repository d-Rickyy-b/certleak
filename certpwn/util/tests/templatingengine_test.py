# -*- coding: utf-8 -*-

import json
import unittest

from certpwn.util.templatingengine import TemplatingEngine


class TestTemplatingEngine(unittest.TestCase):

    def setUp(self):
        """Sets up the test case"""
        with open("test.json", "r", encoding="utf-8") as f:
            self.update = json.load(f)

    def test_fill_template(self):
        """Checks if templating engine inserts cert data correctly into the template"""
        analyzer_name = "TestAnalyzer"
        template = "New update matched by analyzer '${analyzer_name}' - Domains: ${data.leaf_cert.subject.CN}\n\nMatches:\n${matches}"
        expected = "New update matched by analyzer '{0}' - Domains: {1}\n\nMatches:\n{2}".format(analyzer_name, "mytechnicalhindi.com", "")

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


if __name__ == "__main__":
    unittest.main()
