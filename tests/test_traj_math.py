from __future__ import print_function
import unittest
from pytraj import io as mdio
from pytraj.utils import eq, aa_eq
from pytraj.decorators import no_test, test_if_having, test_if_path_exists
from pytraj.utils import Timer

class Test(unittest.TestCase):
    def test_0(self):
        import numpy as np
        #traj = mdio.load("./data/nogit/tip3p/md.trj", "./data/nogit/tip3p/tc5bwat.top")[:5]
        trajiter = mdio.load("./data/md1_prod.Tc5b.x", "./data/Tc5b.top")
        traj_saved = trajiter[:]
        traj_saved.join([trajiter[:] for _ in range(2000)], copy=False)

        traj = traj_saved.copy()
        print (traj)
        xyz = traj.xyz[:]
        xyz0 = xyz[0].copy()

        # iadd
        traj = traj_saved.copy()
        xyz = traj.xyz[:]
        traj += 1.0
        xyz += 1.0
        aa_eq(traj.xyz, xyz)
        traj += xyz0
        xyz += xyz0
        aa_eq(traj.xyz, xyz)
        
        trajcp = traj.copy()
        xyz_s = traj.xyz.copy()
        trajcp += 2.
        traj += trajcp
        aa_eq(traj.xyz, trajcp.xyz + xyz_s)

        # isub
        traj = traj_saved.copy()
        xyz = traj.xyz[:]
        traj -= 1.0
        xyz -= 1.0
        aa_eq(traj.xyz, xyz)
        fa = traj.copy()
        traj -= fa
        aa_eq(traj.xyz, fa.xyz - fa.xyz)

        # idiv
        traj = traj_saved.copy()
        xyz = traj.xyz[:]
        traj /= 2.0
        xyz /= 2.0
        aa_eq(traj.xyz, xyz)

        xyz_s = traj.xyz.copy()
        traj2 =  traj.copy()
        traj2 /= 0.5
        xyz_2 = traj2.xyz.copy()
        traj /= traj2
        aa_eq(traj.xyz, xyz_s / xyz_2)

        # imul
        traj = traj_saved.copy()
        xyz = traj.xyz[:]
        traj *= 2.0
        xyz *= 2.0
        aa_eq(traj.xyz, xyz)

        fa = traj.copy()
        traj *= fa
        aa_eq(traj.xyz, fa.xyz[:]**2)

        @Timer()
        def time_traj(traj):
            traj += 1.
            traj *= 1.
            traj /= 1.
            traj -= 1.

        @Timer()
        def time_np(xyz):
            xyz += 1.
            xyz *= 1.
            xyz /= 1.
            xyz -= 1.

        print ("time_traj")
        time_traj(traj)
        print ("time_np")
        time_np(xyz)

if __name__ == "__main__":
    unittest.main()