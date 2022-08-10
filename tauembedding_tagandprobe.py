from __future__ import annotations  # needed for type annotations in > python 3.7

from typing import List

from .producers import event as event
from .producers import muons as muons
from .producers import taus as taus
from .producers import electrons as electrons
from .producers import pairquantities as pairquantities
from .producers import pairselection as pairselection
from .producers import embedding as emb
from .producers import tagandprobe as tagandprobe
from .producers import scalefactors as scalefactors
from .producers import triggers as triggers
from .quantities import nanoAOD as nanoAOD
from .quantities import output as q
from .quantities import tagandprobe_output as tp_q
from code_generation.configuration import Configuration
from code_generation.rules import AppendProducer
from code_generation.modifiers import EraModifier
from code_generation.rules import AppendProducer, RemoveProducer, ReplaceProducer

from .producers import met as met



def build_config(
    era: str,
    sample: str,
    channels: List[str],
    shifts: List[str],
    available_sample_types: List[str],
    available_eras: List[str],
    available_channels: List[str],
):

    if sample != "data" and sample != "embedding" and sample != "dyjets":
        print(
            "WARNING: TagandProbe measurement uses only data, dyjets and embedding samples"
        )
        exit()
    configuration = Configuration(
        era,
        sample,
        channels,
        shifts,
        available_sample_types,
        available_eras,
        available_channels,
    )
    # first add default parameters necessary for all scopes
    configuration.add_config_parameters(
        "global",
        {
            "min_muon_pt": 7.0,
            "max_muon_eta": 2.5,
             "max_muon_dxy": 0.045,
            "max_muon_dz": 0.2,
            "muon_id": "Muon_mediumId",
            "muon_iso_cut": 0.3,
            "min_dimuonveto_pt": 7,
            "min_dimuonveto_eta": 2.5,
            "dimuonveto_id" : "Muon_looseId",
            "dileptonveto_dR" : 0.5, 
            "min_ele_pt": 7.0,
            "max_ele_eta": 2.5,
            "met_filters": [
                "Flag_BadPFMuonFilter",
                "Flag_METFilters",
                "Flag_muonBadTrackFilter",
            ],
        },
    )
    ###### Channel Specifics ######
    # MuMu channel Muon selection
    configuration.add_config_parameters(
        ["mm"],
        {
            "muon_index_in_pair": 0,
            "second_muon_index_in_pair": 1,
            "min_muon_pt": 7.0,
            "max_muon_eta": 2.5,
            "pairselection_min_dR": 0.5,
        },
    )
    # ElEl channel Electron selection
    configuration.add_config_parameters(
        ["ee"],
        {
            "electron_index_in_pair": 0,
            "second_electron_index_in_pair": 1,
            "min_electron_pt": 7.0,
            "max_electron_eta": 2.5,
            "pairselection_min_dR": 0.5,
        },
    )

    # MuTau channel Muon selection
    configuration.add_config_parameters(
        ["mt"],
        {
            "min_muon_pt": 20.0,
            "max_muon_eta": 2.3,
            "muon_index_in_pair": 0,
            "second_muon_index_in_pair": 1,
            # "pairselection_min_dR": 0.5,
        },
    )

      # MuTau channel Tau selection
    configuration.add_config_parameters(
        ["mt"],
        {
            "min_tau_pt": 20.0,
            "max_tau_eta": 2.3,
            "max_tau_dz" : 0.2,
            "tau_dms" : "0,1,10,11",
            "pairselection_min_dR": 0.5,
            "vsjet_tau_id_bit" : 3 ,
            "vsele_tau_id_bit" : 3,
            "vsmu_tau_id_bit" : 3, 
  
        },
    )

    # MuMu Channel Trigger setup
    configuration.add_config_parameters(
        ["mm"],
        {
            "singlemoun_trigger": EraModifier(
                {
                    "2018": [
                        {
                            "flagname_1": "trg_IsoMu24_1",
                            "flagname_2": "trg_IsoMu24_2",
                            "hlt_path": "HLT_IsoMu24",
                            "ptcut": 25,
                            "etacut": 2.5,
                            "filterbit": 3,
                            "trigger_particle_id": 13,
                            "max_deltaR_triggermatch": 0.4,
                        },
                        {
                            "flagname_1": "trg_IsoMu27_1",
                            "flagname_2": "trg_IsoMu27_2",
                            "hlt_path": "HLT_IsoMu27",
                            "ptcut": 28,
                            "etacut": 2.5,
                            "filterbit": 3,
                            "trigger_particle_id": 13,
                            "max_deltaR_triggermatch": 0.4,
                        },
                        {
                            "flagname_1": "trg_Mu17TrkMu8_DZ_Mu17_1",
                            "flagname_2": "trg_Mu17TrkMu8_DZ_Mu17_2",
                            "hlt_path": "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ",
                            "ptcut": 18,
                            "etacut": 2.5,
                            "filterbit": 4,
                            "trigger_particle_id": 13,
                            "max_deltaR_triggermatch": 0.4,
                        },
                        {
                            "flagname_1": "trg_Mu17TrkMu8_DZ_Mu8_1",
                            "flagname_2": "trg_Mu17TrkMu8_DZ_Mu8_2",
                            "hlt_path": "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ",
                            "ptcut": 18,
                            "etacut": 2.5,
                            "filterbit": 4,
                            "trigger_particle_id": 13,
                            "max_deltaR_triggermatch": 0.4,
                        },
                        {
                            "flagname_1": "trg_Mu17TrkMu8_DZMass8_Mu17_1",
                            "flagname_2": "trg_Mu17TrkMu8_DZMass8_Mu17_2",
                            "hlt_path": "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8",
                            "ptcut": 9,
                            "etacut": 2.5,
                            "filterbit": 4,
                            "trigger_particle_id": 13,
                            "max_deltaR_triggermatch": 0.4,
                        },
                        {
                            "flagname_1": "trg_Mu17TrkMu8_DZMass8_Mu8_1",
                            "flagname_2": "trg_Mu17TrkMu8_DZMass8_Mu8_2",
                            "hlt_path": "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8",
                            "ptcut": 9,
                            "etacut": 2.5,
                            "filterbit": 4,
                            "trigger_particle_id": 13,
                            "max_deltaR_triggermatch": 0.4,
                        },
                    ],
                }
            ),
        },
    )
    # ElEl Channel Trigger setup
    configuration.add_config_parameters(
        ["ee"],
        {
            "singleelectron_trigger": EraModifier(
                {
                    "2018": [
                        {
                            "flagname_1": "trg_single_ele27_1",
                            "flagname_2": "trg_single_ele27_2",
                            "hlt_path": "HLT_Ele27_WPTight_Gsf",
                            "ptcut": 28,
                            "etacut": 2.1,
                            "filterbit": 1,
                            "trigger_particle_id": 11,
                            "max_deltaR_triggermatch": 0.4,
                        },
                        {
                            "flagname_1": "trg_single_ele32_1",
                            "flagname_2": "trg_single_ele32_2",
                            "hlt_path": "HLT_Ele32_WPTight_Gsf",
                            "ptcut": 33,
                            "etacut": 2.1,
                            "filterbit": 1,
                            "trigger_particle_id": 11,
                            "max_deltaR_triggermatch": 0.4,
                        },
                        {
                            "flagname_1": "trg_single_ele35_1",
                            "flagname_2": "trg_single_ele35_2",
                            "hlt_path": "HLT_Ele35_WPTight_Gsf",
                            "ptcut": 36,
                            "etacut": 2.1,
                            "filterbit": 1,
                            "trigger_particle_id": 11,
                            "max_deltaR_triggermatch": 0.4,
                        },
                    ],
                }
            ),
        },
    )


    # MuTau Channel Trigger setup
    configuration.add_config_parameters(
        ["mt"],
        {
            "singlemoun_trigger": EraModifier(
                {
                    "2018": [
                        {
                            "flagname_1": "trg_IsoMu24_1",
                            "flagname_2": "trg_IsoMu24_2",
                            "hlt_path": "HLT_IsoMu24",
                            "ptcut": 25,
                            "etacut": 2.5,
                            "filterbit": 3,
                            "trigger_particle_id": 13,
                            "max_deltaR_triggermatch": 0.4,
                        },
                        {
                            "flagname_1": "trg_IsoMu27_1",
                            "flagname_2": "trg_IsoMu27_2",
                            "hlt_path": "HLT_IsoMu27",
                            "ptcut": 28,
                            "etacut": 2.5,
                            "filterbit": 3,
                            "trigger_particle_id": 13,
                            "max_deltaR_triggermatch": 0.4,
                        },
                        {
                            "flagname_1": "trg_Mu17TrkMu8_DZ_Mu17_1",
                            "flagname_2": "trg_Mu17TrkMu8_DZ_Mu17_2",
                            "hlt_path": "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ",
                            "ptcut": 18,
                            "etacut": 2.5,
                            "filterbit": 4,
                            "trigger_particle_id": 13,
                            "max_deltaR_triggermatch": 0.4,
                        },
                        {
                            "flagname_1": "trg_Mu17TrkMu8_DZ_Mu8_1",
                            "flagname_2": "trg_Mu17TrkMu8_DZ_Mu8_2",
                            "hlt_path": "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ",
                            "ptcut": 18,
                            "etacut": 2.5,
                            "filterbit": 4,
                            "trigger_particle_id": 13,
                            "max_deltaR_triggermatch": 0.4,
                        },
                        {
                            "flagname_1": "trg_Mu17TrkMu8_DZMass8_Mu17_1",
                            "flagname_2": "trg_Mu17TrkMu8_DZMass8_Mu17_2",
                            "hlt_path": "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8",
                            "ptcut": 9,
                            "etacut": 2.5,
                            "filterbit": 4,
                            "trigger_particle_id": 13,
                            "max_deltaR_triggermatch": 0.4,
                        },
                        {
                            "flagname_1": "trg_Mu17TrkMu8_DZMass8_Mu8_1",
                            "flagname_2": "trg_Mu17TrkMu8_DZMass8_Mu8_2",
                            "hlt_path": "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8",
                            "ptcut": 9,
                            "etacut": 2.5,
                            "filterbit": 4,
                            "trigger_particle_id": 13,
                            "max_deltaR_triggermatch": 0.4,
                        },

                    ],
                }
            ),
        },
    )
    
    
        # MuTau Channel Trigger setup
    configuration.add_config_parameters(
        ["mt"],
        {
            "mutau_cross_trigger": EraModifier(
                {
                    "2018": [
                        {
                            "flagname": "trg_cross_mu20tau27_hps",
                            "hlt_path": "HLT_IsoMu20_eta2p1_LooseChargedIsoPFTauHPS27_eta2p1_CrossL1",
                            "p1_ptcut": 21,
                            "p1_etacut": 2.5,
                            "p1_filterbit": 3,
                            "p1_trigger_particle_id": 13,
                            "p2_ptcut": 32,
                            "p2_etacut": 2.1,
                            "p2_filterbit": 4,
                            "p2_trigger_particle_id": 15,
                            "max_deltaR_triggermatch": 0.4,
                        }
                    ],
                }
            ),
        },
    )
    
    
    configuration.add_config_parameters(
        ["mt"],
        {
            "singletau_trigger_trailing": EraModifier(
                {
                    "2018": [
                        
                         {
                            "flagname": "trg_single_tau180_2",
                            "hlt_path": "HLT_MediumChargedIsoPFTau180HighPtRelaxedIso_Trk50_eta2p1",
                            "ptcut": 180,
                            "etacut": 2.1,
                            "filterbit": 5,
                            "trigger_particle_id": 15,
                            "max_deltaR_triggermatch": 0.4,
                        }
                    ],
                }
            ),
        },
    )

    # MuTau Channel Trigger setup
    configuration.add_config_parameters(
        ["mt"],
        {
            "mutau_trigger": EraModifier(
                {
                    "2018": [
                        {
                            "flagname_1": "trg_IsoMu20_hps_tau27_1",
                            "flagname_2": "trg_IsoMu20_hps_tau27_2",
                            "hlt_path": "HLT_IsoMu20_eta2p1_LooseChargedIsoPFTauHPS27_eta2p1_CrossL1",
                            "ptcut": 18,
                            "etacut": 2.1,
                            "filterbit": 4,
                            "trigger_particle_id": 15,
                            "max_deltaR_triggermatch": 0.4,
                        },

                        {
                            "flagname_1": "trg_monitor_mu20tau27_hps_1",
                            "flagname_2": "trg_monitor_mu20tau27_hps_2",
                            "hlt_path": "HLT_IsoMu20_eta2p1_LooseChargedIsoPFTauHPS27_eta2p1_CrossL1",
                            "ptcut": 30,
                            "etacut": 2.1,
                            "filterbit": 4,
                            "trigger_particle_id": 15,
                            "max_deltaR_triggermatch": 0.4,
                        },

                        {
                            "flagname_1": "trg_monitor_mu24tau35_mediso_hps_1",
                            "flagname_2": "trg_monitor_mu24tau35_mediso_hps_2",
                            "hlt_path": "HLT_IsoMu24_eta2p1_MediumChargedIsoPFTauHPS35_Trk1_eta2p1_Reg_CrossL1",
                            "ptcut": 18,
                            "etacut": 2.1,
                            "filterbit": 4,
                            "trigger_particle_id": 15,
                            "max_deltaR_triggermatch": 0.4,
                        },




                    ],
                }
            ),
        },
    )

    configuration.add_producers(
        "global",
        [
            event.Lumi,
            # event.MetFilter,
            tagandprobe.BaseMuons,
            tagandprobe.BaseElectrons,
            muons.DiMuonVeto,
            met.MetBasics,
        ],
    )
    configuration.add_producers(
        "mm",
        [
            tagandprobe.GoodMuons,
            muons.VetoMuons,
            muons.VetoSecondMuon,
            muons.ExtraMuonsVeto,
            muons.NumberOfGoodMuons,
            electrons.ExtraElectronsVeto,
            pairselection.ZMuMuPairSelection,
            pairselection.GoodMuMuPairFilter,
            pairselection.LVMu1,
            pairselection.LVMu2,
            pairselection.LVMu1Uncorrected,
            pairselection.LVMu2Uncorrected,
            pairquantities.MuMuPairQuantities,
            tagandprobe.MuonIDs,
            tagandprobe.MuMuSingleMuonTriggerFlags_1,
            tagandprobe.MuMuSingleMuonTriggerFlags_2,
        ],
    )

    configuration.add_producers(
        "ee",
        [
            tagandprobe.GoodElectrons,
            electrons.VetoElectrons,
            electrons.VetoSecondElectron,
            electrons.ExtraElectronsVeto,
            electrons.NumberOfGoodElectrons,
            pairselection.ZElElPairSelection,
            pairselection.GoodElElPairFilter,
            pairselection.LVEl1,
            pairselection.LVEl2,
            pairquantities.ElElPairQuantities,
            tagandprobe.ElectronIDs,
            tagandprobe.ElElSingleElectronTriggerFlags_1,
            tagandprobe.ElElSingleElectronTriggerFlags_2,
        ],
    )


    configuration.add_producers(
        "mt",
        [
            tagandprobe.GoodMuons,
            muons.VetoMuons,
            muons.VetoSecondMuon,
            muons.ExtraMuonsVeto,
            muons.NumberOfGoodMuons,
            electrons.ExtraElectronsVeto,
            taus.GoodTaus1, 
            pairselection.MTPairSelection,
            pairselection.GoodMTPairFilter,
            pairselection.LVMu1,
            pairselection.LVTau2,
            pairselection.LVMu1Uncorrected,
            pairselection.LVTau2Uncorrected,
            pairquantities.MTDiTauPairQuantities,
            # pairquantities.VsJetTauIDFlag_2,
            # tagandprobe.MuonIDs,
            tagandprobe.MuMuSingleMuonTriggerFlags_1,
            # tagandprobe.MuMuSingleMuonTriggerFlags_2,
            tagandprobe.MuTauSingleTauTriggerFlags_1,
            tagandprobe.MuTauSingleTauTriggerFlags_2,
            # triggers.MTGenerateSingleMuonTriggerFlags,
            triggers.MTGenerateCrossTriggerFlags,
            triggers.GenerateSingleTrailingTauTriggerFlags,
            
            scalefactors.Tau_2_VsEleTauID_SF,
            # pairquantities.VsJetTauIDFlag_2,
            # pairquantities.DiTauPairMETQuantities,
            pairquantities.mt_1,
        ],
    )

    configuration.add_outputs(
        ["mm"],
        [
            nanoAOD.run,
            q.lumi,
            nanoAOD.event,
            q.pt_1,
            q.pt_2,
            q.eta_1,
            q.eta_2,
            q.phi_1,
            q.phi_2,
            tp_q.id_medium_1,
            tp_q.id_medium_2,
            tp_q.id_loose_1,
            tp_q.id_loose_2,
            tp_q.id_tight_1,
            tp_q.id_tight_2,
            q.m_vis,
            q.iso_1,
            q.iso_2,
            q.dz_1,
            q.dz_2,
            q.dxy_1,
            q.dxy_2,
            q.nmuons,
            q.is_global_1,
            q.is_global_2,
            q.muon_veto_flag,
            q.electron_veto_flag,
            tagandprobe.MuMuSingleMuonTriggerFlags_1.output_group,
            tagandprobe.MuMuSingleMuonTriggerFlags_2.output_group,
        ],
    )

    configuration.add_outputs(
        ["ee"],
        [
            nanoAOD.run,
            q.lumi,
            nanoAOD.event,
            q.pt_1,
            q.pt_2,
            q.eta_1,
            q.eta_2,
            q.phi_1,
            q.phi_2,
            q.m_vis,
            q.iso_1,
            q.iso_2,
            q.dz_1,
            q.dz_2,
            q.dxy_1,
            q.dxy_2,
            q.electron_veto_flag,
            tp_q.id_wp90_1,
            tp_q.id_wp90_2,
            tp_q.id_wp80_1,
            tp_q.id_wp80_2,
            q.nelectrons,
            tagandprobe.ElElSingleElectronTriggerFlags_1.output_group,
            tagandprobe.ElElSingleElectronTriggerFlags_2.output_group,
        ],
    )


    configuration.add_outputs(
        ["mt"],
        [
            nanoAOD.run,
            q.lumi,
            nanoAOD.event,
            q.pt_1,
            q.pt_2,
            q.eta_1,
            q.eta_2,
            q.phi_1,
            q.phi_2,
            # tp_q.id_medium_1,
            # tp_q.id_medium_2,
            # tp_q.id_loose_1,
            # tp_q.id_loose_2,
            # tp_q.id_tight_1,
            # tp_q.id_tight_2,
            q.m_vis,
            q.iso_1,
            q.iso_2,
            q.dz_1,
            q.dz_2,
            q.dxy_1,
            q.dxy_2,
            q.nmuons,
            q.is_global_1,
            # q.is_global_2,
            q.muon_veto_flag,
            q.electron_veto_flag,
            q.decaymode_2,
            q.taujet_pt_2,
            q.gen_match_2,
            q.dimuon_veto,
            # q.id_wgt_mu_1,
            # q.iso_wgt_mu_1,
            q.mt_1,

            tagandprobe.MuMuSingleMuonTriggerFlags_1.output_group,
            # tagandprobe.MuMuSingleMuonTriggerFlags_2.output_group,
            tagandprobe.MuTauSingleTauTriggerFlags_1.output_group,
            tagandprobe.MuTauSingleTauTriggerFlags_2.output_group,
            pairquantities.VsEleTauIDFlag_2.output_group,
            pairquantities.VsMuTauIDFlag_2.output_group,
            # triggers.MTGenerateSingleMuonTriggerFlags.output_group,
            triggers.MTGenerateCrossTriggerFlags.output_group,
            triggers.GenerateSingleTrailingTauTriggerFlags.output_group,

            scalefactors.Tau_2_VsEleTauID_SF.output_group,
            pairquantities.VsJetTauIDFlag_2.output_group,
        ],
    )


    configuration.add_config_parameters(
        ["mt"],
        {
            
            "tau_sf_file": EraModifier(
                {
                    "2016": "data/jsonpog-integration/POG/TAU/2016postVFP_UL/tau.json.gz",
                    "2017": "data/jsonpog-integration/POG/TAU/2017_UL/tau.json.gz",
                    "2018": "data/jsonpog-integration/POG/TAU/2018_UL/tau.json.gz",
                }
            ),
            "vsjet_tau_id": [
                {
                    "tau_id_discriminator": "DeepTau2017v2p1VSjet",
                    "tau_1_vsjet_sf_outputname": "id_wgt_tau_vsJet_{wp}_1".format(
                        wp=wp
                    ),
                    "tau_2_vsjet_sf_outputname": "id_wgt_tau_vsJet_{wp}_2".format(
                        wp=wp
                    ),
                    "vsjet_tau_id_WP": "{wp}".format(wp=wp),
                    "tau_1_vsjet_id_outputname": "id_tau_vsJet_{wp}_1".format(wp=wp),
                    "tau_2_vsjet_id_outputname": "id_tau_vsJet_{wp}_2".format(wp=wp),
                    "vsjet_tau_id_WPbit": bit,
                }
                for wp, bit in {
                    "VVVLoose": 1,
                    "VVLoose": 2,
                    "VLoose": 3,
                    "Loose": 4,
                    "Medium": 5,
                    "Tight": 6,
                    "VTight": 7,
                    "VVTight": 8,
                }.items()
            ],
            "vsele_tau_id": [
                {
                    "tau_id_discriminator": "DeepTau2017v2p1VSe",
                    "tau_1_vsele_sf_outputname": "id_wgt_tau_vsEle_{wp}_1".format(
                        wp=wp
                    ),
                    "tau_2_vsele_sf_outputname": "id_wgt_tau_vsEle_{wp}_2".format(
                        wp=wp
                    ),
                    "vsele_tau_id_WP": "{wp}".format(wp=wp),
                    "tau_1_vsele_id_outputname": "id_tau_vsEle_{wp}_1".format(wp=wp),
                    "tau_2_vsele_id_outputname": "id_tau_vsEle_{wp}_2".format(wp=wp),
                    "vsele_tau_id_WPbit": bit,
                }
                for wp, bit in {
                    "VVLoose": 2,
                    "VLoose": 3,
                    "Loose": 4,
                    "Medium": 5,
                    "Tight": 6,
                    "VTight": 7,
                    "VVTight": 8,
                }.items()
            ],
            "vsmu_tau_id": [
                {
                    "tau_id_discriminator": "DeepTau2017v2p1VSmu",
                    "tau_1_vsmu_sf_outputname": "id_wgt_tau_vsMu_{wp}_1".format(wp=wp),
                    "tau_2_vsmu_sf_outputname": "id_wgt_tau_vsMu_{wp}_2".format(wp=wp),
                    "vsmu_tau_id_WP": "{wp}".format(wp=wp),
                    "tau_1_vsmu_id_outputname": "id_tau_vsMu_{wp}_1".format(wp=wp),
                    "tau_2_vsmu_id_outputname": "id_tau_vsMu_{wp}_2".format(wp=wp),
                    "vsmu_tau_id_WPbit": bit,
                }
                for wp, bit in {
                    "VLoose": 1,
                    "Loose": 2,
                    "Medium": 3,
                    "Tight": 4,
                }.items()
            ],
            "tau_sf_vsele_barrel": "nom",  # or "up"/"down" for up/down variation
            "tau_sf_vsele_endcap": "nom",  # or "up"/"down" for up/down variation
            "tau_sf_vsmu_wheel1": "nom",
            "tau_sf_vsmu_wheel2": "nom",
            "tau_sf_vsmu_wheel3": "nom",
            "tau_sf_vsmu_wheel4": "nom",
            "tau_sf_vsmu_wheel5": "nom",
        },
    )

    configuration.add_modification_rule(
        ["mt"],
        RemoveProducer(
            producers=[
                pairquantities.tau_gen_match_2,
                scalefactors.Tau_2_VsEleTauID_SF
            ],
            samples="data",
        ),
    )
    # configuration.add_modification_rule(
    #     ["mt"],
    #     RemoveProducer(
    #         producers=[
    #             scalefactors.Tau_2_VsMuTauID_SF,
    #             scalefactors.Tau_2_VsJetTauID_lt_SF,
    #             scalefactors.Tau_2_VsEleTauID_SF,
    #         ],
    #         samples="data",
    #     ),
    # )



    configuration.add_modification_rule(
        "global",
        AppendProducer(
            producers=emb.EmbeddingQuantities, samples=["embedding", "embedding_mc"]
        ),
    )

    #########################
    # Finalize and validate the configuration
    #########################
    configuration.optimize()
    configuration.validate()
    configuration.report()
    return configuration.expanded_configuration()
