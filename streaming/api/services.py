class DataSource(object):

    _size = 1000
    _data = None

    def __init__(self):
        if DataSource._data is None:
            DataSource._data = self._generate()

    @property
    def data(self):
        return self._data

    def _generate(self):
        return [
            {
                'text': 'value{}'.format(idx),
                'number': idx
            }
            for idx in range(self._size)
        ]
