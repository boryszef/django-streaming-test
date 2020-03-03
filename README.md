### Benchmark of JSON API, AVRO and Protobuf

This repo contains a benchmark of two binary formats that can be used to stream large amount of data from Django API -
Apache's Avro and Google's Protobuf. I am comparing them against pure JSON.

There are three endpoints:
- /drf
- /avro
- /pb
serving the same data - list of dicts containing one number and one text value.

## Results of the benchmark

With 500.000 items in the list, the size of the transferred data is as follows:
- Avro: 7,880,638 bytes
- Protobuf: 9,372,378 bytes
- JSON: 19,277,781 bytes

The time spent to generate the response is the following:
- JSON: 0.002 s
- Protobuf: 1.234 s
- Avro: 24.609 s

Based on this very simple test, Avro's output seems to be slightly more compact at the price of much higher
generation time. Protobuf, on the other hand, offers better size to speed ratio.

## How to re-run the test

The benchmark uses standard django's testing framework:
```shell script
./manage.py test
```

