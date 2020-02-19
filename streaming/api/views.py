from io import BytesIO

import avro
from avro.datafile import DataFileWriter
from avro.io import DatumWriter
from django.http import StreamingHttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView

from api import api_pb2
from api.services import DataSource


class JSONView(APIView):

    def get(self, request):
        data = DataSource().data
        return Response(data)


def avro_view(request):
    data = DataSource().data
    schema = avro.schema.Parse(open("api/api.avsc", "rb").read())
    buffer = BytesIO()
    writer = avro.io.DatumWriter(schema)
    encoder = avro.io.BinaryEncoder(buffer)
    for item in data:
        writer.write(item, encoder)
    response = StreamingHttpResponse(buffer.getvalue(), content_type='avro/binary')
    return response


def protobuf_view(request):
    response = api_pb2.Response()
    for data in DataSource().data:
        item = response.items.add()
        item.text = data['text']
        item.number = data['number']

    return StreamingHttpResponse(response.SerializeToString(), content_type='text/plain')

