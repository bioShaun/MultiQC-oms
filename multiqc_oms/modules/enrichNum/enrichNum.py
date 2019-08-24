#!/usr/bin/env python

""" MultiQC module to parse output from HISAT2 """


from __future__ import print_function
import os
import json
import logging
from multiqc.modules.base_module import BaseMultiqcModule
from multiqc.plots import bargraph, linegraph

# Initialise the logger
log = logging.getLogger(__name__)


class MultiqcModule(BaseMultiqcModule):
    """ Show Number of diff genes. """

    def __init__(self):

        # Initialise the parent object
        super(MultiqcModule, self).__init__(name="Enrichment analysis", anchor="enrichNum",
                                            info=" is applied to differential expressed genes using "
                                            "<a href='https://bioconductor.org/packages/release/bioc/html/goseq.html' target='_blank'>goseq</a> "
                                            "and <a href='http://kobas.cbi.pku.edu.cn/' target='_blank'>KOBAS</a>."
                                            "Top 20 Enriched KEGG Pathways and GO terms were selected to show in the report.")

        self.kegg_dict = dict()
        for n, f in enumerate(
                self.find_log_files(
                    'enrichNum/kegg',
                    filecontents=False,
                    filehandles=False)):
            if n > 0:
                raise ValueError('more than one kegg summary found.')
            kegg_file = os.path.join(f['root'], f['fn'])
            self.kegg_dict = json.load(open(kegg_file))
            self.write_data_file({'kegg': f}, 'multiqc_enrichNum_kegg')

        if len(self.kegg_dict) == 0:
            raise UserWarning
        else:
            self.add_section(
                name='KEGG Pathway',
                anchor='enrichNum-kegg',
                plot=self.enrich_num_chart('enrichNum_kegg_plot',
                                           'Top Enriched KEGG Pathways',
                                           self.kegg_dict))

        self.go_dict = dict()
        for n, f in enumerate(
                self.find_log_files(
                    'enrichNum/go',
                    filecontents=False,
                    filehandles=False)):
            if n > 0:
                raise ValueError('more than one go summary found.')
            go_file = os.path.join(f['root'], f['fn'])
            self.go_dict = json.load(open(go_file))
            self.write_data_file({'go': f}, 'multiqc_enrichNum_go')

        if len(self.go_dict) == 0:
            raise UserWarning
        else:
            self.add_section(
                name='GO',
                anchor='enrichNum-go',
                plot=self.enrich_num_chart('enrichNum_go_plot',
                                           'Top Enriched GO Terms',
                                           self.go_dict))

    def enrich_num_chart(self, plot_id, plot_title, plot_data):

        # Config for the plot
        pconfig = {
            'id': plot_id,
            'title': plot_title,
            'ylab': '-log10(Corrected P-value)',
            'stacking': None,
            'cpswitch': False,
            'tt_percentages': False,
            'tt_decimals': 2,
        }
        return bargraph.plot(plot_data, pconfig=pconfig)
