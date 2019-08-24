#!/usr/bin/env python

""" MultiQC module to parse output from HISAT2 """

from __future__ import print_function
from collections import OrderedDict
import os
import logging
import pandas as pd


from multiqc import config
from multiqc.plots import heatmap
from multiqc.modules.base_module import BaseMultiqcModule

# Initialise the logger
log = logging.getLogger(__name__)


class MultiqcModule(BaseMultiqcModule):
    """ Show Number of diff genes. """

    def __init__(self):

        # Initialise the parent object
        super(MultiqcModule, self).__init__(name="Differential analysis", anchor="diffNum",
                                            info=" is generated from normalised gene counts through "
                                            "<a href='https://bioconductor.org/packages/release/bioc/html/edgeR.html' target='_blank'>edgeR</a>.")

        n = dict()

        diff_num_sections = [
            'diff_bar',
            'diff_matrix',
        ]

        for sm in diff_num_sections:
            try:
                module = __import__(
                    'multiqc_oms.modules.diffNum.{}'.format(sm), fromlist=[''])
                n[sm] = getattr(module, 'parse_reports')(self)
                if n[sm] > 0:
                    log.info("Found {} {} reports".format(n[sm], sm))
            except (ImportError, AttributeError, UserWarning):
                log.warn("Could not find diffNum Section '{}'".format(sm))

        # Exit if we didn't find anything
        if sum(n.values()) == 0:
            raise UserWarning
