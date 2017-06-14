# ==============================================================================
# This script creates git branch and updates pom version
'''
1. tag eg. b_1704.x
2. create branch eg. 1704.x
3. mvn clean, update pom version eg. 1704-obs,
4. update infra/commons properties
5. commit
6. push
'''
# author: Quadir Sha Kareemullah
# ==============================================================================

import os
import sys
import subprocess
import argparse
import logging
from datetime import datetime
import re


# ------------------------------------------------------------------------------
# global variables
# ------------------------------------------------------------------------------
git_dir = '.git'
pom_file = 'pom.xml'
path_sep='/\\'
cwd = os.getcwd()
start_time = datetime.now()
log_file = 'git_create_branch_'+ start_time.strftime('%Y-%m-%d_%H-%M-%S') + '.log'
log_to_file = False
rgx_non_alpha = re.compile(r'\W+')
rgx_pom_ver = re.compile(r'<version>(.+)</version>')
rgx_pom_ver_grp=1

# ------------------------------------------------------------------------------
# parse command line arguments
# ------------------------------------------------------------------------------
'''
-f, --logfile: enable logging to file
-g, --debug: enable debug mode
-d, --dir: repositories base directory
-r, --repos: repositories list
-m, --mvn: execute maven build
-M, --mvn-offline: execute maven build in offline mode
-j <issue_id>, --jira <issue_id>: jira issue id
-s <src_branch>, --src-branch <src_branch>: source branch
-b <branch-name>, --branch <branch-name>: branch name
-v <pom_ver>, --version <pom_ver>: pom version
'''
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dir',
                        dest='base_dir', default='.', metavar='<base_dir>',
                        help='repositories base directory')
    parser.add_argument('-r', '--repos',
                        dest='repo_list', nargs='+', metavar='<repo>',
                        help='repositories list')
    parser.add_argument('-m', '--mvn', action='store_true',
                        dest='mvn_build',
                        help='execute maven build')
    parser.add_argument('-M', '--mvn-offline', action='store_true',
                        dest='mvn_build_offline',
                        help='execute maven build in offline mode')
    parser.add_argument('-g', '--debug', action='store_const',
                        dest='log_level', const=logging.DEBUG, default=logging.INFO,
                        help='enable debug mode')
    parser.add_argument('-f', '--logfile', action='store_true',
                        dest='log_to_file',
                        help='enable logging to file')
    parser.add_argument('-j', '--jira',
                        dest='jira_issue', metavar='<issue_id>',
                        help='jira issue id')                        
    parser.add_argument('-s', '--src-branch',
                        dest='src_branch_name', metavar='<src_branch>',
                        help='source branch')
    parser.add_argument('-b', '--branch',
                        dest='branch_name', required=True, metavar='<branch>',
                        help='create branch')
    parser.add_argument('-v', '--version',
                        dest='pom_ver', required=True, metavar='<version>',
                        help='pom version')

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
       logging.error('Directory "{}" does not exist !!!\nExiting'.format(base_dir))
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
# create & push git tag
# ------------------------------------------------------------------------------
def create_tag(tag_name, tag_msg):
    tag_cmd = ['git', 'tag', '-a', tag_name]
    if tag_msg:
        tag_cmd.extend(['-m', tag_msg])
    exec_cmd(tag_cmd)
    exec_cmd(['git', 'push', 'origin', tag_name])


# ------------------------------------------------------------------------------
# checkout git branch
# ------------------------------------------------------------------------------
def checkout_branch(src_branch_name):
    if src_branch_name:
        # prepend with obs/ if repo is ccsecure
        if 'ccsecure' in os.getcwd():
            src_branch_name = 'obs/' + src_branch_name

        exec_cmd(['git', 'checkout', src_branch_name])


