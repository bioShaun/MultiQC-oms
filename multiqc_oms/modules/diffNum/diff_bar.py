#!/usr/bin/env python

""" MultiQC submodule to parse output from diff number table"""

import os
from collections import OrderedDict
import logging
import pandas as pd

from multiqc.plots import bargraph

# Initialise the logger
log = logging.getLogger(__name__)


def parse_reports(self):
    """ Find diff number table and parse their data """

    # Set up vars
    self.diff_num = dict()

    # Go through files and parse data using regexes
    for n, f in enumerate(
            self.find_log_files(
                'diffNum/diff_bar', filehandles=False, filecontents=False)):
        if n > 0:
            raise ValueError('more than one diff number table found.')
        self.diff_num['table'] = f

    if len(self.diff_num) == 0:
        raise UserWarning

    self.write_data_file(self.diff_num, 'multiqc_diffNum_bar')
    diff_num_file = os.path.join(
        self.diff_num['table']['root'], self.diff_num['table']['fn'])
    diff_num_df = pd.read_csv(diff_num_file, index_col=0)
    plot_data = OrderedDict()
    for idx_i in diff_num_df.index:
        plot_data[idx_i] = {'up-regulated': diff_num_df.loc[idx_i].up,
                            'down-regulated': diff_num_df.loc[idx_i].down}

    pconfig = {
        'title': 'Differential Expressed Genes',
        'cpswitch_counts_label': 'Number of Genes',
    }

    self.add_section(
        description=('This plot shows the Differential expressed gene number'
                     ' for each compare.'),
        plot=bargraph.plot(plot_data, pconfig=pconfig)
    )

    # Return number of compares found
    return len(plot_data)
