from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='PyPrintful',
    version='1.0.0a6',
    description='A Python3 wrapper for the Printful.com API.',
    long_description=long_description,
    url='https://github.com/559Labs/pyPrintful',
    author='559 Labs',
    author_email='hello@559labs.com',
    license='Apache',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Framework :: Django',
        'Framework :: Django :: 1.10',
        'Intended Audience :: Developers',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Natural Language :: English',
        'Operating System :: OS Independent',
    ],
    keywords='api python3 dtg ondemand printing',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=['requests', 'pytz'],
    extras_require={
        'dev': ['check-manifest', 'twine', 'Sphinx'],
        'test': ['coverage', 'nose'],
    },
)
