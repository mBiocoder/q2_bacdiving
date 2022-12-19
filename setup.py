# ----------------------------------------------------------------------------
# Copyright (c) 2016-2022, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

#!/usr/bin/env python3
import versioneer
from setuptools import setup, find_packages

setup(
    name="q2-bacdiving",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    packages=find_packages(),
    package_data={'q2_bacdiving': ['citations.bib']},
    author="Mahima Arunkumar",
    author_email="M.Arunkumar@campus.lmu.de",
    description="Accesses and retrieves information from the Bacterial Diversity Metadatabase BacDive.",
    license='BSD-3-Clause',
    url="https://qiime2.org",
    entry_points={
        'qiime2.plugins': ['q2-bacdiving=q2_bacdiving.plugin_setup:plugin']
    },
    zip_safe=False,
)
