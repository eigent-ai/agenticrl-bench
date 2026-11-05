"""Tests for the formatter module."""
from objspy.formatter import format_report


class TestBasicFormatting:
    def test_type_in_output(self):
        report = {
            "type": "TestObj",
            "attributes": {
                "name": {"value": "hello", "category": "data", "signature": None}
            },
        }
        output = format_report(report)
        assert "TestObj" in output

    def test_attr_in_output(self):
        report = {
            "type": "TestObj",
            "attributes": {
                "name": {"value": "hello", "category": "data", "signature": None}
            },
        }
        output = format_report(report)
        assert "name" in output


class TestFalsyValues:
    def test_zero_included(self):
        report = {
            "type": "TestObj",
            "attributes": {
                "count": {"value": 0, "category": "data", "signature": None},
            },
        }
        output = format_report(report)
        assert "count" in output

    def test_empty_string_included(self):
        report = {
            "type": "TestObj",
            "attributes": {
                "label": {"value": "", "category": "data", "signature": None},
            },
        }
        output = format_report(report)
        assert "label" in output

    def test_empty_list_included(self):
        report = {
            "type": "TestObj",
            "attributes": {
                "items": {"value": [], "category": "data", "signature": None},
            },
        }
        output = format_report(report)
        assert "items" in output


class TestNestedFormatting:
    def test_nested_dict_multiline(self):
        nested = {f"section_{i}": {f"key_{j}": j * 100 for j in range(5)} for i in range(4)}
        report = {
            "type": "TestObj",
            "attributes": {
                "data": {"value": nested, "category": "data", "signature": None}
            },
        }
        output = format_report(report)
        lines = output.split("\n")
        assert len(lines) > 5, "Nested dict should be pretty-printed across multiple lines"


class TestSignatureDisplay:
    def test_method_signature_shown(self):
        report = {
            "type": "TestObj",
            "attributes": {
                "greet": {
                    "value": "callable",
                    "category": "method",
                    "signature": "(self, name)",
                }
            },
        }
        output = format_report(report)
        assert "(self, name)" in output
