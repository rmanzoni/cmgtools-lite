import numpy as np
from CMGTools.H2TauTau.proto.analyzers.H2TauTauTreeProducerBase import H2TauTauTreeProducerBase
from CMGTools.H2TauTau.proto.analyzers.TreeRateVariables import event_vars, physobj_vars, trigobj_vars


class H2TauTauTreeProducerTauTauRate(H2TauTauTreeProducerBase):

    '''Tree producer for di-tau trigger rate studies'''

    # event
    def bookEvent(self, tree):
        self.bookGeneric(tree, event_vars)

    def fillEvent(self, tree, event):
        self.fillGeneric(tree, event_vars, event)

    def declareVariables(self, setup):
        super(H2TauTauTreeProducerTauTauRate, self).declareVariables(setup)

        self.bookEvent(self.tree)
        self.var(self.tree, 'tag')
        self.var(self.tree, 'probe')

        self.var(self.tree, 'ntaus')

        # RIC cannot make variable size vector work, revert to fixed size
        self.tree.vector('trig_taus_pt', 10)
        self.tree.vector('trig_taus_eta', 10)
        self.tree.vector('trig_taus_phi', 10)
        self.tree.vector('trig_taus_mass', 10)
        self.tree.vector('trig_taus_charge', 10)
        self.tree.vector('trig_taus_leadtrack_pt', 10)
        self.tree.vector('trig_taus_charged3hits', 10)
        self.tree.vector('trig_taus_charged5hits', 10)
        self.tree.vector('trig_taus_charged8hits', 10)
        self.tree.vector('trig_taus_neutral', 10)
        self.tree.vector('trig_taus_dbcorr0p2Cone0p8', 10)
        self.tree.vector('trig_taus_rhocorrCone0p5', 10)
        self.tree.vector('trig_taus_photons', 10)

    def process(self, event):

        super(H2TauTauTreeProducerTauTauRate, self).process(event)

        taus = event.trigger_taus
                
        taus_pt = np.array([tt.pt() for tt in taus])
        taus_eta = np.array([tt.eta() for tt in taus])
        taus_phi = np.array([tt.phi() for tt in taus])
        taus_mass = np.array([tt.mass() for tt in taus])
        taus_charge = np.array([tt.charge() for tt in taus])
        
        lt_pts = []
        for tt in taus:
            try:
                lt_pts.append(tt.leadPFChargedHadrCand().pt())
            except:
                lt_pts.append(-99.)
        
        taus_leadtrack_pt = np.array(lt_pts)
        
        taus_charged3hits = np.array([tt.trigger_charged3hits for tt in taus])
        taus_charged5hits = np.array([tt.trigger_charged5hits for tt in taus])
        taus_charged8hits = np.array([tt.trigger_charged8hits for tt in taus])
        taus_neutral = np.array([tt.trigger_neutral for tt in taus])
        taus_dbcorr0p2Cone0p8 = np.array([tt.trigger_dbcorr0p2Cone0p8 for tt in taus])
        taus_rhocorrCone0p5 = np.array([tt.trigger_rhocorrCone0p5 for tt in taus])
        taus_photons = np.array([tt.trigger_photons for tt in taus])

        self.fillEvent(self.tree, event)
        self.fill(self.tree, 'tag', event.tag)
        self.fill(self.tree, 'probe', event.probe)
        self.fill(self.tree, 'ntaus', len(taus))
        
        self.tree.vfill('trig_taus_pt', taus_pt)
        self.tree.vfill('trig_taus_eta', taus_eta)
        self.tree.vfill('trig_taus_phi', taus_phi)
        self.tree.vfill('trig_taus_mass', taus_mass)
        self.tree.vfill('trig_taus_charge', taus_charge)
        self.tree.vfill('trig_taus_leadtrack_pt', taus_leadtrack_pt)

        self.tree.vfill('trig_taus_charged3hits', taus_charged3hits)
        self.tree.vfill('trig_taus_charged5hits', taus_charged5hits)
        self.tree.vfill('trig_taus_charged8hits', taus_charged8hits)
        self.tree.vfill('trig_taus_neutral', taus_neutral)
        self.tree.vfill('trig_taus_dbcorr0p2Cone0p8', taus_dbcorr0p2Cone0p8)
        self.tree.vfill('trig_taus_rhocorrCone0p5', taus_rhocorrCone0p5)
        self.tree.vfill('trig_taus_photons', taus_photons)

#         import pdb; pdb.set_trace()
        self.fillTree(event)
