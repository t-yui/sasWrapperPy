#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys
import configparser
import argparse
import subprocess
from logzero import logger


def argParse():
    parser = argparse.ArgumentParser(
                add_help=True
                )
    parser.add_argument(
        '-i',
        '--input',
        dest='infile',
        type=str
        )
    parser.add_argument(
        '-l',
        '--log',
        default='',
        dest='logfile',
        type=str
        )
    parser.add_argument(
        '-o',
        '--output',
        default='',
        dest='outfile',
        type=str
        )
    parser.add_argument(
        '-s',
        '--splash',
        action='store_true',
        default=False
        )
    parser.add_argument(
        '-d',
        '--dat',
        default=False,
        action='store_true',
        dest="dat"
        )
    args = parser.parse_args()
    return args


def confParse():
    config = configparser.ConfigParser()
    path = os.path.dirname(os.path.abspath(__file__))
    config.read(path + '/sas.ini')
    return config


def sasExec(sas_path, infile, logfile, outfile, splash):
    cmd = sas_path + '/sas.exe ' \
            + ' -SYSIN ' + infile \
            + ' -LOG ' + logfile \
            + ' -PRINT ' + outfile
    if not splash:
        cmd = cmd + ' -NOSPLASH'
    os.system(cmd)


def convertSASDATtoCSV(sas_path, infile, logfile, outfile, splash):
    infile_linux = convertPath(infile, w_to_l=False)
    infile_base = os.path.basename(infile_linux)
    infile_name, ext = os.path.splitext(infile_base)
    outfile_name = getCurrentDir() + '/' + infile_name + '.csv'
    outfile_name = convertPath(outfile_name)

    try:
        os.mkdir('./tmp_convert')
    except:
        pass

    cmd = 'echo \"' \
            + 'data ' + infile_name + '; ' \
            + 'set \'' + infile.replace('\\', '\\\\') + '\'; run; ' \
            + 'proc export data = ' + infile_name + ' ' \
            + 'outfile = \'' + outfile_name.replace('\\', '\\\\') + '\' ' \
            + 'dbms = csv replace; run; \"' \
            + '> ./tmp_convert/convert.sas'
    os.system(cmd)
    conv_prog = convertPath(getCurrentDir() + '/tmp_convert/convert.sas')
    if logfile == getCurrentDir():
        logfile = logfile + '/tmp_convert/convert.log'
    sasExec(sas_path,
            conv_prog,
            logfile,
            outfile,
            splash)
    try:
        os.system('rm -rf ./tmp_convert')
    except:
        pass


def convertPath(path, w_to_l=True):
    if w_to_l:
        cmd = 'wslpath -w ' + str(path)
    else:
        cmd = 'wslpath -u ' + str(path)
    path = subprocess.check_output(cmd, shell=True)
    path = str(path).strip('b').strip('\'').strip('\\n')
    return path


def getCurrentDir():
    cur_dir = subprocess.check_output('pwd', shell=True)
    cur_dir = str(cur_dir).strip('b').strip('\'').strip('\\n')
    return cur_dir


if __name__ == '__main__':
    args = argParse()
    config = confParse()

    # get arguments and configs
    sas_path = config['GENERAL']['sas_path']
    infile = convertPath(args.infile)
    logfile = args.logfile
    outfile = args.outfile
    splash = args.splash
    dat = args.dat

    # initialize
    if logfile == '':
        logfile = convertPath(
                    getCurrentDir()
                    )
    if outfile == '':
        outfile = convertPath(
                    getCurrentDir()
                    )

    # sas execute section
    if dat:
        try:
            convertSASDATtoCSV(sas_path, infile, logfile, outfile, splash)
            logger.info('SAS data was converted Successfully.')
        except Exception as e:
            logger.error(e)
            sys.exit(1)
    else:
        try:
            sasExec(sas_path, infile, logfile, outfile, splash)
            logger.info('SAS program was executed.')
        except Exception as e:
            logger.error(e.args)
            sys.exit(1)
