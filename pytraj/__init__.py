"""
pytraj
"""
from __future__ import absolute_import
from sys import platform as _platform
import os

from .tools import find_lib as _find_lib

# check `libcpptraj` and raise ImportError
# only check for Linux since I don't know much about
# OS X and Windows
try:
    # try to check `libcpptraj` that not in LD_LIBRARY_PATH search
    # in _find_lib
    from .core import Atom
except ImportError:
    if 'linux' in _platform:
        if not _find_lib("cpptraj"):
            raise ImportError("can not find libcpptraj. Make sure to install it "
                              "or export LD_LIBRARY_PATH correctly")

try:
    from .core import Atom, Residue, Molecule
except ImportError:
    import os
    source_folders = ['./scripts', './devtools', './docs']
    is_source_folder = True
    for f in source_folders:
        is_source_folder = False if not os.path.exists(f) else True
    if is_source_folder:
        raise ImportError("you are import pytraj in source folder. "
                          "Should go to another location and try again")
try:
    import numpy as np
    np.set_printoptions(threshold=10)
except ImportError:
    np = None

from .__version__ import __version__
version = __version__
from . import options

# import partial from functools
from functools import partial

from .core import Atom, Residue, Molecule
from .core.CpptrajState import CpptrajState
from .import array
from .Topology import Topology
from .ArgList import ArgList
from .AtomMask import AtomMask
from .math import Vec3
from .Frame import Frame
from .Trajectory import Trajectory
from .TrajectoryIterator import TrajectoryIterator
from .trajs.Trajout import Trajout
from .datasets.cast_dataset import cast_dataset
from .parms.ParmFile import ParmFile
from . import io
from .io import (load, iterload, load_remd, iterload_remd,
                 _load_from_filelist, _iterload_from_filelist,
                 _load_from_frame_iter,
                 load_pdb_rcsb, load_pdb,
                 load_pseudo_parm, load_cpptraj_file,
                 load_datafile, load_hdf5,
                 load_sample_data,
                 load_ParmEd, load_full_ParmEd,
                 load_mdtraj,
                 load_MDAnalysis, load_MDAnalysisIterator,
                 load_topology, read_parm, write_parm,
                 get_coordinates,
                 save, write_traj,
                 read_pickle, read_json,
                 to_pickle, to_json,
                 )

load_from_frame_iter = _load_from_frame_iter

# dataset stuff
from .datafiles.load_sample_data import load_sample_data
from .datasetlist import DatasetList

# tool
from . import tools

# actions and analyses
from .actions import CpptrajActions as allactions
from .analyses import CpptrajAnalyses as allanalyses
from ._common_actions import calculate
from . import common_actions
from . dssp_analysis import calc_dssp
from . common_actions import (rmsd, search_hbonds,
                              calc_rmsd_with_rotation_matrices,
                              calc_multidihedral,
                              autoimage, nastruct,
                              calc_angle, calc_dihedral, calc_distance,
                              calc_center_of_mass, calc_center_of_geometry,
                              calc_dssp, calc_jcoupling, calc_molsurf,
                              calc_radgyr, calc_rdf, calc_vector,
                              calc_pairwise_rmsd,
                              calc_atomicfluct,
                              calc_bfactors,
                              energy_decomposition,
                              native_contacts,
                              auto_correlation_function,
                              cross_correlation_function,
                              timecorr,
                              center,
                              translate,
                              rotate,
                              rotate_dihedral,
                              scale,
                              )

# create alias
distance = calc_distance
angle = calc_angle
dihedral = calc_dihedral
nucleic_acid_analysis = nastruct
calc_RMSF = calc_atomicfluct
rmsd_with_rotation_matrices = calc_rmsd_with_rotation_matrices
multidihedral = calc_multidihedral
xcorr = cross_correlation_function
acorr = auto_correlation_function
dssp = calc_dssp
bfactors = calc_bfactors
radgyr = calc_radgyr
molsurf = calc_molsurf
center_of_mass = calc_center_of_mass
center_of_geometry = calc_center_of_geometry

from . matrix_analysis import distance_matrix
from . dihedral_analysis import (
    calc_phi, calc_psi, calc_omega, calc_chin, calc_chip)

from .action_dict import ActionDict
from .analysis_dict import AnalysisDict
adict = ActionDict()
analdict = AnalysisDict()
from . import matrix_analysis
from . import dihedral_analysis
from . import vector_analysis

# others
from .misc import info
from .run_tests import run_tests

from ._shared_methods import _frame_iter_master as frame_iter_master

# turn off verbose in cpptraj
# TODO: need to move set_world_silent and set_error_silent to the same file
from ._set_silent import set_error_silent, set_world_silent

def to_numpy_Trajectory(traj, top, unitcells=None):
    from . import api
    import numpy as np
    from ._xyz import XYZ

    t = api.Trajectory(top=top)
    if isinstance(traj, np.ndarray) or isinstance(traj, XYZ):
        t.xyz = np.asarray(traj)
    elif hasattr(traj, 'xyz'):
        t.xyz = traj.xyz
        if hasattr(traj, 'unitcells'):
            t.unitcells = traj.unitcells
    else:
        t.xyz = get_coordinates(traj)
    if unitcells is not None:
        t.unitcells = unitcells
    return t

def set_cpptraj_verbose(cm=True):
    if cm:
        set_world_silent(False)
    else:
        set_world_silent(True)

set_world_silent(True)

def show():
    # just delay importing
    """show plot
    """
    from matplotlib import pyplot
    pyplot.show()

def savefig(fname, *args, **kwd):
    from matplotlib import pyplot
    pyplot.savefig(fname, *args, **kwd)

def show_versions():
    """
    """
    from .__cpptraj_version__ import info as compiled_info
    from .__cpptraj_version__ import __cpptraj_version__
    from .__cpptraj_version__ import __cpptraj_internal_version__
    print("pytraj version = ", version)
    print("cpptraj version = ", __cpptraj_version__)
    print("cpptraj internal version = ", __cpptraj_internal_version__)
    print("cpptraj compiled flag = ", compiled_info())
