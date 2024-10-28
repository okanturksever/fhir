import json

import dotted

# This is a simple class just to give you guys a brief idea how to extract fields from json.
# By the help of dotted you can keep your code simple like this.
class DataExtractor:

    def extract_data(self, data, fields):
        results = {}
        for field in fields:
            value = dotted.get(data, field["src_key"])

            if isinstance(value, tuple):
                value = list(value)

            # If you don't wanna use labeling..
            dst_key = field.get("dst_key") or field["src_key"]

            # I put json support just for now, you can support the other types as well (integer, float or even regex)
            # It seems it would be a good idea to take this part out of here
            if field.get("format") == "json":
                value = self._parse_json(value)

            results[dst_key] = value
        return results

    @staticmethod
    def _parse_json(value):
        if isinstance(value, list):
            return [json.loads(item) for item in value]
        elif isinstance(value, str):
            return json.loads(value)
        return value
