from setuptools import setup


setup(
    name='undercrawler',
    packages=['undercrawler'],
    install_requires=[
        'autologin-middleware',
        'autopager>=0.2',
        'botocore',
        'Formasaurus[with_deps]>=0.8',
        'MaybeDont',
        'scrapy-cdr>=0.2.0',
        'scrapy-splash>=0.6',
        'scrapy>=1.1.0',
        'typing',
    ],
)
