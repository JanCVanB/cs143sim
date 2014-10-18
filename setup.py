'''The cs143sim setuptools installation configuration
'''
import codecs
import os

import setuptools

import cs143sim


HERE = os.path.abspath(os.path.dirname(__file__))
with codecs.open(os.path.join(HERE, 'README.rst'), encoding='utf-8') as f:
    README = f.read()

setuptools.setup(
    author="H. Lan, Y. Ou, S. Richerd, J. Van Bruggen, J. Zhang",
    author_email='cs143-project@googlegroups.com',
    description='Simulator for operation of an abstract communication network (Caltech CS/EE 143, Fall 2014)',
    name=cs143sim.__name__,
    url='https://github.com/jvanbrug/cs143sim',
    version=cs143sim.__version__,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Education',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Communications :: Internet Phone',
        'Topic :: Education',
        'Topic :: Internet',
        'Topic :: Scientific/Engineering',
    ],
    install_requires=['simpy==3.0.5'],
    keywords='caltech cs143 abstract network architecture protocol simulator simulation simpy',
    license='MIT',
    long_description=README,
    packages=setuptools.find_packages(exclude=['docs', 'tests']),
    package_data={
    },
    entry_points={
    },
)
