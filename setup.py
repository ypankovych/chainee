from distutils.core import setup

version = "1.0"
setup(
    name='chainee',
    packages=['chainee'],
    version=version,
    license='MIT',
    description='Chain your predicates, easy way.',
    author='Yaroslav Pankovych',
    author_email='flower.moor@gmail.com',
    url='https://github.com/ypankovych/chainee',
    download_url=f'https://github.com/ypankovych/chainee/archive/refs/tags/{version}.tar.gz',
    keywords=['chain', 'easy', 'predicate'],
    long_description=__doc__,
    Install_requires=["anytree"],
    classifiers=[
        'Topic :: Utilities',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'Development Status :: 5 - Production/Stable',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: Implementation :: CPython'
    ],
)