"""Setup configuration for pizza ordering system."""

from setuptools import setup, find_packages

setup(
    name="pizza-ordering-system",
    version="1.0.0",
    description="A comprehensive pizza ordering application built with TDD methodology",
    author="Lateef Mumin",
    author_email="lmumin@jhu.edu",
    packages=find_packages(),
    package_dir={"": "."},
    python_requires=">=3.11",
    install_requires=[
        "pytest>=7.0.0",
        "pytest-cov>=4.0.0",
        "pytest-html>=3.0.0",
        "sphinx>=5.0.0",
        "sphinx-rtd-theme>=1.0.0",
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Testing",
    ],
)