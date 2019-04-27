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
        type=str,
        required=True
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
    args = parser.parse_args()
    return args


def confParse():
    config = configparser.ConfigParser()
    path = os.path.dirname(sys.argv[0])
    config.read(path + '/sas.ini')
    return config


def sasExec(sas_path, infile, logfile, outfile):
    # convert path from linux to windows
    infile = convertPath(infile)
    logfile = convertPath(logfile)
    outfile = convertPath(outfile)

    # sas execution
    cmd = sas_path + '/sas.exe ' \
        + ' -SYSIN ' + infile \
        + ' -LOG ' + logfile \
        + ' -PRINT ' + outfile \
        + ' -NOSPLASH'
    os.system(cmd)


def convertSASDATtoCSV(sas_path, infile, logfile, outfile):
    infile_base = os.path.basename(infile)
    infile_name, ext = os.path.splitext(infile_base)
    infile = convertPath(infile)
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
            outfile,)
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


def convertEncode(txtfile, sjis_to_utf8=True):
    if sjis_to_utf8:
        _from = 'sjis'
        _to = 'utf-8'
    else:
        _from = 'utf-8'
        _to = 'sjis'
    cmd = 'iconv' \
        + ' -f ' + _from \
        + ' -t ' + _to \
        + ' ' + txtfile \
        + ' -o ' + txtfile \
        + ' >/dev/null 2>&1'
    try:
        subprocess.check_call(cmd, shell=True)
        msg = txtfile + ' : Encoding was converted' \
            + ' from ' + _from \
            + ' to ' + _to
        logger.info(msg)
    except:
        msg = txtfile + ' : Encoding was not converted.'
        logger.warning(msg)


if __name__ == '__main__':
    args = argParse()
    config = confParse()

    # get arguments and configs
    sas_path = config['GENERAL']['sas_path']
    infile = args.infile
    logfile = args.logfile
    outfile = args.outfile

    # get ext information of infile
    infile_base = os.path.basename(infile)
    infile_name, ext = os.path.splitext(infile_base)
    infile_root, infile_ext = os.path.splitext(infile)

    # initialize path
    if logfile == '':
        logfile = getCurrentDir() \
                + '/' + infile_name \
                + '.log'
    if outfile == '':
        outfile = getCurrentDir() \
                + '/' + infile_name \
                + '.lst'

    # sas execute section
    if infile_ext == '.sas7bdat':
        try:
            convertSASDATtoCSV(sas_path,
                               infile,
                               logfile,
                               outfile)
            msg = 'SAS data was converted to CSV.'
            logger.info(msg)
        except Exception as e:
            logger.error(e)
            sys.exit(1)
    elif infile_ext == '.sas':
        try:
            sasExec(sas_path,
                    infile,
                    logfile,
                    outfile)
            convertEncode(logfile)
            if os.path.exists(outfile):
                convertEncode(outfile)
            msg = 'SAS program was executed.'
            logger.info(msg)
        except Exception as e:
            logger.error(e)
            sys.exit(1)
    else:
        err_msg = 'Specify .sas or .sas7bdat file for "-i" option.'
        logger.error(err_msg)
        sys.exit(1)
