import copy
import re 
from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator

creator = ComponentCreator()

# samples in 900 have HEP17 fucked up
DYJetsTT_RelValHEP17_900    = creator.makeMCComponent('DYJetsTT_RelValHEP17_900'   , '/RelValZTT_13/CMSSW_9_0_0-90X_upgrade2017_realistic_v20_HS-v1/MINIAODSIM'                 , 'CMS', '.*root', 1.0)
# QCD15tp3000_RelValHEP17_900 = creator.makeMCComponent('QCD15tp3000_RelValHEP17_900', '/RelValQCD_FlatPt_15_3000HS_13/CMSSW_9_0_0-90X_upgrade2017_realistic_v20_HS-v1/MINIAODSIM', 'CMS', '.*root', 1.0)

# samples in 902 are those to use
QCD15tp3000_RelValHEP17_902 = creator.makeMCComponent('QCD15tp3000_RelValHEP17_902', '/RelValQCD_FlatPt_15_3000HS_13/CMSSW_9_0_2-PU25ns_90X_upgrade2017_realistic_v20_HS_2017_resub-v1/MINIAODSIM', 'CMS', '.*root', 1.0, useAAA=True)
TTbar_RelValHEP17_902       = creator.makeMCComponent('TTbar_RelValHEP17_902'      , '/RelValTTbar_13/CMSSW_9_0_2-PU25ns_90X_upgrade2017_realistic_v20_HS_2017_resub-v1/MINIAODSIM'               , 'CMS', '.*root', 1.0, useAAA=True)
DYJetsMM_RelValHEP17_902    = creator.makeMCComponent('DYJetsMM_RelValHEP17_902'   , '/RelValZMM_13/CMSSW_9_0_2-PU25ns_90X_upgrade2017_realistic_v20_HS_2017-v1/MINIAODSIM'                       , 'CMS', '.*root', 1.0, useAAA=True)
DYJetsTT_RelValHEP17_902    = creator.makeMCComponent('DYJetsTT_RelValHEP17_902'   , '/RelValZTT_13/CMSSW_9_0_2-PU25ns_90X_upgrade2017_realistic_v20_HS_2017_resub-v1/MINIAODSIM'                 , 'CMS', '.*root', 1.0, useAAA=True)
