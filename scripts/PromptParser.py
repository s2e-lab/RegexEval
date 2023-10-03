#!/usr/bin/env python3

import requests
import sys
import os
import json

def extract_code(storage):

    for item in range(len(storage['Sources'])):
        for thing in range(len(storage['Sources'][item]['ChatgptSharing'])):
            # obtain chatgpt code
            urlcode = storage['Sources'][item]['ChatgptSharing'][thing]['URL']
            unique_chatgpt_code = urlcode.split('/')[4]
            # check if conversation exists
            if 'Conversations' in storage['Sources'][item]['ChatgptSharing'][thing]:
                for new in range(len(storage['Sources'][item]['ChatgptSharing'][thing]['Conversations'])):
                    curr = storage['Sources'][item]['ChatgptSharing'][thing]['Conversations'][new]['ListOfCode']
                    # check if list of code is given
                    if curr:
                        # filter by coding language
                        for arg in range(len(curr)):
                            # obtain serial
                            block = curr[arg]['ReplaceString']
                            serial = block.split('_')[2][0]
                            # find language for extension
                            language = curr[arg]['Type']
                            if language == 'python' or language == 'py':
                                extension = '.py'
                                path = 'Python'
                            elif language == 'java':
                                extension = '.java'
                                path = 'Java'
                            else:
                                continue
                            # write file
                            filename = unique_chatgpt_code + '_' + serial + extension
                            completeName = os.path.join(path, filename) 
                            myfile = open(completeName, 'w')
                            myfile.write(curr[arg]['Content'])
                            myfile.close()

