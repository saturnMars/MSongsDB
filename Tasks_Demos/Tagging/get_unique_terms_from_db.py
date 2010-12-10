"""
Thierry Bertin-Mahieux (2010) Columbia University
tb2332@columbia.edu

This code is used to get the list of unique terms as fast
as possible from an SQLite precomputed database (artist_term.db).
It dumps it to a file which can be used later.
Goal is the same as: get_unique_terms.py   just WAY faster
Twist: you need the list of unique terms to build the database
in the first place. Good news: we did it for you!

This is part of the Million Song Dataset project from
LabROSA (Columbia University) and The Echo Nest.


Copyright 2010, Thierry Bertin-Mahieux

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""


import os
import sys
import glob
import time
import datetime
import numpy as np
try:
    import sqlite3
except ImportError:
    print 'you need sqlite3 installed to use this program'
    sys.exit(0)


def die_with_usage():
    """ HELP MENU """
    print 'get_unique_terms.py'
    print '  by T. Bertin-Mahieux (2010) Colubia University'
    print 'GOAL'
    print '  creates a list of unique tags as fast as possible'
    print '  actually, this code just extracts it from a SQLite db'
    print 'USAGE'
    print '  python get_unique_terms.py <artist_term.db> <output.txt>'
    print 'PARAM'
    print '   artist_term.db    - SQLite database of artists/terms'
    print '   output.txt        - result text file, one tag per line'
    print ''
    print 'if you do not have the artist_term.db SQLite, check the slower code:'
    print '                        /Tasks_Demos/NamesAnalysis/get_unique_terms.py'
    print 'for artist list, check: /Tasks_Demos/NamesAnalysis/list_all_artists.py'
    print '             or faster: /Tasks_Demos/SQLite/list_all_artists_from_db.py'
    sys.exit(0)


if __name__ == '__main__':

    # help menu
    if len(sys.argv) < 3:
        die_with_usage()

    # params
    dbfile = os.path.abspath(sys.argv[1])
    output = os.path.abspath(sys.argv[2])

    # sanity checks
    if not os.path.isfile(dbfile):
        print 'ERROR: database not found:',dbfile
        sys.exit(0)
    if os.path.exists(output):
        print 'ERROR:',output,'already exists! delete or provide a new name'
        sys.exit(0)

    # query the database
    q = "SELECT DISTINCT term FROM terms ORDER BY term" # DISTINCT useless
    conn = sqlite3.connect(dbfile)
    c = conn.cursor()
    res = c.execute(q)
    alltags = map(lambda x: x[0],res.fetchall())
    c.close()
    conn.close()
    print 'found',len(alltags),'unique terms.'

    # write to file
    f = open(output,'w')
    for t in alltags:
        f.write(t + '\n')
    f.close()
