from ..quantities import output as q
from ..quantities import nanoAOD as nanoAOD
from code_generation.producer import Producer, ProducerGroup, ExtendedVectorProducer


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

####################
# Set of producers for quantities of good boosted taus
####################

boostedLVMu1 = Producer(
    name="boostedLVMu1",
    call="lorentzvectors::build({df}, {input_vec}, 0, {output})",
    input=[
        q.boosteddileptonpair,
        nanoAOD.Muon_pt,
        nanoAOD.Muon_eta,
        nanoAOD.Muon_phi,
        nanoAOD.Muon_mass,
    ],
    output=[q.boosted_p4_1],
    scopes=["mt", "mm"],
)
boostedLVTau2 = Producer(
    name="boostedLVTau2",
    call="lorentzvectors::build({df}, {input_vec}, 1, {output})",
    input=[
        q.boosteddileptonpair,
        q.boostedTau_pt_corrected,
        nanoAOD.boostedTau_eta,
        nanoAOD.boostedTau_phi,
        q.boostedTau_mass_corrected,
    ],
    output=[q.boosted_p4_2],
    scopes=["mt", "et", "tt"],
)

boosted_pt_1 = Producer(
    name="boosted_pt_1",
    call="quantities::pt({df}, {output}, {input})",
    input=[q.boosted_p4_1],
    output=[q.boosted_pt_1],
    scopes=["mt", "et", "tt", "em", "ee", "mm"],
)
boosted_pt_2 = Producer(
    name="boosted_pt_2",
    call="quantities::pt({df}, {output}, {input})",
    input=[q.boosted_p4_2],
    output=[q.boosted_pt_2],
    scopes=["mt", "et", "tt", "em", "ee", "mm"],
)
boosted_eta_1 = Producer(
    name="boosted_eta_1",
    call="quantities::eta({df}, {output}, {input})",
    input=[q.boosted_p4_1],
    output=[q.boosted_eta_1],
    scopes=["mt", "et", "tt", "em", "ee", "mm"],
)
boosted_eta_2 = Producer(
    name="boosted_eta_2",
    call="quantities::eta({df}, {output}, {input})",
    input=[q.boosted_p4_2],
    output=[q.boosted_eta_2],
    scopes=["mt", "et", "tt", "em", "ee", "mm"],
)
boosted_phi_1 = Producer(
    name="boosted_phi_1",
    call="quantities::phi({df}, {output}, {input})",
    input=[q.boosted_p4_1],
    output=[q.boosted_phi_1],
    scopes=["mt", "et", "tt", "em", "ee", "mm"],
)
boosted_phi_2 = Producer(
    name="boosted_phi_2",
    call="quantities::phi({df}, {output}, {input})",
    input=[q.boosted_p4_2],
    output=[q.boosted_phi_2],
    scopes=["mt", "et", "tt", "em", "ee", "mm"],
)
boosted_mass_1 = Producer(
    name="boosted_mass_1",
    call="quantities::mass({df}, {output}, {input})",
    input=[q.boosted_p4_1],
    output=[q.boosted_mass_1],
    scopes=["mt", "et", "tt", "em", "ee", "mm"],
)
boosted_mass_2 = Producer(
    name="boosted_mass_2",
    call="quantities::mass({df}, {output}, {input})",
    input=[q.boosted_p4_2],
    output=[q.boosted_mass_2],
    scopes=["mt", "et", "tt", "em", "ee", "mm"],
)

