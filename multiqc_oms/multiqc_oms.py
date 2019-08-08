from multiqc.utils import config


def load_config():
    my_search_patterns = {
        'dupradar': {'fn': '*.markDups_duprateExpDensCurve.txt'},
        'expCorr': {'fn': 'log2CPM_sample_cor.csv'},
        'stringtie': {'fn': '*.tmap'}
    }
    config.update_dict(config.sp, my_search_patterns)
