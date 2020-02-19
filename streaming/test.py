import io

import avro
import requests
from django.test import TestCase

from api.services import DataSource


class TestRunner(TestCase):

    def test_drf(self):
        expected_response = DataSource().data
        response = requests.get('http://127.0.0.1:8000/drf/')
        for c, e in zip(response.json(), expected_response):
            self.assertDictEqual(c, e)

    def test_avro(self):
        schema = avro.schema.Parse(open("api/api.avsc", "rb").read())
        expected_response = DataSource().data
        response = requests.get('http://127.0.0.1:8000/avro/')
        raw_bytes = response.content
        print(raw_bytes)
        buffer = io.BytesIO(raw_bytes)
        decoder = avro.io.BinaryDecoder(buffer)
        reader = avro.io.DatumReader(schema)
        row = reader.read(decoder)
        while row:
            print(row)
            expected = expected_response.pop(0)
            self.assertDictEqual(row, expected)
            row = reader.read(decoder)
