import PhysicsTools.HeppyCore.framework.config as cfg
from PhysicsTools.HeppyCore.framework.heppy_loop import getHeppyOption
from PhysicsTools.Heppy.utils.cmsswPreprocessor  import CmsswPreprocessor
from PhysicsTools.HeppyCore.framework.config     import printComps

from PhysicsTools.Heppy.analyzers.objects.TauAnalyzer                import TauAnalyzer

from CMGTools.H2TauTau.proto.analyzers.TriggerAnalyzer               import TriggerAnalyzer
from CMGTools.H2TauTau.proto.analyzers.TauTriggerTreeProducer        import TauTriggerTreeProducer
from CMGTools.H2TauTau.proto.analyzers.TauGenTreeProducer            import TauGenTreeProducer
from CMGTools.H2TauTau.proto.analyzers.LeptonWeighter                import LeptonWeighter
from CMGTools.H2TauTau.proto.analyzers.L1Stage2TriggerAnalyzer       import L1Stage2TriggerAnalyzer, Stage2L1ObjEnum
from CMGTools.H2TauTau.proto.analyzers.TriggerObjectAnalyzer         import TriggerObjectAnalyzer
      
from CMGTools.RootTools.utils.splitFactor                            import splitFactor
from CMGTools.RootTools.samples.samples_13TeV_RunIISpring16MiniAODv2 import DYJetsToLL_M50_reHLT, DYJetsToLL_M50_LO_reHLT

from CMGTools.H2TauTau.htt_ntuple_base_cff                           import skimAna, vertexAna, puFileData, puFileMC, eventSelector, jsonAna, triggerAna, pileUpAna, httGenAna, NJetsAna


# Get all heppy options; set via "-o production" or "-o production=True"
# production = True run on batch, production = False (or unset) run locally
production  = getHeppyOption('production')
production  = False
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

tauAna = TauAnalyzer.defaultConfig

treeProducer = cfg.Analyzer(
    TauTriggerTreeProducer,
    name='TauTreeProducer'
)

genTreeProducer = cfg.Analyzer(
    TauGenTreeProducer,
    name='TauGenTreeProducer'
)

samples = [DYJetsToLL_M50_reHLT]

split_factor = 1e5

for sample in samples:
    sample.triggers = ['HLT_ZeroBias_v%d' %i for i in range(1, 8)] + ['MC_LooseIsoPFTau20_v%d'%i for i in range(1, 8)]
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
level1Ana.process = 'HLT'

###################################################
###          TRIGGER OBJECT ANALYZER            ###
###################################################
trigObjAna = TriggerObjectAnalyzer.defaultConfig
trigObjAna.triggerResultsHandle = ('TriggerResults', '', 'HLT')
trigObjAna.triggerObjectsHandle = ('selectedPatTrigger', '', 'RECO')
trigObjAna.filters = ['hltPFTau20TrackLooseIsoAgainstMuon']

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
    skimAna,
    vertexAna,
    triggerAna,
    #httGenAna,
    pileUpAna,
    tauAna,
    treeProducer
])

###################################################
###            SET BATCH OR LOCAL               ###
###################################################
if not production:
    comp                 = selectedComponents[0]
    selectedComponents   = [comp]
    comp.splitFactor     = 1
    comp.fineSplitFactor = 1
    comp.files           = [
        # 2016 geometry
        'root://eoscms.cern.ch//eos/cms/store/relval/CMSSW_8_1_0_pre16/RelValZTT_13/MINIAODSIM/PU25ns_81X_mcRun2_asymptotic_v11-v1/10000/764A2CB3-F8A6-E611-9FB7-0CC47A4C8F26.root',
        'root://eoscms.cern.ch//eos/cms/store/relval/CMSSW_8_1_0_pre16/RelValZTT_13/MINIAODSIM/PU25ns_81X_mcRun2_asymptotic_v11-v1/10000/DEC376B9-F8A6-E611-AC13-0025905B85BC.root',
        # 2017 geometry
#         'root://eoscms.cern.ch//eos/cms/store/relval/CMSSW_8_1_0_pre16/RelValZTT_13/MINIAODSIM/PU25ns_81X_upgrade2017_realistic_v22-v1/10000/7639F4F0-29AE-E611-AE92-0025905B8564.root',
#         'root://eoscms.cern.ch//eos/cms/store/relval/CMSSW_8_1_0_pre16/RelValZTT_13/MINIAODSIM/PU25ns_81X_upgrade2017_realistic_v22-v1/10000/C82D2DEF-29AE-E611-A2B5-0025905B85EC.root',
    ]

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
