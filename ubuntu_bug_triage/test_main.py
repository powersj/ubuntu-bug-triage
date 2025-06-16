import unittest

from ubuntu_bug_triage import __main__ as ubt_main


class CliTest(unittest.TestCase):
    def test_tag_default(self):
        args = ubt_main.parse_args(args=[])
        assert args.tags == []
        assert args.tags_combinator == "All"

    def test_tags_parse(self):
        """CLI parses negative and normal tags."""
        mock_argv = [
            "--any-tag",
            "-t",
            "foo",
            "-tbar",
            "--tag",
            "baz",
            "-t-notfoo",
            "-t=-notbar",
            "--tag=-notbaz",
        ]
        args = ubt_main.parse_args(args=mock_argv)
        assert args.tags == ["foo", "bar", "baz", "-notfoo", "-notbar", "-notbaz"]
        assert args.tags_combinator == "Any"
