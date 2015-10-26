from __future__ import print_function
import unittest
from pytraj.base import *
from pytraj import adict
from pytraj import io as mdio
from pytraj.utils.check_and_assert import assert_almost_equal
from pytraj.testing import cpptraj_test_dir
import pytraj.common_actions as pyca
from pytraj.trajectory import Trajectory
from pytraj.compat import izip


class Test(unittest.TestCase):
    def test_0(self):
        # test append
        traj = Trajectory()
        t = mdio.iterload("./data/md1_prod.Tc5b.x", "./data/Tc5b.top")
        traj.top = t.top

        # append single Frame
        traj.append(t[0])
        assert traj.n_frames == 1

        # append xyz
        traj.append(t.xyz[:])
        assert traj.n_frames == t.n_frames + 1

        # append TrajectoryIterator
        traj.append(t)
        assert traj.n_frames == t.n_frames * 2 + 1

        # append frame_iter
        traj.append(t.iterframe())
        assert traj.n_frames == t.n_frames * 3 + 1

        # append iterframe_master
        from pytraj._shared_methods import iterframe_master
        traj.append(iterframe_master(t))
        assert traj.n_frames == t.n_frames * 4 + 1

        # append itself
        NFrames = traj.n_frames
        traj.append(traj)
        assert traj.n_frames == NFrames * 2

        # append itself frame_iter
        traj.append(traj.iterframe(stop=2))
        assert traj.n_frames == NFrames * 2 + 2

        # append iterframe_master for itself
        NFrames = traj.n_frames
        traj.append(iterframe_master(traj))
        assert traj.n_frames == NFrames * 2

        # append iterframe_master for itself + other
        n0 = traj.n_frames
        n1 = t.n_frames
        traj.append(iterframe_master([traj, t]))
        assert traj.n_frames == 2 * n0 + n1


if __name__ == "__main__":
    unittest.main()
