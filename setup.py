#!/usr/bin/env python
"""
MultiQC-oms is a plugin for MultiQC, providing additional tools which are
specific to OMS.

"""

from setuptools import setup, find_packages

version = '0.6'

setup(
    name='multiqc_oms',
    version=version,
    author='Lx Gui',
    author_email='guilixuan@gmail.com',
    description="MultiQC plugin for the OMS",
    long_description=__doc__,
    keywords='bioinformatics',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'couchdb',
        'simplejson',
        'pyyaml',
        'requests',
        'multiqc'
    ],
    entry_points={
        'multiqc.modules.v1': [
            'dupradar = multiqc_oms.modules.dupradar:MultiqcModule',
            'expCorr = multiqc_oms.modules.expCorr:MultiqcModule',
            'stringtie = multiqc_oms.modules.stringtie:MultiqcModule',
            'diffNum = multiqc_oms.modules.diffNum:MultiqcModule',
            'enrichNum = multiqc_oms.modules.enrichNum:MultiqcModule',
        ],
        'multiqc.templates.v1': [
            'oms = multiqc_oms.templates.oms',
        ],
        'multiqc.hooks.v1': [
            'before_config = multiqc_oms.multiqc_oms:load_config',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: JavaScript',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Scientific/Engineering :: Visualization',
    ],
)
