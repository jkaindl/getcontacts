############################################################################
# Copyright 2018 Anthony Ma & Stanford University                          #
#                                                                          #
# Licensed under the Apache License, Version 2.0 (the "License");          #
# you may not use this file except in compliance with the License.         #
# You may obtain a copy of the License at                                  #
#                                                                          #
#     http://www.apache.org/licenses/LICENSE-2.0                           #
#                                                                          #
# Unless required by applicable law or agreed to in writing, software      #
# distributed under the License is distributed on an "AS IS" BASIS,        #
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. #
# See the License for the specific language governing permissions and      #
# limitations under the License.                                           #
############################################################################

##############################################################################
# Imports
##############################################################################

from .contact_utils import *

__all__ = ['prep_salt_bridge_computation', 'compute_salt_bridges']

##############################################################################
# Functions
##############################################################################


def prep_salt_bridge_computation(traj_frag_molid, frame_idx, sele_id):
    """
    Compute all possible anion and cation atoms from first frame of simulation

    Returns
    -------
    anion_list: list of strings
        List of atom labels for atoms in ASP or GLU that
        can form salt bridges
    cation_list: list of strings
        List of atom labels for atoms in LYS, ARG, HIS that
        can form salt bridges
    """
    anion_list = get_anion_atoms(traj_frag_molid, frame_idx, sele_id)
    cation_list = get_cation_atoms(traj_frag_molid, frame_idx, sele_id)
    return anion_list, cation_list


def compute_salt_bridges(traj_frag_molid, frame_idx, sele_id, SALT_BRIDGE_CUTOFF_DISTANCE=4.0):
    """
    Compute salt bridges in a frame of simulation

    Parameters
    ----------
    traj_frag_molid: int
        Identifier to simulation fragment in VMD
    frame_idx: int
        Frame number to query
    sele_id: string, default = None
        Compute contacts on subset of atom selection based on VMD query
    SALT_BRIDGE_CUTOFF_DISTANCE: float, default = 4.0 angstroms
        cutoff for distance between anion and cation atoms

    Returns
    -------
    salt_bridges: list of tuples, [(frame_index, itype, atom1_label, atom2_label), ...]
        itype = "sb"
    """
    anion_list, cation_list = prep_salt_bridge_computation(traj_frag_molid, frame_idx, sele_id)
    salt_bridges = []
    for anion_atom in anion_list:
        for cation_atom in cation_list:
            dist = compute_distance(traj_frag_molid, frame_idx, anion_atom, cation_atom)
            if dist < SALT_BRIDGE_CUTOFF_DISTANCE:
                salt_bridges.append([frame_idx, "sb", anion_atom, cation_atom])

    return salt_bridges
