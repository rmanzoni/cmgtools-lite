import ROOT
from itertools import product
from collections import namedtuple


from PhysicsTools.Heppy.analyzers.core.Analyzer       import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle     import AutoHandle
from PhysicsTools.HeppyCore.utils.deltar              import deltaR
from PhysicsTools.Heppy.physicsobjects.PhysicsObjects import Tau

class TauDiscriminatorAnalyzer(Analyzer):

    def declareHandles(self):
        super(TauDiscriminatorAnalyzer, self).declareHandles()

        for k, v in self.cfg_ana.inputs.iteritems():
            self.handles[k] = AutoHandle(v, 'reco::PFTauDiscriminator')        
            self.handles[k].discriminator = True

#         self.handles['l1taus'] = AutoHandle('Tau', 'BXVector<l1t::Tau>')
            
#         self.handles['hlt_trk_taus'] = AutoHandle('hltSelectedPFTausTrackPt0Reg', 'vector<reco::PFTau>')        
#         self.handles['hlt_trk_taus'] = AutoHandle('hltSelectedPFTausTrackPt1Reg', 'vector<reco::PFTau>')        

    def process(self, event):

        self.readCollections(event.input)
        
        if not(hasattr(self.cfg_ana, 'saveCollection') and self.cfg_ana.saveCollection):
            taus = [tt for tt in [event.diLepton.leg1(), event.diLepton.leg2()] if isinstance(tt, Tau)]
        
        
#         l1taus = self.handles['l1taus'].product()
                
        for k, v in self.handles.iteritems():
            
#             if k == 'l1taus':
#                 continue
                      
#             if not(hasattr(v, 'discriminator') and getattr(v, 'discriminator')):
#                 continue
            
            # why reading a fucking map is so difficult?
            coll = v.product()
            ntaus = coll.size()

            TauDiscriminator = namedtuple('TauDiscriminator', 'tau discriminator')
            
            discriminators = []
            for i in range(ntaus):
                mydisc = TauDiscriminator(
                    tau           = coll.keyProduct().product().at(i),
                    discriminator = coll.value(i),
                )
                discriminators.append(mydisc)
        
            dRmax = 0.3
            
            if hasattr(self.cfg_ana, 'saveCollection') and self.cfg_ana.saveCollection:
                setattr(event, k, discriminators)
            
            else:
                #for tau, map in product(taus, discriminators):
                for tau in taus:
                    tau.dRhlt = 0.3
                    for map in discriminators:
                        dR = deltaR(tau.eta(), tau.phi(), map.tau.eta(), map.tau.phi())
                        if dR < tau.dRhlt:
                            setattr(tau, k, map.discriminator)
                            setattr(tau, 'hlt_tau', map.tau)
                            tau.dRhlt = dR

#             if k == 'trigger_charged5hits':
#                 import pdb ; pdb.set_trace()

#         hlt_trk_taus = self.handles['hlt_trk_taus'].product()        
        
#         for tau in taus:
#             dRmax = 0.3    
#             for hlt_tau in hlt_trk_taus:
#                 dR = deltaR(tau.eta(), tau.phi(), hlt_tau.eta(), hlt_tau.phi())
#                 if dR < dRmax:
#                    setattr(tau, 'hlt_trk_tau', hlt_tau)
#                    dRmax = dR
        
#         for tau in taus:        
            #if hasattr(tau, 'hlt_trk_tau') and tau.hlt_trk_tau.leadPFChargedHadrCand().pt()<1.: 
#             if tau.hlt_trk_tau.leadPFChargedHadrCand().pt()<10.: 
#                 import pdb ; pdb.set_trace()
        
        
        return True
