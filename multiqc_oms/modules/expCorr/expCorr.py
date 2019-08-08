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
    """ dupradar module. """

    def __init__(self):

        # Initialise the parent object
        super(MultiqcModule, self).__init__(name="Sample Correlation", anchor="expCorr",
                                            info=" is generated from normalised gene counts through "
                                            "<a href='https://bioconductor.org/packages/release/bioc/html/edgeR.html' target='_blank'>edgeR</a>.")

        # Find and load correlation matrix
        self.cor_data = dict()
        for n, f in enumerate(self.find_log_files('expCorr', filehandles=False, filecontents=False)):
            if n > 0:
                raise ValueError('more than one correlation matrix found.')
            self.cor_data['correlation'] = f

        if len(self.cor_data) == 0:
            raise UserWarning

        log.info("Found {} reports".format(len(self.cor_data)))

        # Write parsed report data to a file
        self.write_data_file(self.cor_data, 'multiqc_expCorr')
        heatmap_name, heatmap_val = self.parse_corr_matrix()
        # correlation heatmap
        self.cor_heatmap_plot(heatmap_name, heatmap_val)

    def parse_corr_matrix(self):
        """
        """
        f = self.cor_data['correlation']
        cor_file = os.path.join(f['root'], f['fn'])
        cor_df = pd.read_csv(cor_file, index_col=0)
        heatmap_name = list(cor_df.columns)
        heatmap_val = [list(cor_df.loc[i]) for i in cor_df.index]
        return heatmap_name, heatmap_val

    def cor_heatmap_plot(self, heatmap_name, heatmap_val):
        """ Make the HighCharts HTML to plot sample correlation heatmap. """

        # Split the data into SE and PE
        pconfig = {
            'title': 'Pearson correlation',
            'xlab': True,
        }
        self.add_section(
            description='Pearson correlation between log<sub>2</sub> normalised CPM values are calculated and clustered.',
            plot=heatmap.plot(heatmap_val, heatmap_name, pconfig=pconfig)
        )
