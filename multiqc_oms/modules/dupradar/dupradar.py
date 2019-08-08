#!/usr/bin/env python

""" MultiQC module to parse output from HISAT2 """

from __future__ import print_function
from collections import OrderedDict
import logging
import re
import json

from multiqc import config
from multiqc.plots import linegraph
from multiqc.modules.base_module import BaseMultiqcModule

# Initialise the logger
log = logging.getLogger(__name__)


class MultiqcModule(BaseMultiqcModule):
    """ dupradar module. """

    def __init__(self):

        # Initialise the parent object
        super(MultiqcModule, self).__init__(name="DupRadar", anchor="dupradar",
                                            href='https://bioconductor.org/packages/release/bioc/html/dupRadar.html',
                                            info=" provides duplication rate quality control for RNA-Seq datasets. "
                                            "Highly expressed genes can be expected to have a lot of duplicate reads, "
                                            "but high numbers of duplicates at low read counts can indicate low library "
                                            "complexity with technical duplication. ")

        # Find and load any HISAT2 reports
        self.dupradar_data = dict()
        for f in self.find_log_files('dupradar', filehandles=True):
            self.parse_dupradar_logs(f)

        # Filter to strip out ignored sample names
        self.dupradar_data = self.ignore_samples(self.dupradar_data)

        if len(self.dupradar_data) == 0:
            raise UserWarning

        log.info("Found {} reports".format(len(self.dupradar_data)))

        # Write parsed report data to a file
        self.write_data_file(self.dupradar_data, 'multiqc_dupradar')

        # Basic Stats Table
        # Report table is immutable, so just updating it works
        # self.hisat2_general_stats_table()

        # Alignment Rate Plot
        self.dupradar_plot()

    def parse_dupradar_logs(self, f):
        """
        """

        s_name = f['s_name']
        parsed_data = OrderedDict()

        for l in f['f']:
            if l[0] != '#':
                reads_kbp, dup_rate = l.strip().split()
                parsed_data[float(reads_kbp)] = float(dup_rate)
        self.add_data_source(f, s_name)
        self.dupradar_data[s_name] = parsed_data

    def dupradar_plot(self):
        """ Make the HighCharts HTML to plot gene duplication distributions. """

        # Split the data into SE and PE
        pconfig = {
            'title': 'DupRadar General Linear Model',
            'xLog': True,
            'xlab': 'expression (reads/kbp)',
            'ylab': '% duplicate reads',
            'ymax': 100,
            'ymin': 0,
            'tt_label': '<b>{point.x:.1f} reads/kbp</b>: {point.y:,.2f}% duplicates',
            'xPlotLines': [
                {
                    'color': 'green',
                    'dashStyle': 'LongDash',
                    'value': 0.5,
                    'width': 1,
                    'label': {
                        'style': {'color': 'green'},
                        'text': '0.5 RPKM',
                        'verticalAlign': 'bottom',
                        'y': -65,
                    }
                },
                {
                    'color': 'red',
                    'dashStyle': 'LongDash',
                    'value': 1000,
                    'width': 1,
                    'label': {
                        'style': {'color': 'green'},
                        'text': '1 read/bp',
                        'verticalAlign': 'bottom',
                        'y': -65,
                    }
                },
            ],

        }
        self.add_section(
            description='This plot shows the general linear models - a summary of the gene duplication distributions.',
            plot=linegraph.plot(self.dupradar_data, pconfig)
        )
