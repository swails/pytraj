from __future__ import print_function
import unittest
from pytraj.base import *
from pytraj import adict
from pytraj import io as mdio
from pytraj.utils import eq, aa_eq
from pytraj.decorators import no_test, test_if_having, test_if_path_exists
from pytraj.testing import cpptraj_test_dir
import pytraj.common_actions as pyca

class Test(unittest.TestCase):
    def test_0(self):
        traj = mdio.load("./data/md1_prod.Tc5b.x", "./data/Tc5b.top")
        fa = traj[:]
        print (fa.xyz[0, :10])
        xyz = fa.xyz / 10.
        fa.update_xyz(xyz)
        aa_eq(xyz, fa.xyz)
        print (fa.xyz[0, :10], xyz[0, :10])

if __name__ == "__main__":
    unittest.main()