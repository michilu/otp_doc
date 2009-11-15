#!/usr/bin/env python

import httplib
import os
import sys
import tarfile
import urlparse

SOURCE = sys.argv[1]
TARBALL = sys.argv[2]
DOWNLOADDIR = sys.argv[3]

def main():
    os.chdir(DOWNLOADDIR)
    scheme, netloc, path, params, query, fragment = urlparse.urlparse(SOURCE)
    con = httplib.HTTPConnection(netloc)
    con.request("GET", path)
    response = con.getresponse()
    if response.status != 200:
        con.close()
        sys.exit(1)
    output = open(TARBALL, "w")
    output.write(response.read())
    output.close()
    con.close()

    tar = tarfile.open(TARBALL)
    tar.extractall()
    tar.close()

if __name__ == "__main__":
    main()
