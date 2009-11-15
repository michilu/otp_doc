#!/usr/bin/env python

import os
import sys
import shutil

from lxml import etree
from lxml import html
import html2rest
import html2rst

#ROOTDIR = sys.argv[1]
#SOURCEDIR = sys.argv[2]
ROOTDIR = "downloads"
SOURCEDIR = "source"

def mkdir(path):
    _path = path.split(os.sep)
    postion = len(_path)
    while not os.path.exists(path):
        try:
            os.mkdir(os.sep.join(_path[0:postion]))
        except OSError:
            postion = postion - 1
        else:
            postion = postion + 1

def main():
    for root, dirs, files in os.walk(ROOTDIR):
        if not root.endswith("/doc"):
            continue
        for srcdir, dirs, files in os.walk(root):
            if os.sep in srcdir:
                dstdir = os.sep.join([SOURCEDIR] + srcdir.split(os.sep)[1:])
            if not os.path.exists(dstdir):
                #mkdir(dstdir)
                os.makedirs(dstdir)
            for _file in files:
                src, dst = map(lambda x:os.sep.join([x, _file]), (srcdir, dstdir))
                base = src[len(ROOTDIR)+1:]
                if src.endswith(".html"):
                    #if "/java/" not in src:
                        #continue
                    head, tail = os.path.splitext(dst)
                    dst = "".join([head, ".rst"])
                    try:
                        dst_file = open(dst, "w")
                        title = " ".join((s.capitalize() for s in os.path.splitext(base)[0].replace("/","_-_").split("_")))
                        title_line = ["="*len(title)] * 2
                        title_line[1:1] = [title]
                        [dst_file.write("".join((i,"\n"))) for i in title_line]
                        dst_file.write("\n")
                        html2rest.html2rest(
                            html.tostring(html.fromstring(open(src).read())),
                            dst_file)
                    except (UnicodeEncodeError, UnicodeDecodeError, IndexError), e:
                        print
                        print src, e
                    else:
                        sys.stdout.write(".")
                        sys.stdout.flush()
                    finally:
                        dst_file.close()
                else:
                    shutil.copyfile(src, dst)
    return

if __name__ == "__main__":
    main()
