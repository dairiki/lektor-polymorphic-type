# -*- coding: utf-8 -*-
import ast
import io
import re
from setuptools import setup

with io.open('README.md', 'rt', encoding="utf8") as f:
    readme = f.read()

_description_re = re.compile(r'description\s+=\s+(?P<description>.*)')
with open('lektor_deferred_type.py', 'rb') as f:
    description = str(ast.literal_eval(_description_re.search(
        f.read().decode('utf-8')).group(1)))


setup(
    author='Jeff Dairiki',
    author_email='dairiki@dairiki.org',
    description=description,
    keywords='Lektor plugin',
    license='MIT',
    license_file='LICENSE',
    long_description=readme,
    long_description_content_type='text/markdown',
    name='lektor-deferred-type',
    py_modules=['lektor_deferred_type'],
    url='https://github.com/dairiki/lektor-deferred-type',
    version='0.1b1',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Plugins',
        'Environment :: Web Environment',
        'Framework :: Lektor',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    entry_points={
        'lektor.plugins': [
            'deferred-type = lektor_deferred_type:DeferredTypePlugin',
        ]
    }
)
