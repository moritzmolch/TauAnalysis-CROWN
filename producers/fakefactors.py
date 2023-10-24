from ..quantities import output as q
from ..quantities import nanoAOD as nanoAOD
from code_generation.producer import Producer, ProducerGroup

RawFakeFactors_nmssm_lt = Producer(
    name="RawFakeFactors_nmssm_lt",
    call='fakefactors::raw_fakefactor_nmssm_lt({df}, {output}, {input}, "{ff_variation}", "{ff_file}")',
    input=[
        q.pt_2,
        q.njets,
        q.mt_1,
        q.nbtag,
    ],
    output=[q.raw_fake_factor],
    scopes=["mt", "et"],
)
RawFakeFactors_nmssm_boosted_lt = Producer(
    name="RawFakeFactors_nmssm_boosted_lt",
    call='fakefactors::raw_fakefactor_nmssm_boosted_lt({df}, {output}, {input}, "{ff_variation_boosted}", "{ff_file_boosted}")',
    input=[
        q.boosted_pt_2,
        q.njets_boosted,
        q.boosted_mt_1,
        q.nbtag_boosted,
    ],
    output=[q.raw_fake_factor_boosted],
    scopes=["mt", "et"],
)
RawFakeFactors_nmssm_tt_1 = Producer(
    name="RawFakeFactors_nmssm_tt_1",
    call='fakefactors::raw_fakefactor_nmssm_tt({df}, {output}, 0, {input}, "{ff_variation}", "{ff_file}")',
    input=[
        q.pt_1,
        q.pt_2,
        q.njets,
        # q.nbtag,
    ],
    output=[q.raw_fake_factor_1],
    scopes=["tt"],
)
RawFakeFactors_nmssm_tt_2 = Producer(
    name="RawFakeFactors_nmssm_tt_2",
    call='fakefactors::raw_fakefactor_nmssm_tt({df}, {output}, 1, {input}, "{ff_variation}", "{ff_file}")',
    input=[
        q.pt_1,
        q.pt_2,
        q.njets,
        # q.nbtag,
    ],
    output=[q.raw_fake_factor_2],
    scopes=["tt"],
)

FakeFactors_nmssm_lt = Producer(
    name="FakeFactors_nmssm_lt",
    call='fakefactors::fakefactor_nmssm_lt({df}, {output}, {input}, "{ff_variation}", "{ff_file}", "{ff_corr_file}")',
    input=[
        q.pt_2,
        q.njets,
        q.mt_1,
        q.nbtag,
        q.pt_1,
        q.iso_1,
        q.m_vis,
    ],
    output=[q.fake_factor],
    scopes=["mt", "et"],
)
FakeFactors_nmssm_boosted_lt = Producer(
    name="FakeFactors_nmssm_boosted_lt",
    call='fakefactors::fakefactor_nmssm_boosted_lt({df}, {output}, {input}, "{ff_variation_boosted}", "{ff_file_boosted}", "{ff_corr_file_boosted}")',
    input=[
        q.boosted_pt_2,
        q.njets_boosted,
        q.boosted_mt_1,
        q.nbtag_boosted,
        q.boosted_pt_1,
        q.boosted_m_vis,
    ],
    output=[q.fake_factor_boosted],
    scopes=["mt", "et"],
)
FakeFactors_nmssm_tt_1 = Producer(
    name="FakeFactors_nmssm_tt_1",
    call='fakefactors::fakefactor_nmssm_tt({df}, {output}, 0, {input}, "{ff_variation}", "{ff_file}", "{ff_corr_file}")',
    input=[
        q.pt_1,
        q.pt_2,
        q.njets,
        # q.nbtag,
        q.m_vis,
    ],
    output=[q.fake_factor_1],
    scopes=["tt"],
)
FakeFactors_nmssm_tt_2 = Producer(
    name="FakeFactors_nmssm_tt_2",
    call='fakefactors::fakefactor_nmssm_tt({df}, {output}, 1, {input}, "{ff_variation}", "{ff_file}", "{ff_corr_file}")',
    input=[
        q.pt_1,
        q.pt_2,
        q.njets,
        # q.nbtag,
        q.m_vis,
    ],
    output=[q.fake_factor_2],
    scopes=["tt"],
)