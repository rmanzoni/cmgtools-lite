import PhysicsTools.HeppyCore.framework.config as cfg
from PhysicsTools.HeppyCore.framework.heppy_loop import getHeppyOption
from PhysicsTools.Heppy.utils.cmsswPreprocessor  import CmsswPreprocessor
from PhysicsTools.HeppyCore.framework.config     import printComps

from PhysicsTools.Heppy.analyzers.objects.TauAnalyzer                import TauAnalyzer
from CMGTools.H2TauTau.proto.analyzers.TauAnalyzer                   import TauAnalyzer

from CMGTools.H2TauTau.proto.analyzers.TriggerAnalyzer               import TriggerAnalyzer
from CMGTools.H2TauTau.proto.analyzers.TauTriggerTreeProducer        import TauTriggerTreeProducer
from CMGTools.H2TauTau.proto.analyzers.TauGenTreeProducer            import TauGenTreeProducer
from CMGTools.H2TauTau.proto.analyzers.LeptonWeighter                import LeptonWeighter
from CMGTools.H2TauTau.proto.analyzers.L1Stage2TriggerAnalyzer       import L1Stage2TriggerAnalyzer, Stage2L1ObjEnum
from CMGTools.H2TauTau.proto.analyzers.TriggerObjectAnalyzer         import TriggerObjectAnalyzer
     
from CMGTools.RootTools.utils.splitFactor                            import splitFactor
from CMGTools.RootTools.samples.samples_13TeV_RunIISummer16MiniAODv2 import DYJetsToLL_M50_LO_ext, WJetsToLNu_LO, Zprimes, Wprimes, QCDHT, QCDPt

from CMGTools.H2TauTau.htt_ntuple_base_cff                           import skimAna, mcWeighter, jetAna, vbfAna, vertexAna, puFileData, puFileMC, eventSelector, jsonAna, triggerAna, pileUpAna, httGenAna, NJetsAna


# Get all heppy options; set via "-o production" or "-o production=True"
# production = True run on batch, production = False (or unset) run locally
production  = getHeppyOption('production')
production  = True
pick_events = False
data        = False
cmssw       = False


triggerAna = cfg.Analyzer(
    TriggerAnalyzer,
    name='TriggerAnalyzer',
    addTriggerObjects=True,
    requireTrigger=False,
    usePrescaled=False,
    triggerResultsHandle=('TriggerResults', '', 'HLT'),
    triggerObjectsHandle=('selectedPatTrigger', '', 'PAT'),
)

# tauAna = TauAnalyzer.defaultConfig # from Heppy
tauAna = cfg.Analyzer(
    TauAnalyzer,
    name='TauAnalyzer',
    filtersToMatch=['hltPFTau140TrackPt50LooseAbsOrRelVLooseIso', 'hltPFTau20TrackLooseIsoAgainstMuon']
)

treeProducer = cfg.Analyzer(
    TauTriggerTreeProducer,
    name='TauTreeProducer'
)

genTreeProducer = cfg.Analyzer(
    TauGenTreeProducer,
    name='TauGenTreeProducer'
)

samples = [DYJetsToLL_M50_LO_ext, WJetsToLNu_LO] + Zprimes + Wprimes + QCDHT + QCDPt

split_factor = 1e5

for sample in samples:
    sample.triggers  = ['HLT_VLooseIsoPFTau140_Trk50_eta2p1_v%d'                 %i for i in range(1, 8)]
    
    # extra trigger to check
