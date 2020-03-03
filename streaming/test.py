import io

import requests
import simplejson as json
from avro.io import BinaryDecoder, DatumReader
from avro.schema import SchemaFromJSONData
from django.test import TestCase, RequestFactory

from api import api_pb2
from api.avro_schema import avro_api_schema
from api.services import DataSource
from api.views import JSONView, avro_view, protobuf_view


class TestRunner(TestCase):

    def _assert(self, content):
        self.expected_response = DataSource().data
        for c, e in zip(content, self.expected_response):
            self.assertDictEqual(c, e)

    def test_drf(self):
        request = RequestFactory().get('http://127.0.0.1:8000/drf/?format=json')
        view = JSONView.as_view()
        response = view(request)
        response.render()
        print("drf - response size = {}".format(len(response.content)))
        content = json.loads(response.content)
        self._assert(content)

    def test_avro(self):
        request = RequestFactory().get('http://127.0.0.1:8000/avro/')
        response = avro_view(request)
        print("avro - response size = {}".format(len(response.content)))
        content = self._decode_avro(response.content)
        self._assert(content)

    def test_protobuf(self):
        request = RequestFactory().get('http://127.0.0.1:8000/pb/')
        response = protobuf_view(request)
        print("protobuf - response size = {}".format(len(response.content)))
        content = self._decode_protobuf(response.content)
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
    def _decode_protobuf(content):
        model = api_pb2.Response()
        model.ParseFromString(content)
        content = [
            {'text': item.text, 'number': item.number}
            for item in model.items
        ]
        return content
