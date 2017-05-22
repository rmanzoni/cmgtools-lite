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

        self.maxtaus = 10
        self.bookEvent(self.tree)
#         self.var(self.tree, 'tag')
#         self.var(self.tree, 'probe')

        self.var(self.tree, 'ntaus')

        # RIC cannot make variable size vector work, revert to fixed size
        self.tree.vector('trig_taus_pt', self.maxtaus)
        self.tree.vector('trig_taus_eta', self.maxtaus)
        self.tree.vector('trig_taus_phi', self.maxtaus)
        self.tree.vector('trig_taus_mass', self.maxtaus)
        self.tree.vector('trig_taus_charge', self.maxtaus)
        
        self.tree.vector('trig_taus_leadtrack_pt', self.maxtaus)
        
        self.tree.vector('trig_taus_charged3hits'    , self.maxtaus)
        self.tree.vector('trig_taus_charged5hits'    , self.maxtaus)
        self.tree.vector('trig_taus_charged8hits'    , self.maxtaus)
        self.tree.vector('trig_taus_neutral'         , self.maxtaus)
        self.tree.vector('trig_taus_photons'         , self.maxtaus)

        self.tree.vector('trig_taus_charged3hits_reg', self.maxtaus)
        self.tree.vector('trig_taus_charged5hits_reg', self.maxtaus)
        self.tree.vector('trig_taus_charged8hits_reg', self.maxtaus)
        self.tree.vector('trig_taus_neutral_reg'     , self.maxtaus)
        self.tree.vector('trig_taus_photons_reg'     , self.maxtaus)

#         self.tree.vector('trig_taus_dbcorr0p2Cone0p8', 10)
#         self.tree.vector('trig_taus_rhocorrCone0p5', 10)

        self.tree.vector('trig_taus_L2_iso', self.maxtaus)
        self.tree.vector('trig_taus_L2_pt', self.maxtaus)
        self.tree.vector('trig_taus_L2_eta', self.maxtaus)
        self.tree.vector('trig_taus_L2_phi', self.maxtaus)
        self.tree.vector('trig_taus_L2_mass', self.maxtaus)

        self.tree.vector('trig_taus_L1_iso', self.maxtaus)
        self.tree.vector('trig_taus_L1_pt', self.maxtaus)
        self.tree.vector('trig_taus_L1_eta', self.maxtaus)
        self.tree.vector('trig_taus_L1_phi', self.maxtaus)
        self.tree.vector('trig_taus_L1_mass', self.maxtaus)

#         self.tree.vector('trig_lead_trk_finding', self.maxtaus)
#         self.tree.vector('trig_lead_trk_reg_pt1', self.maxtaus)

        self.tree.vector('trig_lead_trk_finding_match', self.maxtaus)
        self.tree.vector('trig_lead_trk_reg_pt1_match', self.maxtaus)


    def process(self, event):
        super(H2TauTauTreeProducerTauTauRate, self).process(event)

        taus = event.trigger_taus[:self.maxtaus]

        taus_pt = np.array([tt.pt() for tt in taus])
        taus_eta = np.array([tt.eta() for tt in taus])
        taus_phi = np.array([tt.phi() for tt in taus])
        taus_mass = np.array([tt.mass() for tt in taus])
        taus_charge = np.array([tt.charge() for tt in taus])
        
        # this requires you save all HLT PFCandidates... kinda heavy...
        lt_pts = []
        for tt in taus:
            try:
                lt_pts.append(tt.leadPFChargedHadrCand().pt())
            except:
                lt_pts.append(-99.)
        
        taus_leadtrack_pt = np.array(lt_pts)
                
        taus_charged3hits_reg = np.array([tt.trigger_charged3hits_reg if hasattr(tt, 'trigger_charged3hits_reg') else -99. for tt in taus])
        taus_charged5hits_reg = np.array([tt.trigger_charged5hits_reg if hasattr(tt, 'trigger_charged5hits_reg') else -99. for tt in taus])
        taus_charged8hits_reg = np.array([tt.trigger_charged8hits_reg if hasattr(tt, 'trigger_charged8hits_reg') else -99. for tt in taus])
        taus_neutral_reg      = np.array([tt.trigger_neutral_reg      if hasattr(tt, 'trigger_neutral_reg'     ) else -99. for tt in taus])
        taus_photons_reg      = np.array([tt.trigger_photons_reg      if hasattr(tt, 'trigger_photons_reg'     ) else -99. for tt in taus])

        taus_charged3hits     = np.array([tt.trigger_charged3hits     if hasattr(tt, 'trigger_charged3hits'    ) else -99. for tt in taus])
        taus_charged5hits     = np.array([tt.trigger_charged5hits     if hasattr(tt, 'trigger_charged5hits'    ) else -99. for tt in taus])
        taus_charged8hits     = np.array([tt.trigger_charged8hits     if hasattr(tt, 'trigger_charged8hits'    ) else -99. for tt in taus])
        taus_neutral          = np.array([tt.trigger_neutral          if hasattr(tt, 'trigger_neutral'         ) else -99. for tt in taus])
        taus_photons          = np.array([tt.trigger_photons          if hasattr(tt, 'trigger_photons'         ) else -99. for tt in taus])

