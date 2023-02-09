from ..quantities import output as q
from ..quantities import nanoAOD as nanoAOD
from code_generation.producer import Producer, ProducerGroup

####################
# Set of producers used for selection possible good jets
####################
FatJetPtCorrection = Producer(
    name="FatJetPtCorrection",
    call="physicsobject::jet::JetPtCorrection({df}, {output}, {input}, {fatjet_reapplyJES}, {fatjet_jes_sources}, {fatjet_jes_shift}, {fatjet_jer_shift}, {fatjet_jec_file}, {fatjet_jer_tag}, {fatjet_jes_tag}, {fatjet_jec_algo})",
    input=[
        nanoAOD.FatJet_pt,
        nanoAOD.FatJet_eta,
        nanoAOD.FatJet_phi,
        nanoAOD.FatJet_area,
        nanoAOD.FatJet_rawFactor,
        nanoAOD.FatJet_ID,
        nanoAOD.GenJetAK8_pt,
        nanoAOD.GenJetAK8_eta,
        nanoAOD.GenJetAK8_phi,
        nanoAOD.rho,
    ],
    output=[q.FatJet_pt_corrected],
    scopes=["global"],
)
FatJetPtCorrection_data = Producer(
    name="FatJetPtCorrection_data",
    call="physicsobject::jet::JetPtCorrection_data({df}, {output}, {input}, {fatjet_jec_file}, {fatjet_jes_tag_data}, {fatjet_jec_algo})",
    input=[
        nanoAOD.FatJet_pt,
        nanoAOD.FatJet_eta,
        nanoAOD.FatJet_area,
        nanoAOD.FatJet_rawFactor,
        nanoAOD.rho,
    ],
    output=[q.FatJet_pt_corrected],
    scopes=["global"],
)
FatJetMassCorrection = Producer(
    name="FatJetMassCorrection",
    call="physicsobject::ObjectMassCorrectionWithPt({df}, {output}, {input})",
    input=[
        nanoAOD.FatJet_mass,
        nanoAOD.FatJet_pt,
        q.FatJet_pt_corrected,
    ],
    output=[q.FatJet_mass_corrected],
    scopes=["global"],
)
# in embdedded sample, we simply rename the nanoAOD fatjets to the fatjet_pt_corrected column
RenameFatJetPt = Producer(
    name="RenameFatJetPt",
    call="basefunctions::rename<ROOT::RVec<float>>({df}, {input}, {output})",
    input=[nanoAOD.FatJet_pt],
    output=[q.FatJet_pt_corrected],
    scopes=["global"],
)
RenameFatJetMass = Producer(
    name="RenameFatJetMass",
    call="basefunctions::rename<ROOT::RVec<float>>({df}, {input}, {output})",
    input=[nanoAOD.FatJet_mass],
    output=[q.FatJet_mass_corrected],
    scopes=["global"],
)
RenameFatJetsData = ProducerGroup(
    name="RenameFatJetsData",
    call=None,
    input=None,
    output=None,
    scopes=["global"],
    subproducers=[RenameFatJetPt, RenameFatJetMass],
)
FatJetEnergyCorrection = ProducerGroup(
    name="FatJetEnergyCorrection",
    call=None,
    input=None,
    output=None,
    scopes=["global"],
    subproducers=[FatJetPtCorrection, FatJetMassCorrection],
)
FatJetEnergyCorrection_data = ProducerGroup(
    name="FatJetEnergyCorrection",
    call=None,
    input=None,
    output=None,
    scopes=["global"],
    subproducers=[FatJetPtCorrection_data, FatJetMassCorrection],
)

FatJetPtCut = Producer(
    name="FatJetPtCut",
    call="physicsobject::CutPt({df}, {input}, {output}, {min_fatjet_pt})",
    input=[q.FatJet_pt_corrected],
    output=[],
    scopes=["global"],
)
FatJetEtaCut = Producer(
    name="FatJetEtaCut",
    call="physicsobject::CutEta({df}, {input}, {output}, {max_fatjet_eta})",
    input=[nanoAOD.FatJet_eta],
    output=[],
    scopes=["global"],
)
FatJetIDCut = Producer(
    name="FatJetIDCut",
    call="physicsobject::jet::CutID({df}, {output}, {input}, {fatjet_id})",
    input=[nanoAOD.FatJet_ID],
    output=[q.fatjet_id_mask],
    scopes=["global"],
)
GoodFatJets = ProducerGroup(
    name="GoodFatJets",
    call="physicsobject::CombineMasks({df}, {output}, {input})",
    input=[],
    output=[q.good_fatjets_mask],
    scopes=["global"],
    subproducers=[FatJetPtCut, FatJetEtaCut, FatJetIDCut],
)

