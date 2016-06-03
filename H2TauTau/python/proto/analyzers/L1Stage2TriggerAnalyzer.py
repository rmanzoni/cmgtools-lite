from itertools import product

from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
from PhysicsTools.HeppyCore.utils.deltar import deltaR

import PhysicsTools.HeppyCore.framework.config as cfg

class Stage2L1ObjEnum:
    EGamma, EtSum, Jet, Tau, Muon = [0, 3, 5, 7, 9] # nor range(5) to keep some compatibility with stage-1 


class L1Stage2TriggerAnalyzer(Analyzer):

    def __init__(self, *args, **kwargs):
        super(L1Stage2TriggerAnalyzer, self).__init__(*args, **kwargs)
            
    def beginLoop(self, setup):
        super(L1Stage2TriggerAnalyzer, self).beginLoop(setup)
        self.counters.addCounter('L1Stage2TriggerAnalyzer')
        count = self.counters.counter('L1Stage2TriggerAnalyzer')
        count.register('all events')
        count.register('leg 1 match')
        count.register('leg 2 match')

    def declareHandles(self):
        super(L1Stage2TriggerAnalyzer, self).declareHandles()
        
        if hasattr(self.cfg_ana, 'label'):
            labelcalo = self.cfg_ana.labelcalo
            labelmuon = self.cfg_ana.labelmuon
        else:
            labelcalo = 'caloStage2Digis'
            labelmuon = 'gmtStage2Digis'

        self.l1PtCut = self.cfg_ana.l1PtCut if hasattr(self.cfg_ana, 'l1PtCut') else 0.
            
        self.handles[Stage2L1ObjEnum.EGamma] = AutoHandle( (labelcalo, 'EGamma'), 'BXVector<l1t::EGamma>')
        self.handles[Stage2L1ObjEnum.EtSum ] = AutoHandle( (labelcalo, 'EtSum' ), 'BXVector<l1t::EtSum>' )
        self.handles[Stage2L1ObjEnum.Jet   ] = AutoHandle( (labelcalo, 'Jet'   ), 'BXVector<l1t::Jet>'   )
        self.handles[Stage2L1ObjEnum.Muon  ] = AutoHandle( (labelmuon, 'Muon'  ), 'BXVector<l1t::Muon>'  )
        self.handles[Stage2L1ObjEnum.Tau   ] = AutoHandle( (labelcalo, 'Tau'   ), 'BXVector<l1t::Tau>'   )
        
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
            
        legs = {event.diLepton.leg1():dRmax,
                event.diLepton.leg2():dRmax}    
        
        mytaus = []
                    
        for coll in collections:
            mycoll = self.handles[coll].product()
            
            n_l1obj = mycoll.size(bx)
            
            # for now only selects L1 objects from a BX
            # can be generalised
            for leg, l1 in product(legs.keys(), [mycoll.at(bx, i) for i in range(n_l1obj)]):
                if l1.pt() < self.l1PtCut:
                    continue
                dR = deltaR(l1.eta(), l1.phi(), leg.eta(), leg.phi())
                if dR < legs[leg]:
                    leg.L1 = l1
                    leg.L1flavour = coll
                    legs[leg] = dR  

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
#         collections=[Stage2L1ObjEnum.Muon, Stage2L1ObjEnum.Tau],
        collections=[Stage2L1ObjEnum.Tau],
        requireMatches=[],
        bx=0,
        l1PtCut=0.,
        dR=0.5
    )
)
