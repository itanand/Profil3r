# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='Profil3r',
    version="1.3.11",
    packages=find_packages(),
    author="Anand Mohan",
    author_email="hey.itanand@gmail.com",
    install_requires=["pwnedpasswords", "requests", "PyInquirer", "jinja2", "argparse", "bs4"],
    description="Profil3r is an OSINT tool that allows you to find the differents social accounts and emails used by a person",
    include_package_data=True,
    url='https://github.com/itanand/Profil3r',
    classifiers=[
        "Programming Language :: Python",
    ],
    license='MIT'
)