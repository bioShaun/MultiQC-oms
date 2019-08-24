from multiqc.utils import config


def load_config():
    my_search_patterns = {
        'dupradar': {'fn': '*.markDups_duprateExpDensCurve.txt'},
        'expCorr': {'fn': 'log2CPM_sample_cor.csv'},
        'stringtie': {'fn': '*.tmap'},
        'diffNum/diff_bar': {'fn': 'diff.genes.compare.csv'},
        'diffNum/diff_matrix': {'fn': 'diff.genes.matrix.csv'},
        'enrichNum/kegg': {'fn': 'top.kegg.enrich.json'},
        'enrichNum/go': {'fn': 'top.go.enrich.json'},
    }
    config.update_dict(config.sp, my_search_patterns)
