#!/usr/bin/env python

""" MultiQC module to parse output from HISAT2 """

from __future__ import print_function
from collections import OrderedDict
import os
import logging
import pandas as pd

from multiqc import config
from collections import Counter
from multiqc.plots import bargraph
from multiqc.modules.base_module import BaseMultiqcModule

# Initialise the logger
log = logging.getLogger(__name__)


class MultiqcModule(BaseMultiqcModule):
    """ stringtie assembly module. """

    def __init__(self):

        # Initialise the parent object
        super(MultiqcModule, self).__init__(name="StringTie", anchor="stringtie",
                                            href='https://ccb.jhu.edu/software/stringtie/',
                                            info=" is a fast and highly efficient assembler of RNA-Seq alignments into potential transcripts. ")

        # Find and load any HISAT2 reports
        self.stringtie_data = dict()
        for f in self.find_log_files('stringtie', filehandles=False, filecontents=False):
            self.parse_stringtie_logs(f)

        # Filter to strip out ignored sample names
        self.stringtie_data = self.ignore_samples(self.stringtie_data)

        if len(self.stringtie_data) == 0:
            raise UserWarning

        log.info("Found {} reports".format(len(self.stringtie_data)))

        # Write parsed report data to a file
        self.write_data_file(self.stringtie_data, 'multiqc_dupradar')

        # assembly Plot
        self.stringtie_plot()

    def parse_stringtie_logs(self, f):
        """
        """

        s_name = f['s_name']
        f_file = os.path.join(f['root'], f['fn'])
        f_df = pd.read_csv(f_file, sep='\t')
        self.add_data_source(f, s_name)
        self.stringtie_data[s_name] = dict(Counter(f_df.class_code))

    def stringtie_plot(self):
        """ Make the HighCharts HTML to plot stringtie assembly. """

        # Split the data into SE and PE
        pconfig = {
            'title': 'StringTie assemblies',
            'ylab': 'Transcripts number',
            'cpswitch_counts_label': 'Number of Transcripts',
        }
        self.add_section(
            description='This plot shows the different type of transcripts assembled for each sample.',
            plot=bargraph.plot(self.stringtie_data, pconfig=pconfig)
        )
