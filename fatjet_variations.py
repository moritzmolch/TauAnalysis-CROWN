from __future__ import annotations  # needed for type annotations in > python 3.7

from typing import List
from code_generation.configuration import Configuration
from code_generation.systematics import SystematicShift
from .producers import fatjets as fatjets
from .producers import scalefactors as scalefactors


def add_fatjetVariations(
    configuration: Configuration, available_sample_types: List[str], era: str
):
    #########################
    # Jet energy resolution
    #########################
    configuration.add_shift(
        SystematicShift(
            name="AK8jerUncUp",
            shift_config={
                "global": {"fatjet_jer_shift": '"up"'},
            },
            producers={
                "global": {
                    fatjets.FatJetEnergyCorrection,
                },
            },
        ),
        samples=[
            sample
            for sample in available_sample_types
            if sample not in ["data", "embedding", "embedding_mc"]
        ],
    )
    configuration.add_shift(
        SystematicShift(
            name="AK8jerUncDown",
            shift_config={
                "global": {"fatjet_jer_shift": '"down"'},
            },
            producers={
                "global": {
                    fatjets.FatJetEnergyCorrection,
                },
            },
        ),
        samples=[
            sample
            for sample in available_sample_types
            if sample not in ["data", "embedding", "embedding_mc"]
        ],
    )
    #########################
    # Jet energy scale - Total
    #########################
    JEC_sources = '{"Total"}'
    configuration.add_shift(
        SystematicShift(
            name="AK8jesUncTotalUp",
            shift_config={
                "global": {
                    "fatjet_jes_shift": 1,
                    "fatjet_jes_sources": JEC_sources,
                },
            },
            producers={
                "global": {
                    fatjets.FatJetEnergyCorrection,
                },
            },
        ),
        samples=[
            sample
            for sample in available_sample_types
            if sample not in ["data", "embedding", "embedding_mc"]
        ],
    )
    configuration.add_shift(
        SystematicShift(
            name="AK8jesUncTotalDown",
            shift_config={
                "global": {
                    "fatjet_jes_shift": -1,
                    "fatjet_jes_sources": JEC_sources,
                },
            },
            producers={
                "global": {
                    fatjets.FatJetEnergyCorrection,
                },
            },
        ),
        samples=[
            sample
            for sample in available_sample_types
            if sample not in ["data", "embedding", "embedding_mc"]
        ],
    )

    return configuration
