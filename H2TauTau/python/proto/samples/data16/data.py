import PhysicsTools.HeppyCore.framework.config as cfg

#####COMPONENT CREATOR

from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
kreator = ComponentCreator()

# json = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/Cert_271036-273450_13TeV_PromptReco_Collisions16_JSON_NoL1T.txt'
# json = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/Cert_271036-274240_13TeV_PromptReco_Collisions16_JSON.txt' # 0.8/fb
# json = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/Cert_271036-274421_13TeV_PromptReco_Collisions16_JSON.txt' # 2.1/fb
# json = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/Cert_271036-276811_13TeV_PromptReco_Collisions16_JSON.txt' # 12.9/fb
json = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/Cert_271036-277148_13TeV_PromptReco_Collisions16_JSON_NoL1T.txt' # 15.9/fb

# ----- 2016B Prompt-Reco v1 ----- #
SingleElectron_Run2016B_PromptReco_v1 = kreator.makeDataComponent('SingleElectron_Run2016B_PromptReco_v1', '/SingleElectron/Run2016B-PromptReco-v1/MINIAOD', 'CMS', '.*root', json)
DoubleEG_Run2016B_PromptReco_v1       = kreator.makeDataComponent('DoubleEG_Run2016B_PromptReco_v1'      , '/DoubleEG/Run2016B-PromptReco-v1/MINIAOD'      , 'CMS', '.*root', json)
SingleMuon_Run2016B_PromptReco_v1     = kreator.makeDataComponent('SingleMuon_Run2016B_PromptReco_v1'    , '/SingleMuon/Run2016B-PromptReco-v1/MINIAOD'    , 'CMS', '.*root', json)
Tau_Run2016B_PromptReco_v1            = kreator.makeDataComponent('Tau_Run2016B_PromptReco_v1'           , '/Tau/Run2016B-PromptReco-v1/MINIAOD'           , 'CMS', '.*root', json)
DoubleMuon_Run2016B_PromptReco_v1     = kreator.makeDataComponent('DoubleMuon_Run2016B_PromptReco_v1'    , '/DoubleMuon/Run2016B-PromptReco-v1/MINIAOD'    , 'CMS', '.*root', json)
HLTPhysics_Run2016B_PromptReco_v1     = kreator.makeDataComponent('HLTPhysics_Run2016B_PromptReco_v1'    , '/HLTPhysics/Run2016B-PromptReco-v1/MINIAOD'    , 'CMS', '.*root', json)


# ----- 2016B Prompt-Reco v2 ----- #
SingleElectron_Run2016B_PromptReco_v2 = kreator.makeDataComponent('SingleElectron_Run2016B_PromptReco_v2', '/SingleElectron/Run2016B-PromptReco-v2/MINIAOD', 'CMS', '.*root', json)
DoubleEG_Run2016B_PromptReco_v2       = kreator.makeDataComponent('DoubleEG_Run2016B_PromptReco_v2'      , '/DoubleEG/Run2016B-PromptReco-v2/MINIAOD'      , 'CMS', '.*root', json)
SingleMuon_Run2016B_PromptReco_v2     = kreator.makeDataComponent('SingleMuon_Run2016B_PromptReco_v2'    , '/SingleMuon/Run2016B-PromptReco-v2/MINIAOD'    , 'CMS', '.*root', json) #, useAAA=True)
Tau_Run2016B_PromptReco_v2            = kreator.makeDataComponent('Tau_Run2016B_PromptReco_v2'           , '/Tau/Run2016B-PromptReco-v2/MINIAOD'           , 'CMS', '.*root', json)
MuonEG_Run2016B_PromptReco_v2         = kreator.makeDataComponent('MuonEG_Run2016B_PromptReco_v2'        , '/MuonEG/Run2016B-PromptReco-v2/MINIAOD'        , 'CMS', '.*root', json)
DoubleMuon_Run2016B_PromptReco_v2     = kreator.makeDataComponent('DoubleMuon_Run2016B_PromptReco_v2'    , '/DoubleMuon/Run2016B-PromptReco-v2/MINIAOD'    , 'CMS', '.*root', json)
HLTPhysics_Run2016B_PromptReco_v2     = kreator.makeDataComponent('HLTPhysics_Run2016B_PromptReco_v2'    , '/HLTPhysics/Run2016B-PromptReco-v2/MINIAOD'    , 'CMS', '.*root', json)