boosted_muon_dxy_1 = Producer(
    name="boosted_muon_dxy_1",
    call="quantities::dxy({df}, {output}, 0, {input})",
    input=[q.boosteddileptonpair, nanoAOD.Muon_dxy],
    output=[q.boosted_dxy_1],
    scopes=["mt", "mm"],
)
boosted_muon_dz_1 = Producer(
    name="boosted_muon_dz_1",
    call="quantities::dz({df}, {output}, 0, {input})",
    input=[q.boosteddileptonpair, nanoAOD.Muon_dz],
    output=[q.boosted_dz_1],
    scopes=["mt", "mm"],
)
boosted_muon_q_1 = Producer(
    name="boosted_muon_q_1",
    call="quantities::charge({df}, {output}, 0, {input})",
    input=[q.boosteddileptonpair, nanoAOD.Muon_charge],
    output=[q.boosted_q_1],
    scopes=["mt", "mm"],
)
boosted_muon_iso_1 = Producer(
    name="boosted_muon_iso_1",
    call="quantities::isolation({df}, {output}, 0, {input})",
    input=[q.boosteddileptonpair, nanoAOD.Muon_iso],
    output=[q.boosted_iso_1],
    scopes=["mt", "mm"],
)
boosted_muon_is_global_1 = Producer(
    name="boosted_muon_is_global_1",
    call="quantities::muon::is_global({df}, {output}, 0, {input})",
    input=[q.boosteddileptonpair, nanoAOD.Muon_isGlobal],
    output=[q.boosted_is_global_1],
    scopes=["mt", "mm"],
)
boosted_tau_decaymode_1_notau = Producer(
    name="boosted_tau_decaymode_1_notau",
    call="basefunctions::DefineQuantity({df}, {output}, -1)",
    input=[],
    output=[q.boosted_tau_decaymode_1],
    scopes=["et", "mt", "em", "ee", "mm"],
)

# boosted_tau_dxy_2 = Producer(
#     name="boosted_tau_dxy_2",
#     call="quantities::dxy({df}, {output}, 1, {input})",
#     input=[q.boosteddileptonpair, nanoAOD.Tau_dxy],
#     output=[q.boosted_dxy_2],
#     scopes=["mt", "et", "tt"],
# )
# boosted_tau_dz_2 = Producer(
#     name="boosted_tau_dz_2",
#     call="quantities::dz({df}, {output}, 1, {input})",
#     input=[q.boosteddileptonpair, nanoAOD.Tau_dz],
#     output=[q.boosted_dz_2],
#     scopes=["mt", "et", "tt"],
# )
boosted_tau_q_2 = Producer(
    name="boosted_tau_q_2",
    call="quantities::charge({df}, {output}, 1, {input})",
    input=[q.boosteddileptonpair, nanoAOD.boostedTau_charge],
    output=[q.boosted_q_2],
    scopes=["mt", "et", "tt"],
)
boosted_tau_iso_2 = Producer(
    name="boosted_tau_iso_2",
    call="quantities::isolation({df}, {output}, 1, {input})",
    input=[q.boosteddileptonpair, nanoAOD.boostedTau_iso_IDraw],
    output=[q.boosted_iso_2],
    scopes=["mt", "et", "tt"],
)
boosted_tau_decaymode_2 = Producer(
    name="boosted_taudecaymode_2",
    call="quantities::tau::decaymode({df}, {output}, 1, {input})",
    input=[q.boosteddileptonpair, nanoAOD.boostedTau_decayMode],
    output=[q.boosted_tau_decaymode_2],
    scopes=["mt", "et", "tt"],
)
boosted_tau_gen_match_2 = Producer(
    name="boosted_tau_gen_match_2",
    call="quantities::tau::genmatch({df}, {output}, 1, {input})",
    input=[q.boosteddileptonpair, nanoAOD.boostedTau_genMatch],
    output=[q.boosted_tau_gen_match_2],
    scopes=["mt", "et", "tt"],
)
boosted_taujet_pt_2 = Producer(
    name="boosted_taujet_pt_2",
    call="quantities::tau::matching_jet_pt({df}, {output}, 1, {input})",
    input=[q.boosteddileptonpair, nanoAOD.boostedTau_associatedJet, nanoAOD.FatJet_pt],
    output=[q.boosted_taujet_pt_2],
    scopes=["mt", "et", "tt"],
)
isoTauIDFlag_2 = ExtendedVectorProducer(
    name="isoTauIDFlag_2",
    call="quantities::tau::TauIDFlag({df}, {output}, 1, {input}, {iso_boostedtau_id_WPbit})",
    input=[q.boosteddileptonpair, nanoAOD.boostedTau_iso_ID],
    output="boostedtau_2_iso_id_outputname",
    scope=["et", "mt", "tt"],
    vec_config="iso_boostedtau_id",
)
antiEleTauIDFlag_2 = ExtendedVectorProducer(
    name="antiEleTauIDFlag_2",
    call="quantities::tau::TauIDFlag({df}, {output}, 1, {input}, {antiele_boostedtau_id_WPbit})",
    input=[q.boosteddileptonpair, nanoAOD.boostedTau_antiEle_ID],
    output="boostedtau_2_antiele_id_outputname",
    scope=["et", "mt", "tt"],
    vec_config="antiele_boostedtau_id",
)
antiMuTauIDFlag_2 = ExtendedVectorProducer(
    name="antiMuTauIDFlag_2",
    call="quantities::tau::TauIDFlag({df}, {output}, 1, {input}, {antimu_boostedtau_id_WPbit})",
    input=[q.boosteddileptonpair, nanoAOD.boostedTau_antiMu_ID],
    output="boostedtau_2_antimu_id_outputname",
    scope=["et", "mt", "tt"],
    vec_config="antimu_boostedtau_id",
)

