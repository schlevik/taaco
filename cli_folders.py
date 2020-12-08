import subprocess
import tempfile
import zipfile
import click
import os
from configparser import ConfigParser, NoOptionError
# noinspection PyUnresolvedReferences
from taaco import main

item_order_cfg = ['all', 'content', 'function', 'noun', 'pronoun', 'argument', 'verb', 'adj', 'adv', 'sentence',
                  'paragraph', 'adjacent', 'adjacent2', 'ttr', 'connectives', 'givenness', 'lsa', 'lda', 'word2vec',
                  'synonym-overlap', 'n-grams']
item_order_diagnostics_cfg = ['output-diag', 'output-tagged']
item_order_source_cfg = ['key-item-overlap', 'lsa', 'lda', 'word2vec']




@click.command()
@click.option('--indir')
@click.option('--outfile')
@click.option('--source-text', default='')
@click.option('--config', default='taaco.ini')
@click.option('--working-dir', default='.')
def cli_folders(indir, outfile, source_text, config, working_dir):
    directory_to_extract_to = os.path.join(os.path.dirname(__file__),'resources')
    if not os.path.exists(directory_to_extract_to):
        print("Unzipping resources...")
        with zipfile.ZipFile(os.path.join(os.path.dirname(__file__),'resources.zip'), 'r') as the_zip_file:
            the_zip_file.extractall(os.path.join(os.path.dirname(__file__)))
    
    cfg = ConfigParser()
    cfg.read(config)
    items =  [int(cfg.getboolean('Cohesion', item)) for item in item_order_cfg]
    items.extend(int(cfg.getboolean('Diagnostics', item)) for item in item_order_diagnostics_cfg)
    items_source = [int(cfg.getboolean('Source Similarity', item)) for item in item_order_source_cfg]
    print("Config:")
    for name, item in zip(item_order_cfg + item_order_diagnostics_cfg, items):
        print(f"{name}: {item}")
    for name, item in zip(item_order_source_cfg, items_source):
        print(f"{name}: {item}")
    main(indir, outfile, source_text, items, items_source, working_dir)




if __name__ == '__main__':
    cli_folders()