# ----- 2016C Prompt-Reco v2 ----- #
SingleElectron_Run2016C_PromptReco_v2 = kreator.makeDataComponent('SingleElectron_Run2016C_PromptReco_v2', '/SingleElectron/Run2016C-PromptReco-v2/MINIAOD', 'CMS', '.*root', json)
DoubleEG_Run2016C_PromptReco_v2       = kreator.makeDataComponent('DoubleEG_Run2016C_PromptReco_v2'      , '/DoubleEG/Run2016C-PromptReco-v2/MINIAOD'      , 'CMS', '.*root', json)
SingleMuon_Run2016C_PromptReco_v2     = kreator.makeDataComponent('SingleMuon_Run2016C_PromptReco_v2'    , '/SingleMuon/Run2016C-PromptReco-v2/MINIAOD'    , 'CMS', '.*root', json) #, useAAA=True)
Tau_Run2016C_PromptReco_v2            = kreator.makeDataComponent('Tau_Run2016C_PromptReco_v2'           , '/Tau/Run2016C-PromptReco-v2/MINIAOD'           , 'CMS', '.*root', json)
MuonEG_Run2016C_PromptReco_v2         = kreator.makeDataComponent('MuonEG_Run2016C_PromptReco_v2'        , '/MuonEG/Run2016C-PromptReco-v2/MINIAOD'        , 'CMS', '.*root', json)
DoubleMuon_Run2016C_PromptReco_v2     = kreator.makeDataComponent('DoubleMuon_Run2016C_PromptReco_v2'    , '/DoubleMuon/Run2016C-PromptReco-v2/MINIAOD'    , 'CMS', '.*root', json)
HLTPhysics_Run2016C_PromptReco_v2     = kreator.makeDataComponent('HLTPhysics_Run2016C_PromptReco_v2'    , '/HLTPhysics/Run2016C-PromptReco-v2/MINIAOD'    , 'CMS', '.*root', json)


# ----- 2016D Prompt-Reco v2 ----- #
SingleElectron_Run2016D_PromptReco_v2 = kreator.makeDataComponent('SingleElectron_Run2016D_PromptReco_v2', '/SingleElectron/Run2016D-PromptReco-v2/MINIAOD', 'CMS', '.*root', json)
DoubleEG_Run2016D_PromptReco_v2       = kreator.makeDataComponent('DoubleEG_Run2016D_PromptReco_v2'      , '/DoubleEG/Run2016D-PromptReco-v2/MINIAOD'      , 'CMS', '.*root', json)
SingleMuon_Run2016D_PromptReco_v2     = kreator.makeDataComponent('SingleMuon_Run2016D_PromptReco_v2'    , '/SingleMuon/Run2016D-PromptReco-v2/MINIAOD'    , 'CMS', '.*root', json) #, useAAA=True)
Tau_Run2016D_PromptReco_v2            = kreator.makeDataComponent('Tau_Run2016D_PromptReco_v2'           , '/Tau/Run2016D-PromptReco-v2/MINIAOD'           , 'CMS', '.*root', json)
MuonEG_Run2016D_PromptReco_v2         = kreator.makeDataComponent('MuonEG_Run2016D_PromptReco_v2'        , '/MuonEG/Run2016D-PromptReco-v2/MINIAOD'        , 'CMS', '.*root', json)
DoubleMuon_Run2016D_PromptReco_v2     = kreator.makeDataComponent('DoubleMuon_Run2016D_PromptReco_v2'    , '/DoubleMuon/Run2016D-PromptReco-v2/MINIAOD'    , 'CMS', '.*root', json)
HLTPhysics_Run2016D_PromptReco_v2     = kreator.makeDataComponent('HLTPhysics_Run2016D_PromptReco_v2'    , '/HLTPhysics/Run2016D-PromptReco-v2/MINIAOD'    , 'CMS', '.*root', json)


