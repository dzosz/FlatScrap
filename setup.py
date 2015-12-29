from setuptools import setup

setup(name='FlatScrap',
      version='0.2',
      description='Map of rooms for rent in Wroclaw',
      author='tom c.',
      author_email='tom_____@gmail.com',
      url='http://www.python.org/sigs/distutils-sig/',
      install_requires=['Flask', 'Redis', 'rq', 'geopy', 'requests'],
     )
