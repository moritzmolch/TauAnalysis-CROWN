from __future__ import annotations  # needed for type annotations in > python 3.7

from typing import List, Union
import os
from .producers import event as event
from .producers import genparticles as genparticles
from .producers import jets as jets
from .producers import met as met
from .producers import muons as muons
from .producers import pairquantities as pairquantities
from .producers import pairselection as pairselection
from .producers import scalefactors as scalefactors
from .producers import taus as taus
from .producers import triggers as triggers
from .producers import fakefactors as fakefactors
from .quantities import nanoAOD as nanoAOD
from .quantities import output as q

# from code_generation.configuration import Configuration
from code_generation.friend_trees import FriendTreeConfiguration
from code_generation.modifiers import EraModifier, SampleModifier


def build_config(
    era: str,
    sample: str,
    scopes: List[str],
    shifts: List[str],
    available_sample_types: List[str],
    available_eras: List[str],
    available_scopes: List[str],
    quantities_map: Union[str, None] = None,
):
    if quantities_map is None:
        quantities_map = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "dyjets_shift_quantities_map.json",
        )
    configuration = FriendTreeConfiguration(
        era,
        sample,
        scopes,
        shifts,
        available_sample_types,
        available_eras,
        available_scopes,
        quantities_map,
    )

    configuration.add_config_parameters(
        ["mt", "et"],
        {
            "muon_sf_file": "data/embedding/muon_2018UL.json.gz",
            "muon_id_sf": "ID_pt_eta_bins",
            "muon_iso_sf": "Iso_pt_eta_bins",
        },
    )

    # fake factor configurations
    configuration.add_config_parameters(
        ["et"],
        {
            "ff_variation": "nominal",
            "ff_file": EraModifier(
                {
                    "2016": "",
                    "2017": "",
                    "2018": "data/fake_factors/2018/fake_factors_et.json.gz",
                }
            ),
            "ff_corr_file": EraModifier(
                {
                    "2016": "",
                    "2017": "",
                    "2018": "data/fake_factors/2018/FF_corrections_et.json.gz",
                }
            ),
        },
    )
    configuration.add_config_parameters(
        ["mt"],
        {
            "ff_variation": "nominal",
            "ff_file": EraModifier(
                {
                    "2016": "",
                    "2017": "",
                    "2018": "data/fake_factors/2018/fake_factors_mt.json.gz",
                }
            ),
            "ff_corr_file": EraModifier(
                {
                    "2016": "",
                    "2017": "",
                    "2018": "data/fake_factors/2018/FF_corrections_mt.json.gz",
                }
            ),
        },
    )

    configuration.add_producers(
        ["mt", "et"],
        [
            scalefactors.MuonIDSF_friends_1,
            scalefactors.MuonIsoSF_friends_1,
            fakefactors.RawFakeFactors_nmssm_lt,
            fakefactors.FakeFactors_nmssm_lt,
        ],
    )

    configuration.add_outputs(
        ["mt", "et"],
        [
            q.id_wgt_mu_friend_1,
            q.iso_wgt_mu_friend_1,
            q.raw_fake_factor,
            q.fake_factor,
        ],
    )

    #########################
    # Finalize and validate the configuration
    #########################
    configuration.optimize()
    configuration.validate()
    configuration.report()
    return configuration.expanded_configuration()
