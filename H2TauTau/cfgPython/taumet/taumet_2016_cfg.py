import os

import PhysicsTools.HeppyCore.framework.config as cfg

from PhysicsTools.HeppyCore.framework.config import printComps
from PhysicsTools.HeppyCore.framework.heppy_loop import getHeppyOption
from PhysicsTools.Heppy.utils.cmsswPreprocessor import CmsswPreprocessor

# Heppy analyzers
# from PhysicsTools.Heppy.analyzers.core.JSONAnalyzer import JSONAnalyzer
# from PhysicsTools.Heppy.analyzers.core.SkimAnalyzerCount import SkimAnalyzerCount
# from PhysicsTools.Heppy.analyzers.core.EventSelector import EventSelector
# from PhysicsTools.Heppy.analyzers.objects.VertexAnalyzer import VertexAnalyzer
# from PhysicsTools.Heppy.analyzers.core.PileUpAnalyzer import PileUpAnalyzer
# from PhysicsTools.Heppy.analyzers.gen.GeneratorAnalyzer import GeneratorAnalyzer
# from PhysicsTools.Heppy.analyzers.gen.LHEWeightAnalyzer import LHEWeightAnalyzer

# mu-met analyzers
from CMGTools.H2TauTau.proto.analyzers.TauMETAnalyzer import TauMETAnalyzer
from CMGTools.H2TauTau.proto.analyzers.LeptonWeighter import LeptonWeighter
from CMGTools.H2TauTau.proto.analyzers.METFilter import METFilter
from CMGTools.H2TauTau.proto.analyzers.W2TauMETTreeProducer import W2TauMETTreeProducer
from CMGTools.H2TauTau.proto.analyzers.W2LepMETGenAnalyzer import W2LepMETGenAnalyzer

from CMGTools.RootTools.utils.splitFactor import splitFactor
from CMGTools.H2TauTau.proto.samples.spring16.htt_common import WJetsToLNu

# common configuration and sequence
from CMGTools.H2TauTau.htt_ntuple_base_cff import puFileData, puFileMC, pileUpAna, skimAna, vbfAna, mcWeighter, vertexAna, eventSelector, jsonAna, jetAna, triggerAna, recoilCorr, lheWeightAna


# Get all heppy options; set via "-o production" or "-o production=True"

# production = True run on batch, production = False (or unset) run locally
production = getHeppyOption('production', False)
pick_events = getHeppyOption('pick_events', False)
data = getHeppyOption('data', False)
reapplyJEC = getHeppyOption('reapplyJEC', True)
correct_recoil = getHeppyOption('correct_recoil', True)

# Just to be sure
if production:
    pick_events = False

if reapplyJEC:
    jetAna.recalibrateJets = True

if correct_recoil:
    recoilCorr.apply = True

triggerAna.requireTrigger=False

# genAna = GeneratorAnalyzer.defaultConfig
genAna = cfg.Analyzer(
    W2LepMETGenAnalyzer,
    name='W2LepMETGenAnalyzer',
    jetCol='slimmedJets',
    channel='',
    genPtCut=8.
)

muMETAna = cfg.Analyzer(
    TauMETAnalyzer,
    name='TauMETAnalyzer',
    ptlep=23,
    etalep=2.4,
    isocut=0.15,
#     ignoreTriggerMatch=True, # best dilepton doesn't need trigger match
    verbose=False
)

treeProdAna = cfg.Analyzer(
    W2TauMETTreeProducer,
    name='W2TauMETTreeProducer',
)


###################################################
###                  SEQUENCE                   ###
###################################################
sequence = cfg.Sequence([
    lheWeightAna,
    jsonAna,
    skimAna,
    #mcWeighter,
    triggerAna, # First analyser that applies selections
    vertexAna,
    muMETAna,
    genAna,
    jetAna,
    #vbfAna,
    #recoilCorr,
    pileUpAna,
    treeProdAna,
])

selectedComponents = [WJetsToLNu]

# Batch or local
if not production:
    cache = True
    comp = WJetsToLNu
    comp.triggers = ['HLT_LooseIsoPFTau50_Trk30_eta2p1_MET90_v%d' %i for i in range(1,8)] + \
                    ['HLT_LooseIsoPFTau50_Trk30_eta2p1_v%d' %i for i in range(1,8)] + \
                    ['HLT_IsoMu22_v%d' %i for i in range(1,8)] + \
                    ['HLT_VLooseIsoPFTau140_Trk50_eta2p1_v%d' %i for i in range(1,8)] + \
                    ['HLT_Ele32_eta2p1_WPTight_Gsf_v%d' %i for i in range(1,8)]
    comp.splitFactor = 1
    comp.fineSplitFactor = 1
    selectedComponents = [comp]
    comp.files = comp.files[:1]

# the following is declared in case this cfg is used in input to the
# heppy.py script
from PhysicsTools.HeppyCore.framework.eventsfwlite import Events
config = cfg.Config(components=selectedComponents,
                    sequence=sequence,
                    services=[],
                    preprocessor=None,
                    events_class=Events
                    )

printComps(config.components, True)