####################
# Set of producers to apply a veto of fatjets overlapping with ditaupair candidates and ordering fatjets by their pt
# 1. check all fatjets vs the two lepton candidates, if they are not within deltaR = 0.5, keep them --> mask
# 2. Combine mask with good_fatjets_mask
# 3. Generate FatJetCollection, an RVec containing all indices of good FatJets in pt order
# 4. generate fatjet quantity outputs
####################
VetoOverlappingFatJets = Producer(
    name="VetoOverlappingFatJets",
    call="jet::VetoOverlappingJets({df}, {output}, {input}, {deltaR_fatjet_veto})",
    input=[nanoAOD.FatJet_eta, nanoAOD.FatJet_phi, q.p4_1, q.p4_2],
    output=[q.fatjet_overlap_veto_mask],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)

GoodFatJetsWithVeto = ProducerGroup(
    name="GoodJetsWithVeto",
    call="physicsobject::CombineMasks({df}, {output}, {input})",
    input=[q.good_fatjets_mask],
    output=[],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
    subproducers=[VetoOverlappingFatJets],
)

FatJetCollection = ProducerGroup(
    name="FatJetCollection",
    call="jet::OrderJetsByPt({df}, {output}, {input})",
    input=[q.FatJet_pt_corrected],
    output=[q.good_fatjet_collection],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
    subproducers=[GoodFatJetsWithVeto],
)

##########################
# Basic FatJet Quantities
# n_fatjets, pt, eta, phi, b-tag value
##########################

LVFatJet1 = Producer(
    name="LVFatJet1",
    call="lorentzvectors::build({df}, {input_vec}, 0, {output})",
    input=[
        q.good_fatjet_collection,
        q.FatJet_pt_corrected,
        nanoAOD.FatJet_eta,
        nanoAOD.FatJet_phi,
        q.FatJet_mass_corrected,
    ],
    output=[q.fatjet_p4_1],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)