# ------------------------------------------------------------------------------
# create & push git branch
# ------------------------------------------------------------------------------
def create_branch(branch_name):
    # prepend with obs/ if repo is ccsecure
    if 'ccsecure' in os.getcwd():
        branch_name = 'obs/' + branch_name

    exec_cmd(['git', 'checkout', '-b', branch_name])
    exec_cmd(['git', 'push', '--set-upstream', 'origin', branch_name])


# ------------------------------------------------------------------------------
# commit & push changes
# ------------------------------------------------------------------------------
def commit(file_paths, commit_msg, new_branch):
    add_cmd = ['git', 'add' ]
    add_cmd.extend(file_paths)
    exec_cmd(add_cmd)
    exec_cmd(['git', 'commit', '-m', commit_msg])
    exec_cmd(['git', 'push'])


# ------------------------------------------------------------------------------
# searches file for a pattern and returns the matched group
# ------------------------------------------------------------------------------
def rgx_search(file_path, rgx, grp=0):
    with open(file_path, "rt", encoding="utf-8") as file:
        file_text = file.read()
    match = rgx.search(file_text)
    return match.group(grp)

# ------------------------------------------------------------------------------
# searches & replaces all occurrences of a pattern in file
# ------------------------------------------------------------------------------
def rgx_rpl_file_txt(file_path, rgx, rpl_str):
    with open(file_path, "rt", encoding="utf-8") as file:
        file_text = file.read()
    with open(file_path, "wt", encoding="utf-8") as file:
        file.write(rgx.sub(rpl_str, file_text))


# ------------------------------------------------------------------------------
# searches & replaces all occurrences of a string in file
# ------------------------------------------------------------------------------
def rpl_file_txt(file_path, srch_str, rpl_str):
    with open(file_path, "rt", encoding="utf-8") as file:
        file_text = file.read()
    with open(file_path, "wt", encoding="utf-8") as file:
        file.write(file_text.replace(srch_str, rpl_str))


# ------------------------------------------------------------------------------
# gets list of paths for all pom files in the search path
# ------------------------------------------------------------------------------
def get_pom_paths(search_path):
    find_pom_cmd_args = [ 'find', search_path, '-name', 'pom.xml' ]
    return subprocess.check_output(find_pom_cmd_args, shell=True, universal_newlines=True).strip().split('\n')

# ------------------------------------------------------------------------------
# updates pom version
# ------------------------------------------------------------------------------
def update_pom_ver(mvn_paths, pom_ver):
    file_paths = []
    for mvn_dir in mvn_paths:
        os.chdir(mvn_dir)
        exec_cmd(['mvn', '-o', 'clean' ])        
        pom_paths = get_pom_paths(mvn_dir)
        logging.debug(pom_paths)
        for f in pom_paths:
            src_pom_ver = rgx_search(f, rgx_pom_ver, rgx_pom_ver_grp)
            logging.debug('file=%s, src_pom_ver=%s, pom_ver=%s', f, src_pom_ver, pom_ver)
            if src_pom_ver:
                rpl_file_txt(f, src_pom_ver, pom_ver)
        file_paths.extend(pom_paths)
    return file_paths

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

    jira_issue = '' if cmd_args.jira_issue is None else cmd_args.jira_issue + ': '

    branch_name = cmd_args.branch_name.lower()
    tag_id = rgx_non_alpha.sub('_', branch_name)
    for dirname in sorted(git_repos):
        mvn_paths = get_mvn_paths(git_repos[dirname])

        log_hdr(dirname)

        os.chdir(git_repos[dirname])

        exec_cmd(['git', 'pull', '--all'])

        checkout_branch(cmd_args.src_branch_name)

        create_tag('b_' + tag_id + '_pre',
           jira_issue + 'branch creation checkpoint' )

        create_branch(branch_name)

        file_paths = update_pom_ver(mvn_paths, cmd_args.pom_ver)    

        commit(file_paths, jira_issue + 'created branch and updated pom version to ' + cmd_args.pom_ver, branch_name)

        create_tag('b_' + tag_id + '_post',
           jira_issue + 'pom version update checkpoint' )
           
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
