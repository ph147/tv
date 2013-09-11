from setuptools import setup

dependencies = [
    'lxml'
]

setup(
    name = 'tv',
    author = 'me',
    description = 'Watch tv series from free-tv-video-online.me',
    install_requires = dependencies,
    license = 'MIT',
    packages = ['tv'],
)