boosted_p4_vis = Producer(
    name="boosted_p4_vis",
    call="lorentzvectors::CombineP4s({df}, {output}, {input})",
    input=[q.boosted_p4_1, q.boosted_p4_2],
    output=[q.boosted_p4_vis],
    scopes=["mt", "et", "tt", "em", "ee", "mm"],
)
boosted_m_vis = Producer(
    name="boosted_m_vis",
    call="quantities::mass({df}, {output}, {input})",
    input=[q.boosted_p4_vis],
    output=[q.boosted_m_vis],
    scopes=["mt", "et", "tt", "em", "ee", "mm"],
)
boosted_pt_vis = Producer(
    name="boosted_pt_vis",
    call="quantities::pt({df}, {output}, {input})",
    input=[q.boosted_p4_vis],
    output=[q.boosted_pt_vis],
    scopes=["mt", "et", "tt", "em", "ee", "mm"],
)
boosted_deltaR_ditaupair = Producer(
    name="boosted_deltaR_ditaupair",
    call="quantities::deltaR({df}, {output}, {input})",
    input=[q.boosted_p4_1, q.boosted_p4_2],
    output=[q.boosted_deltaR_ditaupair],
    scopes=["mt", "et", "tt", "em", "ee", "mm"],
)

UnrollboostedMuLV1 = ProducerGroup(
    name="UnrollboostedMuLV1",
    call=None,
    input=None,
    output=None,
    scopes=["mt", "mm"],
    subproducers=[
        boosted_pt_1,
        boosted_eta_1,
        boosted_phi_1,
        boosted_mass_1,
        boosted_muon_dxy_1,
        boosted_muon_dz_1,
        boosted_muon_q_1,
        boosted_muon_iso_1,
        boosted_muon_is_global_1,
    ],
)
UnrollboostedTauLV2 = ProducerGroup(
    name="UnrollboostedTauLV2",
    call=None,
    input=None,
    output=None,
    scopes=["et", "mt", "tt"],
    subproducers=[
        boosted_pt_2,
        boosted_eta_2,
        boosted_phi_2,
        boosted_mass_2,
        # tau_dxy_2,
        # tau_dz_2,
        boosted_tau_q_2,
        boosted_tau_iso_2,
        boosted_tau_decaymode_2,
        # boosted_tau_gen_match_2,
        boosted_taujet_pt_2,
        isoTauIDFlag_2,
        antiEleTauIDFlag_2,
        antiMuTauIDFlag_2,
    ],
)
boostedMTDiTauPairQuantities = ProducerGroup(
    name="boostedMTDiTauPairQuantities",
    call=None,
    input=None,
    output=None,
    scopes=["mt"],
    subproducers=[
        UnrollboostedMuLV1,
        UnrollboostedTauLV2,
        boosted_tau_decaymode_1_notau,
        boosted_p4_vis,
        boosted_m_vis,
        boosted_pt_vis,
        boosted_deltaR_ditaupair,
    ],
)