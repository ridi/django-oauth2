from setuptools import find_packages, setup

version = '0.0.15'

# When the project is installed by pip, this is the specification that is used to install its dependencies.
install_requires = [
    "djangorestframework>=3.7.7",
    "django>=2.2.1",
    "PyJWT>=1.6.1",
    "requests>=2.20.0",
]

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
