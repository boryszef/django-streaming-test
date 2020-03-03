# Benchmark of JSON API, AVRO and Protobuf

This repo contains a benchmark of two binary formats that can be used to stream large amount of data from Django API -
Apache's Avro and Google's Protobuf. I am comparing them against pure JSON.

There are three endpoints:
- /drf
- /avro
- /pb
serving the same data - list of dicts containing one number and one text value.

## What are Protobuf and Avro?

Both protocols allow to serialize data into binary format using pre-defined schema. For more details see:
https://avro.apache.org/docs/current/ and https://developers.google.com/protocol-buffers/docs/pythontutorial

## Results of the benchmark

With 500.000 items in the list, the size of the transferred data is as follows:

| Format   | Size [bytes] |
|----------|-------------:|
| Avro     | 7,880,638    |
| Protobuf | 9,372,378    |
| JSON     | 19,277,781   |

The time spent to generate the response is the following:

| Format   | Time [s] |
|----------|---------:|
| JSON     | 0.002    |
| Protobuf | 1.234    |
| Avro     | 24.609   |

Based on this very simple test, Avro's output seems to be slightly more compact at the price of much higher
generation time. Protobuf, on the other hand, offers better size to speed ratio.

## How to re-run the test

The benchmark uses standard django's testing framework:
```shell script
./manage.py test
```

