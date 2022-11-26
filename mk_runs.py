#! /usr/bin/env python
#
#   script generator for project="2021-S1-UM-3"
#
#

import os
import sys

# in prep of the new lmtoy module
try:
    lmtoy = os.environ['LMTOY']
    sys.path.append(lmtoy + '/lmtoy')
    import runs
except:
    print("No LMTOY with runs.py")
    sys.exit(0)

project="2021-S1-UM-3"

#        obsnums per source (make it negative if not added to the final combination)
on = {}
on['UGCA281'] = [-99716, -99718, -99720,
                 100536, 100538, 100540, 100544, 100546, 100548, 100550, 100554, 100556, 100558,  # 1-jun
                ]
#        common parameters per source on the first dryrun (run1, run2)
pars1 = {}
pars1['UGCA281'] = "pix_list=8,10"

#        common parameters per source on subsequent runs (run1a, run2a)
pars2 = {}
pars2['UGCA281'] = "admit=0 srdp=1"

runs.mk_runs(project, on, pars1, pars2)
