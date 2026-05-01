#!/usr/bin/env python3
"""
Setup script for eventraisers package
This is provided as a fallback for older build systems.
Modern builds should use pyproject.toml.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="eventraisers",
    version="1.0.0",
    author="Pac-Dessert1436",
    description="A lightweight Python package for dynamically generating event decorators and trigger functions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Pac-Dessert1436/py-event-raiser-generator",
    packages=find_packages(include=["eventraisers", "eventraisers.*"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Typing :: Typed",
    ],
    python_requires=">=3.9",
    package_data={
        "eventraisers": ["py.typed"],
    },
    zip_safe=False,
)