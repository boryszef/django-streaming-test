from io import BytesIO

from avro.io import DatumWriter, BinaryEncoder
from avro.schema import SchemaFromJSONData
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView

from api import api_pb2
from api.avro_schema import avro_api_schema
from api.services import DataSource, profile_me


class JSONView(APIView):

    @profile_me
    def get(self, request):
        data = DataSource().data
        return Response(data)


@profile_me
def avro_view(request):
    data = DataSource().data
    buffer = BytesIO()

    schema = SchemaFromJSONData(avro_api_schema)
    writer = DatumWriter(schema)
    encoder = BinaryEncoder(buffer)
    writer.write(data, encoder)

    return HttpResponse(buffer.getvalue(), content_type='application/octet-stream')


@profile_me
def protobuf_view(request):
    response = api_pb2.Response()
    for data in DataSource().data:
        item = response.items.add()
        for key, val in data.items():
            setattr(item, key, val)

    return HttpResponse(response.SerializeToString(), content_type='application/octet-stream')