# ----- 2016E Prompt-Reco v2 ----- #
SingleElectron_Run2016E_PromptReco_v2 = kreator.makeDataComponent('SingleElectron_Run2016E_PromptReco_v2', '/SingleElectron/Run2016E-PromptReco-v2/MINIAOD', 'CMS', '.*root', json)
DoubleEG_Run2016E_PromptReco_v2       = kreator.makeDataComponent('DoubleEG_Run2016E_PromptReco_v2'      , '/DoubleEG/Run2016E-PromptReco-v2/MINIAOD'      , 'CMS', '.*root', json)
SingleMuon_Run2016E_PromptReco_v2     = kreator.makeDataComponent('SingleMuon_Run2016E_PromptReco_v2'    , '/SingleMuon/Run2016E-PromptReco-v2/MINIAOD'    , 'CMS', '.*root', json) #, useAAA=True)
Tau_Run2016E_PromptReco_v2            = kreator.makeDataComponent('Tau_Run2016E_PromptReco_v2'           , '/Tau/Run2016E-PromptReco-v2/MINIAOD'           , 'CMS', '.*root', json)
MuonEG_Run2016E_PromptReco_v2         = kreator.makeDataComponent('MuonEG_Run2016E_PromptReco_v2'        , '/MuonEG/Run2016E-PromptReco-v2/MINIAOD'        , 'CMS', '.*root', json)
DoubleMuon_Run2016E_PromptReco_v2     = kreator.makeDataComponent('DoubleMuon_Run2016E_PromptReco_v2'    , '/DoubleMuon/Run2016E-PromptReco-v2/MINIAOD'    , 'CMS', '.*root', json)
HLTPhysics_Run2016E_PromptReco_v2     = kreator.makeDataComponent('HLTPhysics_Run2016E_PromptReco_v2'    , '/HLTPhysics/Run2016E-PromptReco-v2/MINIAOD'    , 'CMS', '.*root', json)


# ----- 2016F Prompt-Reco v1 ----- #
SingleElectron_Run2016F_PromptReco_v1 = kreator.makeDataComponent('SingleElectron_Run2016F_PromptReco_v1', '/SingleElectron/Run2016F-PromptReco-v1/MINIAOD', 'CMS', '.*root', json)
DoubleEG_Run2016F_PromptReco_v1       = kreator.makeDataComponent('DoubleEG_Run2016F_PromptReco_v1'      , '/DoubleEG/Run2016F-PromptReco-v1/MINIAOD'      , 'CMS', '.*root', json)
SingleMuon_Run2016F_PromptReco_v1     = kreator.makeDataComponent('SingleMuon_Run2016F_PromptReco_v1'    , '/SingleMuon/Run2016F-PromptReco-v1/MINIAOD'    , 'CMS', '.*root', json) #, useAAA=True)
Tau_Run2016F_PromptReco_v1            = kreator.makeDataComponent('Tau_Run2016F_PromptReco_v1'           , '/Tau/Run2016F-PromptReco-v1/MINIAOD'           , 'CMS', '.*root', json)
MuonEG_Run2016F_PromptReco_v1         = kreator.makeDataComponent('MuonEG_Run2016F_PromptReco_v1'        , '/MuonEG/Run2016F-PromptReco-v1/MINIAOD'        , 'CMS', '.*root', json)
DoubleMuon_Run2016F_PromptReco_v1     = kreator.makeDataComponent('DoubleMuon_Run2016F_PromptReco_v1'    , '/DoubleMuon/Run2016F-PromptReco-v1/MINIAOD'    , 'CMS', '.*root', json)
HLTPhysics_Run2016F_PromptReco_v1     = kreator.makeDataComponent('HLTPhysics_Run2016F_PromptReco_v1'    , '/HLTPhysics/Run2016F-PromptReco-v1/MINIAOD'    , 'CMS', '.*root', json)


