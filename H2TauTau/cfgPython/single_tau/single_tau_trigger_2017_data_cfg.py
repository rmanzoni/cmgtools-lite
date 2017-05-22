import PhysicsTools.HeppyCore.framework.config as cfg
from PhysicsTools.HeppyCore.framework.heppy_loop import getHeppyOption
from PhysicsTools.Heppy.utils.cmsswPreprocessor  import CmsswPreprocessor
from PhysicsTools.HeppyCore.framework.config     import printComps

from PhysicsTools.Heppy.analyzers.objects.TauAnalyzer          import TauAnalyzer
from CMGTools.H2TauTau.proto.analyzers.TauAnalyzer             import TauAnalyzer

from CMGTools.H2TauTau.proto.analyzers.TriggerAnalyzer         import TriggerAnalyzer
from CMGTools.H2TauTau.proto.analyzers.TauTriggerTreeProducer  import TauTriggerTreeProducer
from CMGTools.H2TauTau.proto.analyzers.TauGenTreeProducer      import TauGenTreeProducer
from CMGTools.H2TauTau.proto.analyzers.LeptonWeighter          import LeptonWeighter
from CMGTools.H2TauTau.proto.analyzers.L1Stage2TriggerAnalyzer import L1Stage2TriggerAnalyzer, Stage2L1ObjEnum
from CMGTools.H2TauTau.proto.analyzers.TriggerObjectAnalyzer   import TriggerObjectAnalyzer
     
from CMGTools.RootTools.utils.splitFactor                      import splitFactor
# import samples
from CMGTools.RootTools.samples.samples_13TeV_DATA2016         import SingleMuon_Run2016B_23Sep2016, SingleMuon_Run2016C_23Sep2016, SingleMuon_Run2016D_23Sep2016, SingleMuon_Run2016E_23Sep2016, SingleMuon_Run2016F_23Sep2016, SingleMuon_Run2016G_23Sep2016, SingleMuon_Run2016H_PromptReco_v2, SingleMuon_Run2016H_PromptReco_v3

from CMGTools.H2TauTau.htt_ntuple_base_cff                     import skimAna, mcWeighter, jetAna, vbfAna, vertexAna, puFileData, puFileMC, eventSelector, jsonAna, triggerAna, pileUpAna, httGenAna, NJetsAna


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
    requireTrigger=True,
    usePrescaled=False,
    triggerResultsHandle=('TriggerResults', '', 'HLT'),
    triggerObjectsHandle=('selectedPatTrigger', '', 'RECO'),
)

# tauAna = TauAnalyzer.defaultConfig # from Heppy
tauAna = cfg.Analyzer(
    TauAnalyzer,
    name='TauAnalyzer',
    filtersToMatch=['hltPFTau140TrackPt50LooseAbsOrRelVLooseIso']
)

treeProducer = cfg.Analyzer(
    TauTriggerTreeProducer,
    name='TauTreeProducer',
    #triggerObjectsHandle = ('selectedPatTrigger', '', 'RECO'),
)

genTreeProducer = cfg.Analyzer(
    TauGenTreeProducer,
    name='TauGenTreeProducer'
)

samples = [SingleMuon_Run2016B_23Sep2016,
           SingleMuon_Run2016C_23Sep2016,
           SingleMuon_Run2016D_23Sep2016,
           SingleMuon_Run2016E_23Sep2016,
           SingleMuon_Run2016F_23Sep2016,
           SingleMuon_Run2016G_23Sep2016,
           SingleMuon_Run2016H_PromptReco_v2,
           SingleMuon_Run2016H_PromptReco_v3]

split_factor = 1e5

for sample in samples:
    sample.triggers  = ['HLT_IsoMu24_v%d' %i for i in range(1, 8)]
    sample.triggerobjects = [
        'hltL3crIsoL1sMu22L1f0L2f10QL3f24QL3trkIsoFiltered0p09',         # last filter of HLT_IsoMu24
    ]
    sample.splitFactor = splitFactor(sample, split_factor)
    sample.json = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/Final/Cert_271036-284044_13TeV_PromptReco_Collisions16_JSON.txt'

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
trigObjAna.triggerResultsHandle = ('TriggerResults', '', 'RECO')
trigObjAna.triggerObjectsHandle = ('selectedPatTrigger', '', 'RECO')
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
    comp                 = SingleMuon_Run2016H_PromptReco_v3
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
