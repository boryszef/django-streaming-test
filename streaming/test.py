import io

import requests
from avro.io import BinaryDecoder, DatumReader
from avro.schema import SchemaFromJSONData
from django.test import TestCase

from api import api_pb2
from api.avro_schema import avro_api_schema
from api.services import DataSource


class TestRunner(TestCase):

    def _assert(self, content):
        self.expected_response = DataSource().data
        for c, e in zip(content, self.expected_response):
            self.assertDictEqual(c, e)

    def test_drf(self):
        response = requests.get('http://127.0.0.1:8000/drf/')
        content = response.json()
        self._assert(content)

    def test_avro(self):
        response = requests.get('http://127.0.0.1:8000/avro/')
        content = self._decode_avro(response.content)
        self._assert(content)

    def test_protobuf(self):
        response = requests.get('http://127.0.0.1:8000/pb/')
        content = self._decode_protobuf(response)
        self._assert(content)

    @staticmethod
    def _decode_avro(raw_bytes):
        schema = SchemaFromJSONData(avro_api_schema)
        buffer = io.BytesIO(raw_bytes)
        decoder = BinaryDecoder(buffer)
        reader = DatumReader(schema)
        content = reader.read(decoder)
        return content

    @staticmethod
    def _decode_protobuf(response):
        model = api_pb2.Response()
        model.ParseFromString(response.content)
        content = [
            {'text': item.text, 'number': item.number}
            for item in model.items
        ]
        return content