# ----- 2016G Prompt-Reco v1 ----- #
SingleElectron_Run2016G_PromptReco_v1 = kreator.makeDataComponent('SingleElectron_Run2016G_PromptReco_v1', '/SingleElectron/Run2016G-PromptReco-v1/MINIAOD', 'CMS', '.*root', json)
DoubleEG_Run2016G_PromptReco_v1       = kreator.makeDataComponent('DoubleEG_Run2016G_PromptReco_v1'      , '/DoubleEG/Run2016G-PromptReco-v1/MINIAOD'      , 'CMS', '.*root', json)
SingleMuon_Run2016G_PromptReco_v1     = kreator.makeDataComponent('SingleMuon_Run2016G_PromptReco_v1'    , '/SingleMuon/Run2016G-PromptReco-v1/MINIAOD'    , 'CMS', '.*root', json) #, useAAA=True)
Tau_Run2016G_PromptReco_v1            = kreator.makeDataComponent('Tau_Run2016G_PromptReco_v1'           , '/Tau/Run2016G-PromptReco-v1/MINIAOD'           , 'CMS', '.*root', json)
MuonEG_Run2016G_PromptReco_v1         = kreator.makeDataComponent('MuonEG_Run2016G_PromptReco_v1'        , '/MuonEG/Run2016G-PromptReco-v1/MINIAOD'        , 'CMS', '.*root', json)
DoubleMuon_Run2016G_PromptReco_v1     = kreator.makeDataComponent('DoubleMuon_Run2016G_PromptReco_v1'    , '/DoubleMuon/Run2016G-PromptReco-v1/MINIAOD'    , 'CMS', '.*root', json)
HLTPhysics_Run2016G_PromptReco_v1     = kreator.makeDataComponent('HLTPhysics_Run2016G_PromptReco_v1'    , '/HLTPhysics/Run2016G-PromptReco-v1/MINIAOD'    , 'CMS', '.*root', json)



data_single_muon     = [SingleMuon_Run2016B_PromptReco_v1    , SingleMuon_Run2016B_PromptReco_v2    , SingleMuon_Run2016C_PromptReco_v2    , SingleMuon_Run2016D_PromptReco_v2    , SingleMuon_Run2016E_PromptReco_v2    , SingleElectron_Run2016F_PromptReco_v1, SingleElectron_Run2016G_PromptReco_v1]
data_single_electron = [SingleElectron_Run2016B_PromptReco_v1, SingleElectron_Run2016B_PromptReco_v2, SingleElectron_Run2016C_PromptReco_v2, SingleElectron_Run2016D_PromptReco_v2, SingleElectron_Run2016E_PromptReco_v2, DoubleEG_Run2016F_PromptReco_v1      , DoubleEG_Run2016G_PromptReco_v1      ]
data_muon_electron   = [                                       MuonEG_Run2016B_PromptReco_v2        , MuonEG_Run2016C_PromptReco_v2        , MuonEG_Run2016D_PromptReco_v2        , MuonEG_Run2016E_PromptReco_v2        , SingleMuon_Run2016F_PromptReco_v1    , SingleMuon_Run2016G_PromptReco_v1    ]
data_tau             = [Tau_Run2016B_PromptReco_v1           , Tau_Run2016B_PromptReco_v2           , Tau_Run2016C_PromptReco_v2           , Tau_Run2016D_PromptReco_v2           , Tau_Run2016E_PromptReco_v2           , Tau_Run2016F_PromptReco_v1           , Tau_Run2016G_PromptReco_v1           ]
data_double_muon     = [DoubleMuon_Run2016B_PromptReco_v1    , DoubleMuon_Run2016B_PromptReco_v2    , DoubleMuon_Run2016C_PromptReco_v2    , DoubleMuon_Run2016D_PromptReco_v2    , DoubleMuon_Run2016E_PromptReco_v2    , MuonEG_Run2016F_PromptReco_v1        , MuonEG_Run2016G_PromptReco_v1        ]
data_double_eg       = [DoubleEG_Run2016B_PromptReco_v1      , DoubleEG_Run2016B_PromptReco_v2      , DoubleEG_Run2016C_PromptReco_v2      , DoubleEG_Run2016D_PromptReco_v2      , DoubleEG_Run2016E_PromptReco_v2      , DoubleMuon_Run2016F_PromptReco_v1    , DoubleMuon_Run2016G_PromptReco_v1    ]
data_hltphysics      = [HLTPhysics_Run2016B_PromptReco_v1    , HLTPhysics_Run2016B_PromptReco_v2    , HLTPhysics_Run2016C_PromptReco_v2    , HLTPhysics_Run2016D_PromptReco_v2    , HLTPhysics_Run2016E_PromptReco_v2    , HLTPhysics_Run2016F_PromptReco_v1    , HLTPhysics_Run2016G_PromptReco_v1    ]

all_data = data_single_muon + data_single_electron + data_muon_electron + data_tau + data_double_muon + data_double_eg + data_hltphysics

for comp in all_data:
    comp.splitFactor = 1000
    comp.isMC = False
    comp.isData = True

