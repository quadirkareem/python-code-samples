
# ==============================================================================
# This script executes common git commands for multiple folders.
#
# author: Quadir Sha Kareemullah
# ==============================================================================

import os
import sys
import subprocess
import argparse
import logging
from datetime import datetime


# ------------------------------------------------------------------------------
# global variables
# ------------------------------------------------------------------------------
git_dir = '.git'
pom_file = 'pom.xml'
path_sep='/\\'
cwd = os.getcwd()
start_time = datetime.now()
log_file = 'git_utils_'+ start_time.strftime('%Y-%m-%d_%H-%M-%S') + '.log'
log_to_file=False


# ------------------------------------------------------------------------------
# parse command line arguments
# ------------------------------------------------------------------------------
'''
-f, --logfile: enable logging to file
-l <count>, --log <count>: print latest commits
-g, --debug: enable debug mode
-d, --dir: repositories base directory
-r, --repos: repositories list
-b, --branch: display current checked out branch name
-B, --branch-all: display all fetched branches
-p, --pull : pull
-P, --pull-all: pull all
-m, --mvn: execute maven build
-M, --mvn-offline: execute maven build in offline mode
-c <branch-name>, --checkout <branch-name>: checkout branch <branch-name>
-n <branch-name>, --new <branch-name>: create branch <branch-name>
'''
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dir',
                        dest='base_dir', default='.', metavar='<base_dir>',
                        help='repositories base directory')
    parser.add_argument('-r', '--repos',
                        dest='repo_list', nargs='+', metavar='<repo>',
                        help='repositories list')
    parser.add_argument('-b', '--branch', action='store_true',
                        dest='print_cur_branch',
                        help='display current checked out branch name')
    parser.add_argument('-B', '--branch-all', action='store_true',
                        dest='print_all_branches',
                        help='display all fetched branches names')
    parser.add_argument('-p', '--pull', action='store_true',
                        dest='pull',
                        help='pull from remote into current branch')
    parser.add_argument('-P', '--pull-all', action='store_true',
                        dest='pull_all',
                        help='fetch all remotes')
    parser.add_argument('-c', '--checkout',
                        dest='co_branch', metavar='<branch>',
                        help='checkout branch')
    parser.add_argument('-n', '--new',
                        dest='new_branch', metavar='<branch>',
                        help='create branch')
    parser.add_argument('-m', '--mvn', action='store_true',
                        dest='mvn_build',
                        help='execute maven build')
    parser.add_argument('-M', '--mvn-offline', action='store_true',
                        dest='mvn_build_offline',
                        help='execute maven build in offline mode')
    parser.add_argument('-l', '--log',
                        dest='print_commits', const='5', nargs='?', metavar='<count>',
                        help='print latest commits')
    parser.add_argument('-g', '--debug', action='store_const',
                        dest='log_level', const=logging.DEBUG, default=logging.INFO,
                        help='enable debug mode')
    parser.add_argument('-f', '--logfile', action='store_true',
                        dest='log_to_file',
                        help='enable logging to file')

    if len(sys.argv)==1:
        parser.print_help()
        sys.exit(1)

    return parser.parse_args()


# ------------------------------------------------------------------------------
# initialize logger
# ------------------------------------------------------------------------------
def init_logger(log_level):
    date_fmt = '%H:%M:%S'
    logging.basicConfig(level=log_level,
                    format='%(asctime)s: %(message)s',
                    datefmt=date_fmt,
                    handlers=[logging.StreamHandler()])
    if log_to_file:
        fileHandler = logging.FileHandler(log_file)
        fileHandler.setFormatter(
            logging.Formatter(
                fmt='%(asctime)s || %(levelname)-8s || %(message)s',
                datefmt=date_fmt)
                )
        logging.getLogger('').addHandler(fileHandler)


# ------------------------------------------------------------------------------
# format & log header
# ------------------------------------------------------------------------------
def log_hdr(hdr):
    logging.info('{:#<80}'.format(hdr + ' '))


# ------------------------------------------------------------------------------
# format & log sub-header
# ------------------------------------------------------------------------------
def log_sub_hdr(sub_hdr):
    logging.info('{:-<80}'.format(sub_hdr + ' '))


