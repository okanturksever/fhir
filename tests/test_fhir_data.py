import json
import unittest

from extractor import DataExtractor


# I tried to apply fhir data
class TestDataExtractor(unittest.TestCase):
    def setUp(self):
        with open("data/ema_example_fhir01.json", "r") as f:
            self.sample_fhir_data = json.load(f)
        self.extractor = DataExtractor()

    def test_extract_basic_fields(self):
        basic_fields = [
            {
                "dst_key": "Meta Domain",
                "src_key": "meta.domain",
            },
            {
                "dst_key": "Meta Version",
                "src_key": "meta.version",
                # "format": "integer"
                # if you want a type support for integers, go implement it..
            },
        ]
        results = self.extractor.extract_data(self.sample_fhir_data, basic_fields)
        self.assertEqual(results.get('Meta Domain'), '100000000013')
        self.assertEqual(results.get('Meta Version'), '3')

    def test_extract_basic_fields_without_label(self):
        basic_fields_without_label = [
            {
                "src_key": "meta.correlationId",
            }
        ]
        results = self.extractor.extract_data(self.sample_fhir_data, basic_fields_without_label)
        self.assertEqual(results.get('meta.correlationId'), "251183b1-035f-42fb-b560-0ef98e6c7054-CD-02of02")

    def test_extract_by_index_from_arrays(self):
        static_array_fields = [
            {
                "dst_key": "First Entry FullUrl",
                "src_key": "bundle.entry[0].fullUrl",
            },
            {
                "dst_key": "Third Entry FullUrl",
                "src_key": "bundle.entry[2].fullUrl",
            },
            {
                "dst_key": "Third Entry Identifier First Value",  # It's Free to cherry-pick
                "src_key": "bundle.entry[2].resource.identifier[0].value",
            },
        ]
        results = self.extractor.extract_data(self.sample_fhir_data, static_array_fields)
        self.assertEqual(results.get('First Entry FullUrl'), 'MedicinalProductDefinition/600044315326')
        self.assertEqual(results.get('Third Entry FullUrl'), 'PackagedProductDefinition/8485040')
        self.assertEqual(results.get('Third Entry Identifier First Value'), 'e637de1f-863e-4afd-8c8f-d72e679d0a5c')

    def test_extract_fields_from_arrays(self):
        dynamic_array_fields = [
            {
                "dst_key": "Extension Ids",
                "src_key": "bundle.entry[*].resource.extension[*].id",
            },
            {
                "dst_key": "Package Ids",
                "src_key": "bundle.entry[*].resource.package[*].containedItem[*].id",
            }
        ]
        results = self.extractor.extract_data(self.sample_fhir_data, dynamic_array_fields)
        self.assertEqual(results.get('Extension Ids'), ['6600042', '3450050', '5608036'])
        self.assertEqual(results.get('Package Ids'), ['4360050', '4357323'])


if __name__ == "__main__":
    unittest.main()