#     sample.triggers += ['HLT_IsoMu22_v%d'                                          %i for i in range(1, 8)]
#     sample.triggers += ['HLT_IsoTkMu22_v%d'                                        %i for i in range(1, 8)]
#     sample.triggers += ['HLT_IsoMu24_v%d'                                          %i for i in range(1, 8)]
#     sample.triggers += ['HLT_IsoTkMu24_v%d'                                        %i for i in range(1, 8)]
#     sample.triggers += ['HLT_Mu50_v%d'                                             %i for i in range(1, 8)]
#     sample.triggers += ['HLT_TkMu50_v%d'                                           %i for i in range(1, 8)]
#     sample.triggers += ['HLT_IsoMu22_eta2p1_v%d'                                   %i for i in range(1, 8)]
#     sample.triggers += ['HLT_IsoTkMu22_eta2p1_v%d'                                 %i for i in range(1, 8)]
#     sample.triggers += ['HLT_IsoMu19_eta2p1_LooseIsoPFTau20_SingleL1_v%d'          %i for i in range(1, 8)]
#     sample.triggers += ['HLT_IsoMu21_eta2p1_LooseIsoPFTau20_SingleL1_v%d'          %i for i in range(1, 8)]
#     sample.triggers += ['HLT_Ele25_eta2p1_WPTight_Gsf_v%d'                         %i for i in range(1, 8)]
#     sample.triggers += ['HLT_Ele27_WPTight_Gsf_v%d'                                %i for i in range(1, 8)]
#     sample.triggers += ['HLT_Ele27_eta2p1_WPLoose_Gsf_v%d'                         %i for i in range(1, 8)]
#     sample.triggers += ['HLT_Ele45_WPLoose_Gsf_L1JetTauSeeded%d'                   %i for i in range(1, 8)]
#     sample.triggers += ['HLT_Ele115_CaloIdVT_GsfTrkIdT_v%d'                        %i for i in range(1, 8)]
#     sample.triggers += ['HLT_Ele24_eta2p1_WPLoose_Gsf_LooseIsoPFTau20_SingleL1_v%d'%i for i in range(1, 8)]
#     sample.triggers += ['HLT_Ele24_eta2p1_WPLoose_Gsf_LooseIsoPFTau20_v%d'         %i for i in range(1, 8)]
#     sample.triggers += ['HLT_Ele24_eta2p1_WPLoose_Gsf_LooseIsoPFTau30_v%d'         %i for i in range(1, 8)]
#     sample.triggers += ['HLT_DoubleMediumIsoPFTau35_Trk1_eta2p1_Reg_v%d'           %i for i in range(1, 8)]
#     sample.triggers += ['HLT_DoubleMediumCombinedIsoPFTau35_Trk1_eta2p1_Reg_v%d'   %i for i in range(1, 8)]

    sample.triggerobjects = []
    sample.splitFactor = splitFactor(sample, split_factor)
    sample.puFileData = puFileData
    sample.puFileMC = puFileMC

###################################################
###             SET COMPONENTS BY HAND          ###
###################################################
selectedComponents = samples

###################################################
###          AD HOC L1 TRIGGER ANALYZER         ###
###################################################
level1Ana = L1Stage2TriggerAnalyzer.defaultConfig
level1Ana.collections = [Stage2L1ObjEnum.Tau]
level1Ana.getter = lambda event : event.taus
level1Ana.process = 'RECO'

###################################################
###          TRIGGER OBJECT ANALYZER            ###
###################################################
trigObjAna = TriggerObjectAnalyzer.defaultConfig
trigObjAna.triggerResultsHandle = ('TriggerResults', '', 'HLT')
trigObjAna.triggerObjectsHandle = ('selectedPatTrigger', '', 'PAT')
trigObjAna.filters = ['hltPFTau140TrackPt50LooseAbsOrRelVLooseIso']

###################################################
###             CHERRY PICK EVENTS              ###
###################################################
if pick_events:
    eventSelector.toSelect = []
    sequence.insert(0, eventSelector)

###################################################
###                  SEQUENCE                   ###
###################################################
sequence = cfg.Sequence([
    jsonAna,
    #mcWeighter,
    skimAna,
    vertexAna,
    triggerAna,
    pileUpAna,
    jetAna,
    #vbfAna,
    tauAna,
    level1Ana,
    treeProducer,
])

###################################################
###            SET BATCH OR LOCAL               ###
###################################################
if not production:
    comp                 = Zprimes[4]
    selectedComponents   = [comp]
    comp.splitFactor     = 1
    comp.fineSplitFactor = 1
    comp.files           = comp.files[:1]

preprocessor = None
if cmssw:
    sequence.append(fileCleaner)
    preprocessor = CmsswPreprocessor("$CMSSW_BASE/src/CMGTools/H2TauTau/prod/h2TauTauMiniAOD_mutau_cfg.py", addOrigAsSecondary=False)

# the following is declared in case this cfg is used in input to the
# heppy.py script
from PhysicsTools.HeppyCore.framework.eventsfwlite import Events
config = cfg.Config(
    components   = selectedComponents,
    sequence     = sequence,
    services     = [],
    preprocessor = preprocessor,
    events_class = Events
)

printComps(config.components, True)

def modCfgForPlot(config):
    config.components = []
