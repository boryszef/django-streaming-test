import cProfile
import io
import pstats


class DataSource(object):

    _size = 500000
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


def profile_me(func):
    def wrapper(*args, **kwargs):
        profiler = cProfile.Profile()
        profiler.enable()
        output = func(*args, **kwargs)
        profiler.disable()
        ps = pstats.Stats(profiler).sort_stats('cumulative')
        ps.print_stats(3)
        return output
    return wrapper