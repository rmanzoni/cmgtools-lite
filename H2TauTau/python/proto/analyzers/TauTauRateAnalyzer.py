import ROOT

from itertools import combinations
from copy      import deepcopy

from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
from PhysicsTools.HeppyCore.utils.deltar import deltaR
from PhysicsTools.Heppy.physicsobjects.Tau import Tau
from PhysicsTools.Heppy.physicsobjects.PhysicsObject import PhysicsObject

class TauTauRateAnalyzer(Analyzer):

    def declareHandles(self):
        super(TauTauRateAnalyzer, self).declareHandles()
        self.handles['taus'] = AutoHandle('slimmedTaus', 'std::vector<pat::Tau>')

    def process(self, event):
        super(TauTauRateAnalyzer, self).process(event)
        # Take the pre-sorted vertices from miniAOD
        event.goodVertices = event.vertices

        alltaus = []

        for discr in self.cfg_ana.discriminators:
            taus = getattr(event, discr)
            
            for ii in taus:
                tt = PhysicsObject(ii.tau)
                alreadyIn = False
                for jj in alltaus:
                    if deltaR(tt, jj) < 0.05:
                        alreadyIn = True
                        setattr(jj, discr, ii.discriminator)
                if not alreadyIn:
                    setattr(tt, discr, ii.discriminator)
                    alltaus.append(tt)

        alltaus.sort(key=lambda x: x.pt(), reverse=True)
                
        recotaus = self.handles['taus'].product()
        
        for tt in alltaus:
            dRmax = 0.5
            for rt in recotaus:        
                dR = deltaR(tt, rt)
                if dR < dRmax:
                     tt.recotau = rt
                     dRmax = dR      
        
        if hasattr(self.cfg_ana, 'ptcut'):
            alltaus = [tt for tt in alltaus if tt.pt()>self.cfg_ana.ptcut]
        
        event.trigger_taus = alltaus

        return True
