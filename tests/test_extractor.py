import unittest

from extractor import DataExtractor


# I wrote these tests to show you the simple features of `extract_data` function.
class TestDataExtractor(unittest.TestCase):
    def setUp(self):
        self.sample_data = {
            "id": "8m0KJz1PLFa8y1T4IK5y7XjnMZuXs",
            "object": "my little object",
            "created": 1706451691,
            "choices": [
                {
                    "index": 0,
                    "message": {
                        "role": "intern",
                        "content": "{\"integration_message\":\"my little message\"}"
                    },
                    "finish_reason": "stop"
                },
                {
                    "index": 1,
                    "message": {
                        "role": "assistant",
                        "content": "{\"integration_message\":\"another message\"}"
                    },
                    "finish_reason": "stop"
                },
                {
                    "index": 2,
                    "message": {
                        "role": "manager",
                        "content": "{\"integration_message\":\"another message2\"}"
                    },
                    "finish_reason": "error"
                }
            ]
        }
        self.extractor = DataExtractor()

    def test_extract_basic_fields(self):
        basic_fields = [
            {
                "dst_key": "Id",
                "src_key": "id",
            },
            {
                "dst_key": "Object",
                "src_key": "object",
            },
        ]
        results = self.extractor.extract_data(self.sample_data, basic_fields)
        self.assertEqual(results.get('Id'), '8m0KJz1PLFa8y1T4IK5y7XjnMZuXs')
        self.assertEqual(results.get('Object'), 'my little object')

    def test_extract_basic_fields_without_label(self):
        basic_fields_without_label = [
            {
                "src_key": "created",
            }
        ]
        results = self.extractor.extract_data(self.sample_data, basic_fields_without_label)
        self.assertEqual(results.get('created'), 1706451691)

    def test_extract_by_index_from_arrays(self):
        static_array_fields = [
            {
                "dst_key": "First Element",
                "src_key": "choices[0].message.role",
            },
            {
                "dst_key": "Third Element",
                "src_key": "choices[2].message.role",
            },
        ]
        results = self.extractor.extract_data(self.sample_data, static_array_fields)
        self.assertEqual(results.get('First Element'), 'intern')
        self.assertEqual(results.get('Third Element'), 'manager')

    def test_extract_fields_from_arrays(self):
        dynamic_array_fields = [
            {
                "dst_key": "Roles",
                "src_key": "choices[*].message.role",
            }
        ]
        results = self.extractor.extract_data(self.sample_data, dynamic_array_fields)
        self.assertEqual(results.get('Roles'), ['intern', 'assistant', 'manager'])

    def test_extract_fields_with_json_types(self):
        json_type_fields = [
            {
                "dst_key": "My JSON Content",
                "src_key": "choices[*].message.content",
                "format": "json"
            }
        ]
        results = self.extractor.extract_data(self.sample_data, json_type_fields)
        self.assertEqual(results.get('My JSON Content'), [{'integration_message': 'my little message'}, {'integration_message': 'another message'}, {'integration_message': 'another message2'}])


if __name__ == "__main__":
    unittest.main()
