"""Unit test utils."""

from forward43.utils.elasticsearch import get_mappings

import unittest
from click.testing import CliRunner

from forward43 import forward43
from forward43 import cli


class TestForward43(unittest.TestCase):
    """Tests for `forward43` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_get_mappings_linkedin(self):
        """Test something."""
        actual_mapping = get_mappings("linkedin")

        expected_mapping = {
            "properties": {
                "company_name"    : { "type" : "text" },
                "description"     : { "type" : "text" },
                "status"          : { "type" : "text" },
                "innovation_type" : { "type" : "text" },
                "country"         : { "type" : "text" },
                "contact"         : { "type" : "text" },
                "year_founded"    : { "type":  "integer" },
                "industry"        : { "type":  "keyword" },
                "num_people"      : { "type":  "integer" },
                "linkedin_link"   : { "type" : "keyword" },
                "website_link"    : { "type" : "keyword" },
            }
        }
        self.assertDictEqual(actual_mapping, expected_mapping)

    def test_get_mappings_scrapes(self):
        """Test something."""
        actual_mapping = get_mappings("project_scrapes")

        expected_mapping = {
            "properties": {
                "title"           : { "type" : "text" },
                "description"     : { "type" : "text" },
                "status"          : { "type" : "text" },
                "innovation_type" : { "type" : "text" },
                "country"         : { "type" : "text" },
                "contact"         : { "type" : "text" },
                "link"            : { "type" : "text" }
            }
        }
        self.assertDictEqual(actual_mapping, expected_mapping)



    def test_command_line_interface(self):
        """Test the CLI."""
        runner = CliRunner()
        result = runner.invoke(cli.main)
        assert result.exit_code == 0
        assert 'forward43.cli.main' in result.output
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert '--help  Show this message and exit.' in help_result.output
