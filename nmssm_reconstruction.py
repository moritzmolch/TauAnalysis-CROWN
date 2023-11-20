from __future__ import annotations  # needed for type annotations in > python 3.7
from typing import List, Union
from .producers import pairquantities as pairquantities
from .producers import hhkinfit as hhkinfit
from .quantities import output as q
from code_generation.friend_trees import FriendTreeConfiguration
from code_generation.modifiers import EraModifier


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

    configuration.add_producers(
        ["mt", "et", "tt"],
        [
            pairquantities.FastMTTQuantities,
            pairquantities.BoostedFastMTTQuantities,
            hhkinfit.YHKinFit_YToBB, 
            hhkinfit.YHKinFit_YToTauTau, 
            hhkinfit.YHKinFit_YToBB_boosted, 
            hhkinfit.YHKinFit_YToTauTau_boosted, 
        ],
    )

    configuration.add_outputs(
        ["mt", "et", "tt"],
        [
            q.m_fastmtt,
            q.pt_fastmtt,
            q.eta_fastmtt,
            q.phi_fastmtt,
            q.boosted_m_fastmtt,
            q.boosted_pt_fastmtt,
            q.boosted_eta_fastmtt,
            q.boosted_phi_fastmtt,
            q.kinfit_convergence_YToBB,
            q.kinfit_mX_YToBB,
            q.kinfit_mY_YToBB,
            q.kinfit_mh_YToBB,
            q.kinfit_chi2_YToBB,
            q.kinfit_prob_YToBB,
            q.kinfit_pull1_YToBB,
            q.kinfit_pull2_YToBB,
            q.kinfit_pullBalance_YToBB,
            q.kinfit_convergence_YToTauTau,
            q.kinfit_mX_YToTauTau,
            q.kinfit_mY_YToTauTau,
            q.kinfit_mh_YToTauTau,
            q.kinfit_chi2_YToTauTau,
            q.kinfit_prob_YToTauTau,
            q.kinfit_pull1_YToTauTau,
            q.kinfit_pull2_YToTauTau,
            q.kinfit_pullBalance_YToTauTau,
            q.kinfit_convergence_YToBB_boosted,
            q.kinfit_mX_YToBB_boosted,
            q.kinfit_mY_YToBB_boosted,
            q.kinfit_mh_YToBB_boosted,
            q.kinfit_chi2_YToBB_boosted,
            q.kinfit_prob_YToBB_boosted,
            q.kinfit_pull1_YToBB_boosted,
            q.kinfit_pull2_YToBB_boosted,
            q.kinfit_pullBalance_YToBB_boosted,
            q.kinfit_convergence_YToTauTau_boosted,
            q.kinfit_mX_YToTauTau_boosted,
            q.kinfit_mY_YToTauTau_boosted,
            q.kinfit_mh_YToTauTau_boosted,
            q.kinfit_chi2_YToTauTau_boosted,
            q.kinfit_prob_YToTauTau_boosted,
            q.kinfit_pull1_YToTauTau_boosted,
            q.kinfit_pull2_YToTauTau_boosted,
            q.kinfit_pullBalance_YToTauTau_boosted,
        ],
    )

    #########################
    # Finalize and validate the configuration
    #########################
    configuration.optimize()
    configuration.validate()
    configuration.report()
    return configuration.expanded_configuration()
