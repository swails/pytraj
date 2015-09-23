#!/usr/bin/env python
from __future__ import print_function
import unittest
import pytraj as pt
from pytraj.utils import eq, aa_eq


class Test(unittest.TestCase):
    def test_0(self):
        traj = pt.iterload("./data/tz2.nc", "./data/tz2.parm7")
        txt = '''
        parm data/tz2.parm7
        trajin data/tz2.nc
        drmsd drms_nofit out drmsd.dat
        rms rms_nofit out drmsd.dat nofit
        rms rms_fit out drmsd.dat
        drmsd drms_fit out drmsd.dat
        '''

        cpp_data = pt.datafiles.load_cpptraj_output(txt)
        print(pt.distance_rmsd(traj))

        ## distance_rmsd
        data_drmsd = pt.distance_rmsd(traj)
        aa_eq(data_drmsd, cpp_data[0])

        # rms_nofit
        aa_eq(cpp_data[1], pt.rmsd(traj, nofit=True))

        # rms_fit
        aa_eq(cpp_data[2], pt.rmsd(traj, nofit=False))

        # drmsd with rmsfit
        aa_eq(cpp_data[3], pt.distance_rmsd(traj(rmsfit=0), ref=traj[0]))


if __name__ == "__main__":
    unittest.main()