#         taus_dbcorr0p2Cone0p8 = np.array([tt.trigger_dbcorr0p2Cone0p8 for tt in taus])
#         taus_rhocorrCone0p5 = np.array([tt.trigger_rhocorrCone0p5 for tt in taus])

        taus_L2_iso  = np.array([tt.L2.L2iso  if hasattr(tt, 'L2') else -99. for tt in taus])
        taus_L2_pt   = np.array([tt.L2.pt()   if hasattr(tt, 'L2') else -99. for tt in taus])
        taus_L2_eta  = np.array([tt.L2.eta()  if hasattr(tt, 'L2') else -99. for tt in taus])
        taus_L2_phi  = np.array([tt.L2.phi()  if hasattr(tt, 'L2') else -99. for tt in taus])
        taus_L2_mass = np.array([tt.L2.mass() if hasattr(tt, 'L2') else -99. for tt in taus])

#         if any([hasattr(tt, 'L1matches') and tt.L1matches for tt in taus]):
#             import pdb ; pdb.set_trace()

        taus_L1_iso  = np.array([tt.L1matches[0].hwIso() if hasattr(tt, 'L1matches') and tt.L1matches else -99. for tt in taus])
        taus_L1_pt   = np.array([tt.L1matches[0].pt()    if hasattr(tt, 'L1matches') and tt.L1matches else -99. for tt in taus])
        taus_L1_eta  = np.array([tt.L1matches[0].eta()   if hasattr(tt, 'L1matches') and tt.L1matches else -99. for tt in taus])
        taus_L1_phi  = np.array([tt.L1matches[0].phi()   if hasattr(tt, 'L1matches') and tt.L1matches else -99. for tt in taus])
        taus_L1_mass = np.array([tt.L1matches[0].mass()  if hasattr(tt, 'L1matches') and tt.L1matches else -99. for tt in taus])

#         taus_lead_trk_finding = np.array([tt.trigger_lead_trk_finding if hasattr(tt, 'trigger_lead_trk_finding') else -99. for tt in taus])
#         taus_lead_trk_reg_pt1 = np.array([tt.trigger_lead_trk_reg_pt1 if hasattr(tt, 'trigger_lead_trk_reg_pt1') else -99. for tt in taus])

        taus_lead_trk_finding_match = np.array([tt.hltPFTau20TrackPt1Reg if hasattr(tt, 'hltPFTau20TrackPt1Reg') else -99. for tt in taus])
        taus_lead_trk_reg_pt1_match = np.array([tt.hltPFTau20Track       if hasattr(tt, 'hltPFTau20Track'      ) else -99. for tt in taus])
                
        self.fillEvent(self.tree, event)
#         self.fill(self.tree, 'tag', event.tag)
#         self.fill(self.tree, 'probe', event.probe)
        self.fill(self.tree, 'ntaus', len(taus))
        
        self.tree.vfill('trig_taus_pt', taus_pt)
        self.tree.vfill('trig_taus_eta', taus_eta)
        self.tree.vfill('trig_taus_phi', taus_phi)
        self.tree.vfill('trig_taus_mass', taus_mass)
        self.tree.vfill('trig_taus_charge', taus_charge)
#         self.tree.vfill('trig_taus_leadtrack_pt', taus_leadtrack_pt)

#         self.tree.vfill('trig_taus_charged3hits'    , taus_charged3hits)
#         self.tree.vfill('trig_taus_charged5hits'    , taus_charged5hits)
#         self.tree.vfill('trig_taus_charged8hits'    , taus_charged8hits)
#         self.tree.vfill('trig_taus_neutral'         , taus_neutral     )
#         self.tree.vfill('trig_taus_photons'         , taus_photons     )

        self.tree.vfill('trig_taus_charged3hits_reg', taus_charged3hits_reg)
        self.tree.vfill('trig_taus_charged5hits_reg', taus_charged5hits_reg)
        self.tree.vfill('trig_taus_charged8hits_reg', taus_charged8hits_reg)
        self.tree.vfill('trig_taus_neutral_reg'     , taus_neutral_reg     )
        self.tree.vfill('trig_taus_photons_reg'     , taus_photons_reg     )
     
#         self.tree.vfill('trig_taus_dbcorr0p2Cone0p8', taus_dbcorr0p2Cone0p8)
#         self.tree.vfill('trig_taus_rhocorrCone0p5', taus_rhocorrCone0p5)

        self.tree.vfill('trig_taus_L2_iso', taus_L2_iso)
        self.tree.vfill('trig_taus_L2_pt', taus_L2_pt)
        self.tree.vfill('trig_taus_L2_eta', taus_L2_eta)
        self.tree.vfill('trig_taus_L2_phi', taus_L2_phi)
        self.tree.vfill('trig_taus_L2_mass', taus_L2_mass)

        self.tree.vfill('trig_taus_L1_iso', taus_L1_iso)
        self.tree.vfill('trig_taus_L1_pt', taus_L1_pt)
        self.tree.vfill('trig_taus_L1_eta', taus_L1_eta)
        self.tree.vfill('trig_taus_L1_phi', taus_L1_phi)
        self.tree.vfill('trig_taus_L1_mass', taus_L1_mass)

#         self.tree.vfill('trig_lead_trk_finding', taus_lead_trk_finding)
#         self.tree.vfill('trig_lead_trk_reg_pt1', taus_lead_trk_reg_pt1)

        self.tree.vfill('trig_lead_trk_finding_match', taus_lead_trk_finding_match)
        self.tree.vfill('trig_lead_trk_reg_pt1_match', taus_lead_trk_reg_pt1_match)

        self.fillTree(event)
