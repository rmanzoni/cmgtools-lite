import PhysicsTools.HeppyCore.framework.config as cfg
from PhysicsTools.HeppyCore.framework.heppy_loop import getHeppyOption
from PhysicsTools.Heppy.utils.cmsswPreprocessor  import CmsswPreprocessor
from PhysicsTools.HeppyCore.framework.config     import printComps

from PhysicsTools.Heppy.analyzers.objects.TauAnalyzer                import TauAnalyzer
from CMGTools.H2TauTau.proto.analyzers.TauAnalyzer                   import TauAnalyzer

from CMGTools.H2TauTau.proto.analyzers.TriggerAnalyzer               import TriggerAnalyzer
from CMGTools.H2TauTau.proto.analyzers.TauTriggerTreeProducer        import TauTriggerTreeProducer
from CMGTools.H2TauTau.proto.analyzers.TauTrigger2017TreeProducer    import TauTrigger2017TreeProducer
from CMGTools.H2TauTau.proto.analyzers.TauGenTreeProducer            import TauGenTreeProducer
from CMGTools.H2TauTau.proto.analyzers.LeptonWeighter                import LeptonWeighter
from CMGTools.H2TauTau.proto.analyzers.L1Stage2TriggerAnalyzer       import L1Stage2TriggerAnalyzer, Stage2L1ObjEnum
from CMGTools.H2TauTau.proto.analyzers.TriggerObjectAnalyzer         import TriggerObjectAnalyzer
from CMGTools.H2TauTau.proto.analyzers.L2TriggerAnalyzer             import L2TriggerAnalyzer
from CMGTools.H2TauTau.proto.analyzers.TauDiscriminatorAnalyzer      import TauDiscriminatorAnalyzer

from CMGTools.RootTools.utils.splitFactor                            import splitFactor

from CMGTools.H2TauTau.proto.samples.tsg17.tau_open_iso              import HiggsGGH125, HiggsVBF125
from CMGTools.H2TauTau.htt_ntuple_base_cff                           import skimAna, mcWeighter, jetAna, vbfAna, vertexAna, puFileData, puFileMC, eventSelector, jsonAna, triggerAna, pileUpAna, httGenAna, NJetsAna


# Get all heppy options; set via "-o production" or "-o production=True"
# production = True run on batch, production = False (or unset) run locally
production  = getHeppyOption('production')
production  = True
pick_events = True
data        = False
cmssw       = False


triggerAna = cfg.Analyzer(
    TriggerAnalyzer,
    name='TriggerAnalyzer',
    addTriggerObjects=True,
    requireTrigger=False,
    usePrescaled=False,
    triggerResultsHandle=('TriggerResults', '', 'TEST'),
    triggerObjectsHandle=('selectedPatTriggerCustom', '', 'TEST'),
)

level2Ana = cfg.Analyzer(
    L2TriggerAnalyzer,
    name='L2TriggerAnalyzer',
    tomatch=lambda event : event.taus, 
    verbose=False,
)

tauAna = cfg.Analyzer(
    TauAnalyzer,
    name='TauAnalyzer',
    filtersToMatch=['hltPFTau20TrackPt1Reg'],
    triggerObjectsHandle=('selectedPatTriggerCustom', '', 'TEST'),
)

treeProducer = cfg.Analyzer(
    TauTrigger2017TreeProducer,
    name='TauTree2017Producer'
)

###################################################
###         TAU DISCRIMINATOR ANALYZER          ###
###################################################
tauDiscAna = cfg.Analyzer(
    TauDiscriminatorAnalyzer,
    tomatch = lambda event : event.taus,
    inputs = {
        'trigger_charged3hits'      : 'hltPFTauCharged3HitsPtSumReg'        ,
        'trigger_charged5hits'      : 'hltPFTauCharged5HitsPtSumReg'        ,
        'trigger_charged8hits'      : 'hltPFTauCharged8HitsPtSumReg'        ,
        'trigger_neutral'           : 'hltPFTauNeutralPtSumReg'             ,
        'trigger_photons'           : 'hltPFTauPhotonPtOutsideSignalConeReg',
    },
    ptcut=20.,
)

genTreeProducer = cfg.Analyzer(
    TauGenTreeProducer,
    name='TauGenTreeProducer'
)

# samples = [HiggsGGH125, HiggsVBF125]
samples = [HiggsVBF125]

split_factor = 1e5

for sample in samples:
    sample.triggers  = ['MC_OpenL2p5Iso_OpenL3Iso_PFTau20_Trk1_Reg_v%d' %i for i in range(1, 2)]
    sample.triggerobjects = []
#     sample.splitFactor = splitFactor(sample, split_factor)
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
level1Ana.process = 'TEST'
level1Ana.labelcalo = 'hltGtStage2Digis'
level1Ana.labelmuons = 'hltGtStage2Digis'

###################################################
###          TRIGGER OBJECT ANALYZER            ###
###################################################
trigObjAna = TriggerObjectAnalyzer.defaultConfig
trigObjAna.triggerResultsHandle = ('TriggerResults'          , '', 'TEST')
trigObjAna.triggerObjectsHandle = ('selectedPatTriggerCustom', '', 'TEST')
trigObjAna.filters = ['hltPFTau20TrackPt1Reg']

###################################################
###             CHERRY PICK EVENTS              ###
###################################################
if pick_events:
    eventSelector.toSelect = [719595]
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
    level2Ana,
    level1Ana,
    tauDiscAna,
    treeProducer,
])

###################################################
###            SET BATCH OR LOCAL               ###
###################################################
if not production:
    comp                 = HiggsVBFH125
    selectedComponents   = [comp]
    comp.splitFactor     = 1
    comp.fineSplitFactor = 1
#     comp.files           = ['file:/afs/cern.ch/work/m/manzoni/tauHLT/2017/CMSSW_9_1_0_pre3/src/HLTrigger/Configuration/test/open_iso/outputFULL.root']

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