def main():
    #url = sys.argv[1]
    ''' data is given in both URLS and ZIPS because each screenshot contained a .zip.json
        it was easier to download 8 zip files and use the rest as URLS '''

    # given urls
    URLS = ['https://raw.githubusercontent.com/NAIST-SE/DevGPT/main/snapshot_20230727/20230727_195816_hn_sharings.json',
    'https://raw.githubusercontent.com/NAIST-SE/DevGPT/main/snapshot_20230727/20230727_195927_pr_sharings.json',
    'https://raw.githubusercontent.com/NAIST-SE/DevGPT/main/snapshot_20230727/20230727_195941_issue_sharings.json',
    'https://raw.githubusercontent.com/NAIST-SE/DevGPT/main/snapshot_20230727/20230727_195954_discussion_sharings.json',
    'https://raw.githubusercontent.com/NAIST-SE/DevGPT/main/snapshot_20230727/20230727_200003_commit_sharings.json',
    'https://raw.githubusercontent.com/NAIST-SE/DevGPT/main/snapshot_20230803/20230803_093947_pr_sharings.json',
    'https://raw.githubusercontent.com/NAIST-SE/DevGPT/main/snapshot_20230803/20230803_094705_issue_sharings.json',
    'https://raw.githubusercontent.com/NAIST-SE/DevGPT/main/snapshot_20230803/20230803_094811_discussion_sharings.json',
    'https://raw.githubusercontent.com/NAIST-SE/DevGPT/main/snapshot_20230803/20230803_095317_commit_sharings.json',
    'https://raw.githubusercontent.com/NAIST-SE/DevGPT/main/snapshot_20230803/20230803_105332_hn_sharings.json',
    'https://raw.githubusercontent.com/NAIST-SE/DevGPT/main/snapshot_20230810/20230810_123110_pr_sharings.json',
    'https://raw.githubusercontent.com/NAIST-SE/DevGPT/main/snapshot_20230810/20230810_123938_issue_sharings.json',
    'https://raw.githubusercontent.com/NAIST-SE/DevGPT/main/snapshot_20230810/20230810_124048_discussion_sharings.json',
    'https://raw.githubusercontent.com/NAIST-SE/DevGPT/main/snapshot_20230810/20230810_124807_commit_sharings.json',
    'https://raw.githubusercontent.com/NAIST-SE/DevGPT/main/snapshot_20230810/20230810_134011_hn_sharings.json',
    'https://raw.githubusercontent.com/NAIST-SE/DevGPT/main/snapshot_20230817/20230817_125147_pr_sharings.json',
    'https://raw.githubusercontent.com/NAIST-SE/DevGPT/main/snapshot_20230817/20230817_130502_issue_sharings.json',
    'https://raw.githubusercontent.com/NAIST-SE/DevGPT/main/snapshot_20230817/20230817_130721_discussion_sharings.json',
    'https://raw.githubusercontent.com/NAIST-SE/DevGPT/main/snapshot_20230817/20230817_131244_commit_sharings.json',
    'https://raw.githubusercontent.com/NAIST-SE/DevGPT/main/snapshot_20230817/20230817_170022_hn_sharings.json',
    'https://raw.githubusercontent.com/NAIST-SE/DevGPT/main/snapshot_20230824/20230824_100450_pr_sharings.json',
    'https://raw.githubusercontent.com/NAIST-SE/DevGPT/main/snapshot_20230824/20230824_101836_issue_sharings.json',
    'https://raw.githubusercontent.com/NAIST-SE/DevGPT/main/snapshot_20230824/20230824_102000_discussion_sharings.json',
    'https://raw.githubusercontent.com/NAIST-SE/DevGPT/main/snapshot_20230824/20230824_102435_commit_sharings.json',
    'https://raw.githubusercontent.com/NAIST-SE/DevGPT/main/snapshot_20230824/20230824_112153_hn_sharings.json',
    'https://raw.githubusercontent.com/NAIST-SE/DevGPT/main/snapshot_20230831/20230831_060603_pr_sharings.json',
    'https://raw.githubusercontent.com/NAIST-SE/DevGPT/main/snapshot_20230831/20230831_061759_issue_sharings.json',
    'https://raw.githubusercontent.com/NAIST-SE/DevGPT/main/snapshot_20230831/20230831_061926_discussion_sharings.json',
    'https://raw.githubusercontent.com/NAIST-SE/DevGPT/main/snapshot_20230831/20230831_063412_commit_sharings.json',
    'https://raw.githubusercontent.com/NAIST-SE/DevGPT/main/snapshot_20230831/20230831_073827_hn_sharings.json',
    'https://raw.githubusercontent.com/NAIST-SE/DevGPT/main/snapshot_20230907/20230907_091631_pr_sharings.json',
    'https://raw.githubusercontent.com/NAIST-SE/DevGPT/main/snapshot_20230907/20230907_092956_issue_sharings.json',
    'https://raw.githubusercontent.com/NAIST-SE/DevGPT/main/snapshot_20230907/20230907_093129_discussion_sharings.json',
    'https://raw.githubusercontent.com/NAIST-SE/DevGPT/main/snapshot_20230907/20230907_110036_commit_sharings.json',
    'https://raw.githubusercontent.com/NAIST-SE/DevGPT/main/snapshot_20230907/20230907_123434_hn_sharings.json',
    'https://raw.githubusercontent.com/NAIST-SE/DevGPT/main/snapshot_20230914/20230914_074826_pr_sharings.json',
    'https://raw.githubusercontent.com/NAIST-SE/DevGPT/main/snapshot_20230914/20230914_080417_issue_sharings.json',
    'https://raw.githubusercontent.com/NAIST-SE/DevGPT/main/snapshot_20230914/20230914_080601_discussion_sharings.json',
    'https://raw.githubusercontent.com/NAIST-SE/DevGPT/main/snapshot_20230914/20230914_083202_commit_sharings.json',
    'https://raw.githubusercontent.com/NAIST-SE/DevGPT/main/snapshot_20230914/20230914_105439_hn_sharings.json']

    # given json zips
    ZIPS = ['20230727_200102_file_sharings.json','20230803_103605_file_sharings.json','20230810_133121_file_sharings.json',
    '20230817_151344_file_sharings.json','20230824_111114_file_sharings.json','20230831_072722_file_sharings.json',
    '20230907_121304_file_sharings.json','20230914_104122_file_sharings.json']

    for url in URLS:
        response = requests.get(url)
        storage = response.json()
        extract_code(storage)

    for fp in ZIPS:
        f = open(fp)
        storage = json.load(f)
        extract_code(storage)

# Main Execution

if __name__ == '__main__':
    main()

# vim: set sts=4 sw=4 ts=8 expandtab ft=python: