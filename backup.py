import os
import os.path
import datetime
import shutil
import time
import argparse


def CopyDirectory(srcpath, backuppath, audit, verbose):
    for fname in os.listdir(srcpath):
        if (verbose):
            print("inspecting: ", os.path.join(srcpath, fname), " against: ", os.path.join(backuppath, fname))
        if (os.path.isdir(os.path.join(srcpath,fname))):
            CopyDirectory(os.path.join(srcpath,fname), os.path.join(backuppath,fname), audit, verbose)
        else:
            CopyIfNewer(os.path.join(srcpath,fname), fname, backuppath, audit, verbose)

def CopyIfNewer(srcfile, filename, backuppath, audit, verbose):
    if (not os.path.exists(backuppath)):
        os.makedirs(backuppath)
        if (verbose):
            print("created mirrored backup folder: ", backuppath)
    if (not os.path.exists(os.path.join(backuppath,filename))):
        shutil.copy(srcfile, os.path.join(backuppath,filename))
        if (audit):
            print("copied:", srcfile)
    else:
        if (verbose):
            print("comparing: ", srcfile, " ", os.path.join(backuppath, filename))
        s_time = os.path.getmtime(srcfile)
        b_time = os.path.getmtime(os.path.join(backuppath,filename))
        s_timestamp = datetime.datetime.fromtimestamp(s_time)
        b_timestamp = datetime.datetime.fromtimestamp(b_time)
        if (verbose):
            print("s: ", s_timestamp, " b: ", b_timestamp)
        if (s_timestamp > b_timestamp):
            shutil.copy(srcfile, os.path.join(backuppath,filename))
            if (audit):
                print("copied: ", srcfile)


def __main__():
    parser = argparse.ArgumentParser(prog="Backup Tool", description="backups files based on modify time")
    parser.add_argument("sourcedir", type=str)
    parser.add_argument("backupdir", type=str)
    parser.add_argument("-v", "--verbose", action='store_true')
    parser.add_argument("-a", "--audit", action='store_true')
    args = parser.parse_args()

    SOURCE_ROOT = os.path.abspath(args.sourcedir)
    BACKUP_ROOT = os.path.abspath(args.backupdir)

    print("Beginning backup of: ", SOURCE_ROOT, " to: ", BACKUP_ROOT, " -v:", args.verbose, " -a:", args.audit)

    CopyDirectory(SOURCE_ROOT, BACKUP_ROOT, args.audit, args.verbose)

__main__()