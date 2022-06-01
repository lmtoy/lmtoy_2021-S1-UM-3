#! /usr/bin/env python
#
#   script generator for project="2021-S1-UM-3"
#
#

import os
import sys

project="2021-S1-UM-3"

#        obsnums per source (make it negative if not added to the final combination)
on = {}
on['UGCA281'] = [99716, 99718, 99720]
#        common parameters per source on the first dryrun (run1, run2)
common1="admit=0 restart=1 badcb=2/1,2/4"
pars1 = {}
pars1['UGCA281'] = ""

#        common parameters per source on subsequent runs (run1a, run2a)
common2="admit=0 restart=1 srdp=1"
pars2 = {}
pars2['UGCA281'] = ""


# below here no need to change code
# ========================================================================

#        helper function for populating obsnum dependant argument
def getargs(obsnum, flags=True):
    """ search for <obsnum>.args
        and in lmtoy.flags
    """
    args = ""    
    if flags:
        f = 'lmtoy.flags'
        if os.path.exists(f):
            lines = open(f).readlines()
            for line in lines:
                if line[0] == '#': continue
                args = args + line.strip() + " "
        
    f = "%d.args" % obsnum
    if os.path.exists(f):
        lines = open(f).readlines()
        for line in lines:
            if line[0] == '#': continue
            args = args + line.strip() + " "
    return args

#        specific parameters per obsnum will be in files <obsnum>.args
pars3 = {}
for s in on.keys():
    for o1 in on[s]:
        o = abs(o1)
        pars3[o] = getargs(o)


run1  = '%s.run1'  % project
run1a = '%s.run1a' % project
run2  = '%s.run2' % project
run2a = '%s.run2a' % project

fp1 = open(run1,  "w")
fp2 = open(run1a, "w")
fp3 = open(run2,  "w")
fp4 = open(run2a, "w")

#                           record the obsnum min/max
o_min =  999999
o_max = -999999

#                           single obsnum
n1 = 0
for s in on.keys():
    for o1 in on[s]:
        o = abs(o1)
        cmd1 = "SLpipeline.sh obsnum=%d _s=%s %s admit=0 restart=1 " % (o,s,pars1[s])
        cmd2 = "SLpipeline.sh obsnum=%d _s=%s %s admit=0 %s" % (o,s,pars2[s], pars3[o])
        fp1.write("%s\n" % cmd1)
        fp2.write("%s\n" % cmd2)
        n1 = n1 + 1
        if o1 < o_min:  o_min=o1
        if o1 > o_max:  o_max=o1        

#                           combination obsnums
n2 = 0        
for s in on.keys():
    obsnums = ""
    n3 = 0
    for o1 in on[s]:
        o = abs(o1)
        if o1 < 0: continue
        n3 = n3 + 1
        if obsnums == "":
            obsnums = "%d" % o
        else:
            obsnums = obsnums + ",%d" % o
    print('%s[%d/%d] :' % (s,n3,len(on[s])), obsnums)
    cmd3 = "SLpipeline.sh _s=%s admit=0 restart=1 obsnums=%s" % (s, obsnums)
    cmd4 = "SLpipeline.sh _s=%s admit=1 srdp=1  obsnums=%s" % (s, obsnums)
    fp3.write("%s\n" % cmd3)
    fp4.write("%s\n" % cmd4)
    n2 = n2 + 1

print("A proper re-run of %s should be in the following order:" % project)
print(run1)
print(run2)
print(run1a)
print(run2a)
print("Where there are %d single obsnum runs, and %d combination obsnums" % (n1,n2))
print("Range of obsnums: %d - %d" % (o_min, o_max))
