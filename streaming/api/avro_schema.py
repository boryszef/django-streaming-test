avro_api_schema = {
    "namespace": "streaming.api",
    "name": "Response",
    "type": "array",
    "items": [
        {
            "name": "Item",
            "type": "record",
            "fields": [
                {"name": "text", "type": "string"},
                {"name": "number",  "type": "int"}
            ]
        }
    ]
}
