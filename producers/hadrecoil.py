from ..quantities import output as q
from ..quantities import nanoAOD as nanoAOD
from code_generation.producer import Producer, ProducerGroup


ScalarHadRecoil = Producer(
    name="ScalarHadRecoil",
    call="hadrecoil::scalar_ht({df}, {output}, {input})",
    input=[
        q.Jet_pt_corrected,
        q.good_jet_collection,
    ],
    output=[q.ht],
    scopes=["et", "mt", "tt", "em", "ee", "mm"],
)
ScalarHadRecoil_boosted = Producer(
    name="ScalarHadRecoil_boosted",
    call="hadrecoil::scalar_ht({df}, {output}, {input})",
    input=[
        q.Jet_pt_corrected,
        q.good_jet_collection_boosted,
    ],
    output=[q.ht_boosted],
    scopes=["et", "mt", "tt", "em", "ee", "mm"],
)
VectorialHadRecoilP4 = Producer(
    name="VectorialHadRecoilP4",
    call="hadrecoil::vectorial_mht({df}, {input}, {output})",
    input=[
        q.Jet_pt_corrected,
        nanoAOD.Jet_eta,
        q.good_jet_collection,
    ],
    output=[q.mht_p4],
    scopes=["et", "mt", "tt", "em", "ee", "mm"],
)
VectorialHadRecoilP4_boosted = Producer(
    name="VectorialHadRecoilP4_boosted",
    call="hadrecoil::vectorial_mht({df}, {input}, {output})",
    input=[
        q.Jet_pt_corrected,
        nanoAOD.Jet_eta,
        q.good_jet_collection_boosted,
    ],
    output=[q.mht_p4_boosted],
    scopes=["et", "mt", "tt", "em", "ee", "mm"],
)
VectorialHadRecoilPt = Producer(
    name="VectorialHadRecoilPt",
    call="quantities::pt({df}, {output}, {input})",
    input=[
        q.mht_p4,

    ],
    output=[q.mht_pt],
    scopes=["et", "mt", "tt", "em", "ee", "mm"],
)
VectorialHadRecoilPt_boosted = Producer(
    name="VectorialHadRecoilPt_boosted",
    call="quantities::pt({df}, {output}, {input})",
    input=[
        q.mht_p4_boosted,

    ],
    output=[q.mht_pt_boosted],
    scopes=["et", "mt", "tt", "em", "ee", "mm"],
)
VectorialHadRecoilPhi = Producer(
    name="VectorialHadRecoilPhi",
    call="quantities::phi({df}, {output}, {input})",
    input=[
        q.mht_p4,

    ],
    output=[q.mht_phi],
    scopes=["et", "mt", "tt", "em", "ee", "mm"],
)
VectorialHadRecoilPhi_boosted = Producer(
    name="VectorialHadRecoilPhi_boosted",
    call="quantities::phi({df}, {output}, {input})",
    input=[
        q.mht_p4_boosted,

    ],
    output=[q.mht_phi_boosted],
    scopes=["et", "mt", "tt", "em", "ee", "mm"],
)
SoftActivityJetHT = Producer(
    name="SoftActivityJetHT",
    call="basefunctions::rename<Float_t>({df}, {input}, {output})",
    input=[nanoAOD.SoftActivityJetHT],
    output=[q.soft_activity_jet_ht],
    scopes=["et", "mt", "tt", "em", "ee", "mm"],
)
SoftActivityJetHT10 = Producer(
    name="SoftActivityJetHT10",
    call="basefunctions::rename<Float_t>({df}, {input}, {output})",
    input=[nanoAOD.SoftActivityJetHT10],
    output=[q.soft_activity_jet_ht_10],
    scopes=["et", "mt", "tt", "em", "ee", "mm"],
)
HadRecoilQuantities = ProducerGroup(
    name="HadRecoilQuantities",
    call=None,
    input=[],
    output=[],
    scopes=["et", "mt", "tt", "em", "ee", "mm"],
    subproducers=[
        ScalarHadRecoil,
        VectorialHadRecoilP4,
        VectorialHadRecoilPt,
        VectorialHadRecoilPhi,
        SoftActivityJetHT,
        SoftActivityJetHT10,
    ],
)
HadRecoilQuantities_boosted = ProducerGroup(
    name="HadRecoilQuantities_boosted",
    call=None,
    input=[],
    output=[],
    scopes=["et", "mt", "tt", "em", "ee", "mm"],
    subproducers=[
        ScalarHadRecoil_boosted,
        VectorialHadRecoilP4_boosted,
        VectorialHadRecoilPt_boosted,
        VectorialHadRecoilPhi_boosted,
    ],
)
