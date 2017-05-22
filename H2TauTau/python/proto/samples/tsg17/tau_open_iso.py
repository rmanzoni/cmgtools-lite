import PhysicsTools.HeppyCore.framework.config as cfg

#####COMPONENT CREATOR

from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
kreator = ComponentCreator()


HiggsGGH125   = kreator.makeMyPrivateMCComponent('HiggsGGH125' , '/GluGluHToTauTau_M125_13TeV_powheg_pythia8/manzoni-singleTau2017OpenIsoV3-29f7dae36643210eaec6ab4912c78586/USER'         , 'PRIVATE', '.*root', dbsInstance='phys03', xSec=1.)
HiggsVBF125   = kreator.makeMyPrivateMCComponent('HiggsVBF125' , '/VBFHToTauTau_M125_13TeV_powheg_pythia8/manzoni-singleTau2017OpenIsoV3-e8016cea1cfae7b182185cd8c19ea5b7/USER'            , 'PRIVATE', '.*root', dbsInstance='phys03', xSec=1.)
       
QCDPt15to30   = kreator.makeMyPrivateMCComponent('QCDPt15to30'  , '/QCD_Pt_15to30_TuneCUETP8M1_13TeV_pythia8/manzoni-singleTau2017OpenIsoV3-d9e74d4da5b5cdef519d19ed8968610c/USER'         , 'PRIVATE', '.*root', dbsInstance='phys03', xSec=1.587E+09)
QCDPt30to50   = kreator.makeMyPrivateMCComponent('QCDPt30to50'  , '/QCD_Pt_30to50_TuneCUETP8M1_13TeV_pythia8/manzoni-singleTau2017OpenIsoV3-d9e74d4da5b5cdef519d19ed8968610c/USER'         , 'PRIVATE', '.*root', dbsInstance='phys03', xSec=1.448E+08)
QCDPt50to80   = kreator.makeMyPrivateMCComponent('QCDPt50to80'  , '/QCD_Pt_50to80_TuneCUETP8M1_13TeV_pythia8/manzoni-singleTau2017OpenIsoV3-d9e74d4da5b5cdef519d19ed8968610c/USER'         , 'PRIVATE', '.*root', dbsInstance='phys03', xSec=1.993E+07)
QCDPt80to120  = kreator.makeMyPrivateMCComponent('QCDPt80to120' , '/QCD_Pt_80to120_TuneCUETP8M1_13TeV_pythia8/manzoni-singleTau2017OpenIsoV3-d9e74d4da5b5cdef519d19ed8968610c/USER'        , 'PRIVATE', '.*root', dbsInstance='phys03', xSec=2.66E+06 )
QCDPt120to170 = kreator.makeMyPrivateMCComponent('QCDPt120to170', '/QCD_Pt_120to170_TuneCUETP8M1_13TeV_pythia8/manzoni-singleTau2017OpenIsoV3-d9e74d4da5b5cdef519d19ed8968610c/USER'       , 'PRIVATE', '.*root', dbsInstance='phys03', xSec=4.921E+05)
QCDPt170to300 = kreator.makeMyPrivateMCComponent('QCDPt170to300', '/QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8/manzoni-singleTau2017OpenIsoV3-d9e74d4da5b5cdef519d19ed8968610c/USER'       , 'PRIVATE', '.*root', dbsInstance='phys03', xSec=1.198E+05)
QCDPt300to470 = kreator.makeMyPrivateMCComponent('QCDPt300to470', '/QCD_Pt_300to470_TuneCUETP8M1_13TeV_pythia8/manzoni-singleTau2017OpenIsoV3-d9e74d4da5b5cdef519d19ed8968610c/USER'       , 'PRIVATE', '.*root', dbsInstance='phys03', xSec=7.841E+03)
QCDPt470to600 = kreator.makeMyPrivateMCComponent('QCDPt470to600', '/QCD_Pt_470to600_TuneCUETP8M1_13TeV_pythia8/manzoni-singleTau2017OpenIsoV3-d9e74d4da5b5cdef519d19ed8968610c/USER'       , 'PRIVATE', '.*root', dbsInstance='phys03', xSec=6.483E+02)
       
DYJetsToLL_M1 = kreator.makeMyPrivateMCComponent('DYJetsToLL_M1', '/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/manzoni-singleTau2017OpenIsoV3-d9e74d4da5b5cdef519d19ed8968610c/USER'            , 'PRIVATE', '.*root', dbsInstance='phys03', xSec=1.90E+04 )
TTJets        = kreator.makeMyPrivateMCComponent('TTJets'       , '/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/manzoni-singleTau2017OpenIsoV3-d9e74d4da5b5cdef519d19ed8968610c/USER'           , 'PRIVATE', '.*root', dbsInstance='phys03', xSec=7.30E+02 )
WJetsToLNu    = kreator.makeMyPrivateMCComponent('WJetsToLNu'   , '/WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/manzoni-singleTau2017OpenIsoV3-d9e74d4da5b5cdef519d19ed8968610c/USER', 'PRIVATE', '.*root', dbsInstance='phys03', xSec=1.318E+05)

all_signal = [
    HiggsGGH125,
    HiggsVBF125,
]

all_qcd    = [
    QCDPt15to30  ,
    QCDPt30to50  ,
    QCDPt50to80  ,
    QCDPt80to120 ,
    QCDPt120to170,
    QCDPt170to300,
    QCDPt300to470,
    QCDPt470to600,
]

all_sm     = [
    DYJetsToLL_M1,
    TTJets       ,
    WJetsToLNu   ,  
]


all_mc = all_signal + all_qcd + all_sm

for comp in all_mc:
    comp.splitFactor = 1000000
    comp.isMC = True
    comp.isData = False
