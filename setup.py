from setuptools import find_packages, setup

version = '0.0.7'

with open('requirements/base.txt') as f:
    install_requires = [line for line in f if line and not line.startswith('-')]


setup(
    name='ridi-django-oauth2',
    version=version,
    url='https://github.com/ridi/django-oauth2',
    license='MIT',
    description='RIDI Django OAuth2 Library',
    keywords=['oauth2', 'oauth2-resource', 'ridi', 'ridibooks'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',

        'License :: OSI Approved :: MIT License',
        'Framework :: Django :: 2.0',
        'Programming Language :: Python :: 3.6',
    ],
    packages=find_packages(exclude=["tests.*", "tests"]),
    install_requires=install_requires,
    include_package_data=True,
)
