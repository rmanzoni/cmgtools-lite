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
            self.handles[k] = AutoHandle(
                v, 
                'reco::PFTauDiscriminator',
                mayFail            = True,
                disableAtFirstFail = False,
                lazy               = False
            )        

    def process(self, event):

        self.readCollections(event.input)
        
        taus = self.cfg_ana.tomatch(event)
        
        for k, v in self.handles.iteritems():
                
            if not v.isValid():
                continue
            
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
                for tau in taus:
                    tau.dRhlt = 0.3
                    for map in discriminators:
                        dR = deltaR(tau.eta(), tau.phi(), map.tau.eta(), map.tau.phi())
                        if dR < tau.dRhlt:
                            setattr(tau, k, map.discriminator)
                            setattr(tau, 'hlt_tau', map.tau)
                            tau.dRhlt = dR        
            
            if hasattr(self.cfg_ana, 'ptcut'):
                discriminators = [dd for dd in discriminators if dd.tau.pt() > self.cfg_ana.ptcut]
            if hasattr(self.cfg_ana, 'maxTriggerTaus'):
                discriminators = discriminators[:min(self.cfg_ana.maxTriggerTaus, len(discriminators))]
            
            # append the tau discriminator collection to the event
            setattr(event, k, discriminators)
            
        return True