NumberOfFatJets = Producer(
    name="NumberOfFatJets",
    call="quantities::jet::NumberOfJets({df}, {output}, {input})",
    input=[q.good_fatjet_collection],
    output=[q.nfatjets],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
fj_pt_1 = Producer(
    name="fj_pt_1",
    call="quantities::pt({df}, {output}, {input})",
    input=[q.fatjet_p4_1],
    output=[q.fj_pt_1],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
fj_eta_1 = Producer(
    name="fj_eta_1",
    call="quantities::eta({df}, {output}, {input})",
    input=[q.fatjet_p4_1],
    output=[q.fj_eta_1],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
fj_phi_1 = Producer(
    name="fj_phi_1",
    call="quantities::phi({df}, {output}, {input})",
    input=[q.fatjet_p4_1],
    output=[q.fj_phi_1],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
fj_mass_1 = Producer(
    name="fj_mass_1",
    call="quantities::mass({df}, {output}, {input})",
    input=[q.fatjet_p4_1],
    output=[q.fj_mass_1],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
fj_msoftdrop_1 = Producer(
    name="msoftdrop_1",
    call="quantities::fatjet::msoftdrop({df}, {output}, {input}, 0)",
    input=[nanoAOD.FatJet_msoftdrop, q.good_fatjet_collection],
    output=[q.fj_msoftdrop_1],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
fj_particleNet_XbbvsQCD_1 = Producer(
    name="particleNet_XbbvsQCD",
    call="quantities::fatjet::particleNet_XbbvsQCD({df}, {output}, {input}, 0)",
    input=[nanoAOD.FatJet_PNet_Xbb, nanoAOD.FatJet_PNet_QCD, q.good_fatjet_collection],
    output=[q.fj_particleNet_XbbvsQCD_1],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
fj_nsubjettiness_2over1_1 = Producer(
    name="nsubjettiness_2over1",
    call="quantities::fatjet::nsubjettiness_ratio({df}, {output}, {input}, 0)",
    input=[nanoAOD.FatJet_tau2, nanoAOD.FatJet_tau1, q.good_fatjet_collection],
    output=[q.fj_nsubjettiness_2over1_1],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
fj_nsubjettiness_3over2_1 = Producer(
    name="nsubjettiness_3over2",
    call="quantities::fatjet::nsubjettiness_ratio({df}, {output}, {input}, 0)",
    input=[nanoAOD.FatJet_tau3, nanoAOD.FatJet_tau2, q.good_fatjet_collection],
    output=[q.fj_nsubjettiness_3over2_1],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)

BasicFatJetQuantities = ProducerGroup(
    name="BasicFatJetQuantities",
    call=None,
    input=None,
    output=None,
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
    subproducers=[
        LVFatJet1,
        NumberOfFatJets,
        fj_pt_1,
        fj_eta_1,
        fj_phi_1,
        fj_mass_1,
        fj_msoftdrop_1,
        fj_particleNet_XbbvsQCD_1,
        fj_nsubjettiness_2over1_1,
        fj_nsubjettiness_3over2_1,
    ],
)

FindFatjetMatchingBjet = Producer(
    name="FindFatjetMatchingBjet",
    call="fatjet::FindFatjetMatchingBjet({df}, {output}, {input}, {fatjet_bpair_matching_max_dR})",
    input=[
        q.good_fatjet_collection,
        q.FatJet_pt_corrected,
        nanoAOD.FatJet_eta,
        nanoAOD.FatJet_phi,
        q.FatJet_mass_corrected,
        q.bpair_p4_1,
    ],
    output=[q.bpair_fatjet],
    scopes=["et", "mt", "tt", "em", "mm", "ee"],
)
LVmatchedFatJet = Producer(
    name="LVmatchedFatJet",
    call="lorentzvectors::build({df}, {input_vec}, 0, {output})",
    input=[
        q.bpair_fatjet,
        q.FatJet_pt_corrected,
        nanoAOD.FatJet_eta,
        nanoAOD.FatJet_phi,
        q.FatJet_mass_corrected,
    ],
    output=[q.matched_fatjet_p4],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
fj_matched_pt = Producer(
    name="fj_matched_pt",
    call="quantities::pt({df}, {output}, {input})",
    input=[q.matched_fatjet_p4],
    output=[q.fj_matched_pt],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
fj_matched_eta = Producer(
    name="fj_matched_eta",
    call="quantities::eta({df}, {output}, {input})",
    input=[q.matched_fatjet_p4],
    output=[q.fj_matched_eta],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
fj_matched_phi = Producer(
    name="fj_matched_phi",
    call="quantities::phi({df}, {output}, {input})",
    input=[q.matched_fatjet_p4],
    output=[q.fj_matched_phi],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
fj_matched_mass = Producer(
    name="fj_matched_mass",
    call="quantities::mass({df}, {output}, {input})",
    input=[q.fatjet_p4_1],
    output=[q.fj_matched_mass],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
fj_matched_msoftdrop = Producer(
    name="fj_matched_msoftdrop",
    call="quantities::fatjet::msoftdrop({df}, {output}, {input}, 0)",
    input=[nanoAOD.FatJet_msoftdrop, q.bpair_fatjet],
    output=[q.fj_matched_msoftdrop],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
fj_matched_particleNet_XbbvsQCD = Producer(
    name="fj_matched_particleNet_XbbvsQCD",
    call="quantities::fatjet::particleNet_XbbvsQCD({df}, {output}, {input}, 0)",
    input=[nanoAOD.FatJet_PNet_Xbb, nanoAOD.FatJet_PNet_QCD, q.bpair_fatjet],
    output=[q.fj_matched_particleNet_XbbvsQCD],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
fj_matched_nsubjettiness_2over1 = Producer(
    name="fj_matched_nsubjettiness_2over1",
    call="quantities::fatjet::nsubjettiness_ratio({df}, {output}, {input}, 0)",
    input=[nanoAOD.FatJet_tau2, nanoAOD.FatJet_tau1, q.bpair_fatjet],
    output=[q.fj_matched_nsubjettiness_2over1],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
fj_matched_nsubjettiness_3over2 = Producer(
    name="fj_matched_nsubjettiness_3over2",
    call="quantities::fatjet::nsubjettiness_ratio({df}, {output}, {input}, 0)",
    input=[nanoAOD.FatJet_tau3, nanoAOD.FatJet_tau2, q.bpair_fatjet],
    output=[q.fj_matched_nsubjettiness_3over2],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)

BasicMatchedFatJetQuantities = ProducerGroup(
    name="BasicMatchedFatJetQuantities",
    call=None,
    input=None,
    output=None,
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
    subproducers=[
        LVmatchedFatJet,
        fj_matched_pt,
        fj_matched_eta,
        fj_matched_phi,
        fj_matched_mass,
        fj_matched_msoftdrop,
        fj_matched_particleNet_XbbvsQCD,
        fj_matched_nsubjettiness_2over1,
        fj_matched_nsubjettiness_3over2,
    ],
)