# ------------------------------------------------------------------------------
# converts seconds to hours, minutes & seconds
# ------------------------------------------------------------------------------
def secs_to_hms(seconds):
    seconds = round(seconds)
    hours = (seconds // 3600) % 24
    minutes = (seconds // 60) % 60
    seconds = seconds % 60
    return hours, minutes, seconds


# ------------------------------------------------------------------------------
# get absolute path
# ------------------------------------------------------------------------------
def get_abs_path(base_dir):
    if not os.path.isdir(base_dir):
       print('Directory "{}" does not exist !!!\nExiting'.format(base_dir))
       sys.exit(1)
    base_dir = os.path.abspath(base_dir)
    # remove trailing slash
    if base_dir[-1] in path_sep: base_dir = base_dir[:-1]
    return base_dir


# ------------------------------------------------------------------------------
# execute a shell command
# ------------------------------------------------------------------------------
def exec_cmd(cmd_args):
    log_sub_hdr('[ ' + ' '.join(cmd_args) + ' ]')

    process = subprocess.Popen(cmd_args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                shell=True, universal_newlines=True)
    with process.stdout:
        for line in iter(process.stdout.readline, ''):
            logging.info(line[:-1])
    exitcode = process.wait()


# ------------------------------------------------------------------------------
# get git repositories list
# ------------------------------------------------------------------------------
def get_git_repos(base_dir, repos_list):
    git_repos = {}
    if not repos_list:
        repos_list = os.listdir(base_dir)
    for item in repos_list:
        # remove trailing path separator
        if item[-1] in path_sep: item = item[:-1]
        # check if path is absolute
        if item[0] in path_sep or item[1] == ':':
            item_path = item
        else:
            item_path = base_dir + os.sep + item
        git_dir_path = item_path + os.sep + git_dir
        if os.path.isdir(item_path) and os.path.isdir(git_dir_path):
            git_repos[item] = item_path
    return git_repos


# ------------------------------------------------------------------------------
# get maven project paths
# ------------------------------------------------------------------------------
def get_mvn_paths(repo_path):
    mvn_paths = []
    for item in os.listdir(repo_path):
        item_path = repo_path + os.sep + item
        pom_path = item_path + os.sep + pom_file
        if os.path.isdir(item_path) and os.path.isfile(pom_path):
            mvn_paths.append(item_path)
    return mvn_paths


# ------------------------------------------------------------------------------
# execute maven install command
# ------------------------------------------------------------------------------
def mvn_build(mvn_paths, offline):
    if offline:
        mvn_cmd_args = ['mvn', '-o', 'clean', 'install', '-DskipTests' ]
    else:
        mvn_cmd_args = ['mvn', 'clean', 'install', '-DskipTests' ]
    for mvn_dir in mvn_paths:
        os.chdir(mvn_dir)
        exec_cmd(mvn_cmd_args)


# ------------------------------------------------------------------------------
# checkout git branch
# ------------------------------------------------------------------------------
def checkout_branch(branch_name):
    exec_cmd(['git', 'pull', '--all'])
    # prepend with obs/ if repo is ccsecure
    if 'ccsecure' in os.getcwd():
        branch_name = 'obs/' + branch_name
    exec_cmd(['git', 'checkout', branch_name])
    exec_cmd(['git', 'pull'])


# ------------------------------------------------------------------------------
# create git branch
# ------------------------------------------------------------------------------
def create_branch(branch_name):
    # prepend with obs/ if repo is ccsecure
    if 'ccsecure' in os.getcwd():
        branch_name = 'obs/' + branch_name
    exec_cmd(['git', 'checkout', '-b', branch_name])
    exec_cmd(['git', 'push', '--set-upstream', 'origin', branch_name])

# ------------------------------------------------------------------------------
# prints latest commits
# git log -<count> --pretty=format:"%ad%x09%an%x09%H%n  -- %s%n" --date=local
# ------------------------------------------------------------------------------
def print_commits(count):
    exec_cmd(['git', 'pull'])
    exec_cmd(['git', 'log', '-' + count, '--pretty=format:%ad%x09%an%x09%H%n  -- %s%n',
                '--date=local', '--author-date-order' ])


# ------------------------------------------------------------------------------
# MAIN
# ------------------------------------------------------------------------------
def main():
    global log_to_file
    cmd_args = parse_args()
    log_to_file = cmd_args.log_to_file
    init_logger(cmd_args.log_level)
    logging.info('CMD: %s', ' '.join(sys.argv))
    logging.debug('cmd_args=%s', cmd_args)
    base_dir = get_abs_path(cmd_args.base_dir)
    logging.info('Current directory: %s', cwd)
    logging.info('Base directory: %s', base_dir)

    git_repos = get_git_repos(base_dir, cmd_args.repo_list)
    logging.debug('git_repos=%s', git_repos)

    logging.info('')
    for dirname in sorted(git_repos):
        mvn_paths = get_mvn_paths(git_repos[dirname])

        log_hdr(dirname)

        os.chdir(git_repos[dirname])

        if cmd_args.print_all_branches:
            exec_cmd(['git', 'branch'])
        elif cmd_args.print_cur_branch:
            exec_cmd(['git', 'rev-parse', '--abbrev-ref', 'HEAD'])

        if cmd_args.pull_all:
            exec_cmd(['git', 'pull', '--all'])
        elif cmd_args.pull:
            exec_cmd(['git', 'pull'])

        if cmd_args.co_branch:
            checkout_branch(cmd_args.co_branch)
        elif cmd_args.new_branch:
            create_branch(cmd_args.new_branch)

        if cmd_args.print_commits:
            print_commits(cmd_args.print_commits)

        if cmd_args.mvn_build:
            mvn_build(mvn_paths, False)
        elif cmd_args.mvn_build_offline:
            mvn_build(mvn_paths, True)

        logging.info('')


def post_process():
    duration = datetime.now() - start_time
    (h, m, s) = secs_to_hms(duration.total_seconds())
    log_hdr('Execution Time: {:02d}h:{:02d}m:{:02d}s'.format(h, m, s))
    if log_to_file:
        print('\nLog file:', log_file)

# ------------------------------------------------------------------------------
# START
# ------------------------------------------------------------------------------
if __name__ == '__main__':
    main()
    post_process()
    sys.exit(0)
