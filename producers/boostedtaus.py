from ..quantities import output as q
from ..quantities import nanoAOD as nanoAOD
from code_generation.producer import Producer, ProducerGroup


####################
# Set of producers used for selection of good boosted taus
####################

boostedTauPtCorrection = Producer(
    name="boostedTauPtCorrection",
    call="basefunctions::rename<ROOT::RVec<float>>({df}, {input}, {output})",
    input=[nanoAOD.boostedTau_pt],
    output=[q.boostedTau_pt_corrected],
    scopes=["et", "mt", "tt"],
)
boostedTauMassCorrection = Producer(
    name="boostedTauMassCorrection",
    call="physicsobject::ObjectMassCorrectionWithPt({df}, {output}, {input})",
    input=[
        nanoAOD.boostedTau_mass,
        nanoAOD.boostedTau_pt,
        q.boostedTau_pt_corrected,
    ],
    output=[q.boostedTau_mass_corrected],
    scopes=["et", "mt", "tt"],
)
boostedTauEnergyCorrection = ProducerGroup(
    name="boostedTauEnergyCorrection",
    call=None,
    input=None,
    output=None,
    scopes=["et", "mt", "tt"],
    subproducers=[
        boostedTauPtCorrection,
        boostedTauMassCorrection,
    ],
)

boostedTauPtCut = Producer(
    name="boostedTauPtCut",
    call="physicsobject::CutPt({df}, {input}, {output}, {min_boostedtau_pt})",
    input=[q.boostedTau_pt_corrected],
    output=[],
    scopes=["et", "mt", "tt"],
)
boostedTauEtaCut = Producer(
    name="boostedTauEtaCut",
    call="physicsobject::CutEta({df}, {input}, {output}, {max_boostedtau_eta})",
    input=[nanoAOD.boostedTau_eta],
    output=[],
    scopes=["et", "mt", "tt"],
)
boostedTauDMCut = Producer(
    name="boostedTauDMCut",
    call="physicsobject::tau::CutDecayModes({df}, {output}, {input}, {vec_open}{tau_dms}{vec_close})",
    input=[nanoAOD.boostedTau_decayMode],
    output=[],
    scopes=["et", "mt", "tt"],
)
MVAisoBoostedTauIDCut = Producer(
    name="MVAisoBoostedTauIDCut",
    call="physicsobject::tau::CutTauID({df}, {output}, {input}, {iso_boostedtau_id_bit})",
    input=[nanoAOD.boostedTau_iso_ID],
    output=[],
    scopes=["et", "mt", "tt"],
)
AntiEleBoostedTauIDCut = Producer(
    name="AntiEleBoostedTauIDCut",
    call="physicsobject::tau::CutTauID({df}, {output}, {input}, {antiele_boostedtau_id_bit})",
    input=[nanoAOD.boostedTau_antiEle_ID],
    output=[],
    scopes=["et", "mt", "tt"],
)
AntiMuBoostedTauIDCut = Producer(
    name="AntiMuBoostedTauIDCut",
    call="physicsobject::tau::CutTauID({df}, {output}, {input}, {antimu_boostedtau_id_bit})",
    input=[nanoAOD.boostedTau_antiMu_ID],
    output=[],
    scopes=["et", "mt", "tt"],
)

GoodBoostedTaus = ProducerGroup(
    name="GoodBoostedTaus",
    call="physicsobject::CombineMasks({df}, {output}, {input})",
    input=[],
    output=[q.good_boostedtaus_mask],
    scopes=["et", "mt", "tt"],
    subproducers=[
        boostedTauPtCut,
        boostedTauEtaCut,
        boostedTauDMCut,
        MVAisoBoostedTauIDCut,
        AntiEleBoostedTauIDCut,
        AntiMuBoostedTauIDCut,
    ],
)
NumberOfGoodBoostedTaus = Producer(
    name="NumberOfGoodBoostedTaus",
    call="quantities::NumberOfGoodLeptons({df}, {output}, {input})",
    input=[q.good_boostedtaus_mask],
    output=[q.nboostedtaus],
    scopes=["mt", "et", "tt"],
)