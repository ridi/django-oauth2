from setuptools import setup, find_packages

version = '0.0.1'

with open('requirements/base.txt') as f:
    install_requires = [line for line in f if line and not line.startswith('-')]


setup(
    ## temporary
    name='django-shard-library',

    version=version,

    ## temporary
    url='https://github.com/ridi/djang-shard-library',

    license='MIT',
    description='RIDI Python OAuth2 Library',
    keywords=['oauth2', 'ridi', 'ridibooks'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',

        'License :: OSI Approved :: MIT License',
        'Framework :: Django :: 2.0',
        'Programming Language :: Python :: 3.6',
    ],
    packages=find_packages(exclude=('tests', 'docs',)),
    install_requires=install_requires,
    include_package_data=True,
)
