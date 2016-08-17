import ROOT
from itertools import product

from PhysicsTools.Heppy.analyzers.core.Analyzer       import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle     import AutoHandle
from PhysicsTools.HeppyCore.utils.deltar              import deltaR
from PhysicsTools.Heppy.physicsobjects.PhysicsObjects import Tau

class TauDiscriminatorAnalyzer(Analyzer):

    def declareHandles(self):
        super(TauDiscriminatorAnalyzer, self).declareHandles()

        for k, v in self.cfg_ana.inputs.iteritems():
            self.handles[k] = AutoHandle(v, 'reco::PFTauDiscriminator')        

    def process(self, event):

        self.readCollections(event.input)
        
        taus = [tt for tt in [event.diLepton.leg1(), event.diLepton.leg2()] if isinstance(tt, Tau)]
                
        for k, v in self.handles.iteritems():
            print '================================'
            print k
            print '================================'
            
            coll = v.product()
        
            dRmax = 0.3
            
            for tau, map in product(taus, coll):
                dR = deltaR(tau.eta(), tau.phi(), map.first.eta(), map.first.phi())
                if dR < dRmax:
                    setattr(tau, k, map.second)
                    print '\n\n', tau
                    print 'trigger tau: ', map.first.pt(), map.first.eta(), map.first.phi()
                    print '==>', map.second

        return True
