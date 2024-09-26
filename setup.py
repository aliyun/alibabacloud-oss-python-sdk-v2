"""
setup module for Alibaba Cloud OSS SDK V2.
"""

import os
from setuptools import setup, find_packages

PACKAGE_NAME = "alibabacloud-oss-v2"
PACKAGE_FOLDER_PATH = PACKAGE_NAME.replace("-", "_")
DESCRIPTION = "Alibaba Cloud OSS (Object Storage Service) SDK V2 for Python"
AUTHOR = "Alibaba Cloud OSS SDK"
AUTHOR_EMAIL = "sdk-team@alibabacloud.com"
URL = "https://github.com/aliyun/alibabacloud-oss-python-sdk-v2"
VERSION = __import__(PACKAGE_FOLDER_PATH).__version__
REQUIRES = [
    "requests>=2.18.4",
    "cryptography>=2.1.4",
    "crcmod-plus>=2.1.0"
]

if not VERSION:
    raise RuntimeError('Cannot find version information')

LONG_DESCRIPTION = ''
if os.path.exists('./README.md'):
    with open("README.md", encoding='utf-8') as fp:
        LONG_DESCRIPTION = fp.read()

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license="Apache License 2.0",
    url=URL,
    keywords=["alibabacloud", "oss"],
    packages=find_packages(exclude=["tests*", "sample*"]),
    include_package_data=True,
    platforms="any",
    install_requires=REQUIRES,
    python_requires=">=3.8",
    classifiers=(
        'Development Status :: 4 - Beta',
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        'License :: OSI Approved :: Apache License 2.0',
    )
)
