#!/usr/bin/env python3
# coding=utf-8

import sys as sys
import os as os
import argparse as argp
import traceback as trb
import logging as log

import pandas as pd

__developer__ = 'Peter Ebert'
__dev_email__ = 'peter.ebert@iscb.org'
__version__ = '0.0.1'

__RAW_GITHUB_URL__ = 'https://raw.githubusercontent.com/deepPipelines'
__DEEP_DOC_REPO__ = 'deepDoc/master'
__DEEP_REF_REPO__ = 'deepReferences/master'
__CONTROL_VOCAB__ = os.path.join(__RAW_GITHUB_URL__, __DEEP_DOC_REPO__, 'vocabulary/deep_pipelines_terms.tsv')
__LOG_FORMAT__ = '%(asctime)s - %(levelname)s: %(message)s'


def parse_command_line():
    """
    :return:
    """
    parser = argp.ArgumentParser(prog='init_deep_pipeline.py', add_help=True)

    parser.add_argument('--version', '-v', action='version',
                        version='%(prog)s {}'.format(__version__))

    grp = parser.add_argument_group('Runtime behavior')
    grp.add_argument('--debug', '-dbg', action='store_true', default=False, dest='debug',
                     help='Print status messages to stderr. Default: False')
    grp.add_argument('--pipeline', '-p', dest='pipeline', type=str, default='test',
                     choices=['test', 'chipseq'],
                     help='Set the appropriate pipeline to initiate. "test" runs'
                          ' a few diagnostic tests w/o any side effects on the'
                          ' local environment.')
    grp.add_argument('--assembly', '-a', dest='assembly', type=str, default='',
                     help='Specify assembly version to use for this pipeline.'
                          ' Note that availability of reference bundles for'
                          ' this pipeline/assembly combination')

    grp = parser.add_argument_group('Pipeline local path')
    grp.add_argument('--work-dir', '-w', type=str, default=os.getcwd(),
                     help='Full path to pipeline working directory.'
                          ' All downloaded reference data will be'
                          ' stored under that path.')

    grp = parser.add_argument_group('deepPipelines remote paths')
    grp.add_argument('--deep-doc', '-doc', type=str, dest='docrepo',
                     default=os.path.join(__RAW_GITHUB_URL__, __DEEP_DOC_REPO__),
                     help='Path to remote repository storing information like'
                          ' accepted entity names (controlled vocabulary).')
    grp.add_argument('--vocabulary', '-voc', type=str, dest='vocabulary',
                     default=__CONTROL_VOCAB__,
                     help='Path to TSV file containing controlled vocabulary'
                          ' to be used throughout all DEEP pipelines.'
                          ' If possible, all terms should be extracted from'
                          ' EGA/SRA metadata schemes to ease later sample deposition.')
    grp.add_argument('--deep-ref', '-ref', type=str, dest='refrepo',
                     default=os.path.join(__RAW_GITHUB_URL__, __DEEP_REF_REPO__),
                     help='Path to remote repository storing reference bundle'
                          ' annotation for various genomic assemblies.')

    args = parser.parse_args()
    return args


def testing(args, logger):
    """
    :param args:
    :param logger:
    :return:
    """
    logger.debug('Running in test mode')
    voc = pd.read_csv(args.vocabulary, sep='\t', header=0)
    logger.debug('Successfully read controlled vocabulary sheet')

    return 0


def main(args, logger):
    """
    :param args:
    :param logger:
    :return:
    """
    return 0


if __name__ == '__main__':
    logger = None
    exc = 1
    try:
        args = parse_command_line()
        if args.debug:
            log.basicConfig(**{'stream': sys.stderr, 'level': log.DEBUG,
                               'format': __LOG_FORMAT__})
        else:
            log.basicConfig(**{'stream': sys.stderr, 'level': log.WARNING,
                               'format': __LOG_FORMAT__})
        logger = log.getLogger()
        if args.pipeline == 'test':
            exc = testing(args, logger)
        else:
            exc = main(args, logger)
    except Exception as ex:
        trb.print_exc()
        if logger is not None:
            logger.error('Properly handled shutdown upon error:\n\n{}'.format(ex))
        exc = 1
    finally:
        log.shutdown()
        sys.exit(exc)
