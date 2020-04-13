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
    long_description=readme,
    long_description_content_type='text/markdown',
    name='lektor-deferred-type',
    py_modules=['lektor_deferred_type'],
    # url='[link to your repository]',
    version='0.1.dev0',
    classifiers=[
        'Framework :: Lektor',
        'Environment :: Plugins',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],
    entry_points={
        'lektor.plugins': [
            'deferred-type = lektor_deferred_type:DeferredTypePlugin',
        ]
    }
)
