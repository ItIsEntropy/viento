from setuptools import setup

setup(
    name='viento',
    version= '0.0.0',
    description='A weather API for weather forecasts',
    long_description='''
    ''',
    author='ItIsEntropy',
    author_email='entropy@e.com',
    py_modules= [],
    license= 'Apache2.0',
    platforms=['win32', 'linux', 'unix', 'bsd', 'darwin'],
    entry_points = {
        'viento.log_handlers': [],
        'viento.file_lockers' : [],
    }
)