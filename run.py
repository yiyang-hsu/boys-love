from os import makedirs
import glob

def metainfo(lines):
    title = 'Untitled'
    author = 'Anonymous'
    info = dict()
    flag = False
    for line in lines:
        if ':' in line:
            key = line.split(':')[0].strip()
            value = line.split(':')[-1].strip()
            info[key] = value
    return info

def write_pages(info, lines):
    path = 'content/collections/{}'.format(info['title'])
    makedirs(path, exist_ok=True)
    head = make_head(info, added='\ndownload: "txt/"')
    length = len(lines) // 500 + 1
    if length > 5:
        index_file = open('{}/_index.md'.format(path), 'w')
        index_file.writelines(head)
        for i in range(length):
            head = make_head(info, i + 1)
            outfile = open('{}/{}.md'.format(path, i + 1), 'w')
            outfile.writelines(head)
            outfile.write('\n')
            outfile.writelines(lines[i*500:i*500+3])
            outfile.write('<!--more-->\n')
            outfile.writelines(lines[i*500+3:i*500+500])
            outfile.close()
        index_file.close()
    else:
        index_file = open('{}/index.md'.format(path), 'w')
        index_file.writelines(head)
        index_file.write('\n')
        index_file.writelines(lines[0:3])
        index_file.write('<!--more-->\n')
        index_file.writelines(lines[3:])
        index_file.close()


def make_head(info, num=None, added=''):
    title = info['title'] + " ({})\nweight: {}".format(num, num) if num else info['title']
    return """---
title: {}
author: {}{}
---
""".format(title, info['author'], added)

def split_lines(lines):
    info_lines = []
    flag = False
    for line in lines:
        if '---' in line:
            flag = ~flag
            continue
        if not flag:
            break
        info_lines.append(line)
    return info_lines, lines[len(info_lines) + 2:]

if __name__ == "__main__":
    for txt in glob.glob("static/txt/zh/*.txt"):
        with open(txt) as file:
            lines = file.readlines()
            info_lines, page_lines = split_lines(lines)
            info = metainfo(info_lines)
            write_pages(info, page_lines)