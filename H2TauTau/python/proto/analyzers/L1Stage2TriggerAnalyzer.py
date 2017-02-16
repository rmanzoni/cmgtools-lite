import ROOT
from itertools import product

from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
from PhysicsTools.HeppyCore.utils.deltar import deltaR

from PhysicsTools.Heppy.physicsobjects.L1Candidate import L1Candidate
from PhysicsTools.Heppy.physicsobjects.Tau import Tau
from PhysicsTools.Heppy.physicsobjects.Muon import Muon
from PhysicsTools.Heppy.physicsobjects.Electron import Electron
from PhysicsTools.Heppy.physicsobjects.Jet import Jet

import PhysicsTools.HeppyCore.framework.config as cfg


class Stage2L1ObjEnum:
    EGamma, EtSum, Jet, Tau, Muon = [0, 3, 5, 7, 9] # nor range(5) to keep some compatibility with stage-1 


class L1Stage2TriggerAnalyzer(Analyzer):

    def __init__(self, *args, **kwargs):
        super(L1Stage2TriggerAnalyzer, self).__init__(*args, **kwargs)
        self.types = {
            Tau      : ROOT.l1t.Tau   ,
            Muon     : ROOT.l1t.Muon  ,
            Electron : ROOT.l1t.EGamma,
            Jet      : ROOT.l1t.Jet   ,
        }
            
    def beginLoop(self, setup):
        super(L1Stage2TriggerAnalyzer, self).beginLoop(setup)
        self.counters.addCounter('L1Stage2TriggerAnalyzer')
        count = self.counters.counter('L1Stage2TriggerAnalyzer')
        count.register('all events')
        count.register('leg 1 match')
        count.register('leg 2 match')

    def declareHandles(self):
        super(L1Stage2TriggerAnalyzer, self).declareHandles()
        
        if hasattr(self.cfg_ana, 'labelcalo'):
            labelcalo = self.cfg_ana.labelcalo
        else:
            labelcalo = 'caloStage2Digis'

        if hasattr(self.cfg_ana, 'labelmuon'):
            labelmuon = self.cfg_ana.labelmuon
        else:
            labelmuon = 'gmtStage2Digis'

        if hasattr(self.cfg_ana, 'process'):
            process = self.cfg_ana.process
        else:
            process = 'HLT'


        self.l1PtCut = self.cfg_ana.l1PtCut if hasattr(self.cfg_ana, 'l1PtCut') else 0.
                    
        self.handles[Stage2L1ObjEnum.EGamma] = AutoHandle( (labelcalo, 'EGamma', process), 'BXVector<l1t::EGamma>')
        self.handles[Stage2L1ObjEnum.EtSum ] = AutoHandle( (labelcalo, 'EtSum' , process), 'BXVector<l1t::EtSum>' )
        self.handles[Stage2L1ObjEnum.Jet   ] = AutoHandle( (labelcalo, 'Jet'   , process), 'BXVector<l1t::Jet>'   )
        self.handles[Stage2L1ObjEnum.Muon  ] = AutoHandle( (labelmuon, 'Muon'  , process), 'BXVector<l1t::Muon>'  )
        self.handles[Stage2L1ObjEnum.Tau   ] = AutoHandle( (labelcalo, 'Tau'   , process), 'BXVector<l1t::Tau>'   )
        
    def process(self, event):
        self.readCollections(event.input)
        
        if hasattr(self.cfg_ana, 'bx'):
            bx = self.cfg_ana.bx
        else:
            bx = 0
        
        collections = self.cfg_ana.collections
        
        dRmax = 0.5
        if hasattr(self.cfg_ana, 'dR'):
            dRmax = self.cfg_ana.dR
        
        legs = self.cfg_ana.getter(event)    
        
        for leg in legs:
            leg.L1matches = []
        
        mytaus = []
                    
        for coll in collections:
            mycoll = self.handles[coll].product()
                                        
            allL1objects = []
            #for ibx in [-2,-1,0,1,2]: # seg violation, fuck you L1
            for ibx in [0]: # FIXME: temporary fix, understand what's going on
                #import pdb ; pdb.set_trace()           
                for i in range(mycoll.size(ibx)):
                    l1 = mycoll.at(ibx, i)
                    l1.bx    = ibx                
                    l1.index = i                
                    allL1objects.append(l1)
                        
            for leg, l1 in product(legs, allL1objects):
                
                if l1.pt() < self.l1PtCut:
                    continue
                
                dR = deltaR(l1, leg)
                
                myL1 = L1Candidate(l1)

                myL1.type   = coll 
                myL1.bx     = l1.bx
                myL1.dR     = dR   
                myL1.goodID = isinstance(l1, self.types[type(leg)])
                                
                if dR < dRmax:
                    leg.L1matches.append(myL1)

        for leg in legs:
            leg.L1matches.sort(key = lambda l1 : (abs(l1.bx) == bx, l1.goodID, l1.pt(), l1.hwIso(), -l1.dR), reverse = True)

        
        if hasattr(self.cfg_ana, 'requireMatches'):
            self.counters.counter('L1Stage2TriggerAnalyzer').inc('all events')
            if 'leg1' in self.cfg_ana.requireMatches:
                if not hasattr(event.diLepton.leg1(), 'L1'):
                    return False
                else:
                    self.counters.counter('L1Stage2TriggerAnalyzer').inc('leg 1 match')
            if 'leg2' in self.cfg_ana.requireMatches:
                if not hasattr(event.diLepton.leg2(), 'L1'):
                    return False
                else:
                    self.counters.counter('L1Stage2TriggerAnalyzer').inc('leg 2 match')

        return True

setattr(L1Stage2TriggerAnalyzer, 'defaultConfig', 
    cfg.Analyzer(
        class_object=L1Stage2TriggerAnalyzer,
        collections=[Stage2L1ObjEnum.Muon, Stage2L1ObjEnum.Tau],
        getter = lambda event : [event.diLepton.leg1(), event.diLepton.leg2()],
#         collections=[Stage2L1ObjEnum.Tau],
        requireMatches=[],
        bx=0,
        l1PtCut=0.,
        l1PtForArbitration=28.,
        dR=0.5
    )
)
