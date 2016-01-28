#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name="morseapi",
    version="0.0.1",
    description="Unofficial API for controlling Wonder Workshops Dot and Dash robots",
    author="Ilya Sukhanov",
    author_email="ilya@sukhanov.net",
    url="https://github.com/IlyaSukhanov/morseapi",
    entry_points={
        "console_scripts": [
            "moto_server = moto.server:main",
        ],
    },
    packages=find_packages(exclude=("tests", "tests.*")),
    install_requires=[
        "pygatt[GATTTOOL]",
        "colour",
        "pyRobots",
    ],
    setup_requires=[
      "coverage",
      "nose",
      "mock",
    ],
    package_data={"": ["LICENSE", "NOTICE"]},
    license=open("LICENSE").read(),
)
