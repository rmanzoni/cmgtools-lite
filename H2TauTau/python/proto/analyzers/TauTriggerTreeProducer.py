import ROOT

from PhysicsTools.Heppy.physicsutils.TauDecayModes import tauDecayModes
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle

from CMGTools.H2TauTau.proto.analyzers.H2TauTauTreeProducerBase import H2TauTauTreeProducerBase
from CMGTools.H2TauTau.proto.analyzers.H2TauTauTreeProducerTauMu import H2TauTauTreeProducerTauMu

from CMGTools.H2TauTau.proto.analyzers.HTTGenAnalyzer import HTTGenAnalyzer

class TauTriggerTreeProducer(H2TauTauTreeProducerBase):
    ''' Tree producer for tau POG study.
    '''

    def __init__(self, *args):
        super(TauTriggerTreeProducer, self).__init__(*args)
        self.maxNTaus = 99

    def declareHandles(self):
        super(TauTriggerTreeProducer, self).declareHandles()
        if hasattr(self.cfg_ana, 'triggerObjectsHandle'):
            myhandle = self.cfg_ana.triggerObjectsHandle
            self.handles['triggerObjects'] = AutoHandle(
                (myhandle[0], myhandle[1], myhandle[2]),
                'std::vector<pat::TriggerObjectStandAlone>'
                )
        else:    
            self.handles['triggerObjects'] =  AutoHandle(
                'selectedPatTrigger',
                'std::vector<pat::TriggerObjectStandAlone>'
                )


    def declareVariables(self, setup):

        self.bookEvent(self.tree)
        self.bookTau(self.tree, 'tau', fill_extra=True)
        self.bookGenParticle(self.tree, 'tau_gen')
        self.bookGenParticle(self.tree, 'tau_gen_vis')
        self.bookL1object(self.tree, 'tau_L1')
        self.var(self.tree, 'tau_gen_decaymode', int)
        #self.var(self.tree, 'trigger_matched_looseisotau20')
        self.var(self.tree, 'trigger_matched_vlooseisotau140')
        self.var(self.tree, 'tau_gen_decayMode')
        self.bookTrackInfo('tau_lead_ch')

        self.var(self.tree, 'trigger_vlooseisotau140'   )
        self.var(self.tree, 'trigger_mctau20'           )

#         self.var(self.tree, 'trigger_isomu22'           )
#         self.var(self.tree, 'trigger_isotkmu22'         )
#         self.var(self.tree, 'trigger_isomu24  '         )
#         self.var(self.tree, 'trigger_isotkmu24'         )
#         self.var(self.tree, 'trigger_mu50'              )
#         self.var(self.tree, 'trigger_tkmu50'            )
#         self.var(self.tree, 'trigger_isomu22eta2p1'     )
#         self.var(self.tree, 'trigger_isotkmu22eta2p1'   )
#         self.var(self.tree, 'trigger_isomu19medisotau32')
#         self.var(self.tree, 'trigger_isomu21medisotau32')
#         self.var(self.tree, 'trigger_ele25tighteta2p1'  )
#         self.var(self.tree, 'trigger_ele27tight'        )
#         self.var(self.tree, 'trigger_ele27looseeta2p1'  )
#         self.var(self.tree, 'trigger_ele45loosetauseed' )
#         self.var(self.tree, 'trigger_ele115'            )
#         self.var(self.tree, 'trigger_ele24tau20singleL1')
#         self.var(self.tree, 'trigger_ele24tau20'        )
#         self.var(self.tree, 'trigger_ele24tau30'        )
#         self.var(self.tree, 'trigger_doubletau35'       )
#         self.var(self.tree, 'trigger_doubletau35comb'   )

        if hasattr(self.cfg_ana, 'addParticles'):
            for particle in self.cfg_ana.addParticles:
                self.bookParticle(self.tree, 'l2_%s' %particle)
        

    def bookTrackInfo(self, name):
        H2TauTauTreeProducerTauMu.bookTrackInfo(self, name)

    def fillTrackInfo(self, track, name='tau_track'):
        H2TauTauTreeProducerTauMu.fillTrackInfo(self, track, name)

    def process(self, event):
        super(TauTriggerTreeProducer, self).process(event)

        # needed when doing handle.product(), goes back to
        # PhysicsTools.Heppy.analyzers.core.Analyzer
        self.readCollections(event.input)

        if not eval(self.skimFunction):
            return False

        fired_triggers = [info.name for info in getattr(event, 'trigger_infos', []) if info.fired]


        # make sure you select an unbiassed sample:
        if event.input.eventAuxiliary().isRealData() and len(event.taus) == 1:
            triggerObjects = self.handles['triggerObjects'].product()
            # count how many objects have potentially fired IsoMu24
            firedisomu24 = len([to.hasFilterLabel('hltL3crIsoL1sMu22L1f0L2f10QL3f24QL3trkIsoFiltered0p09') for to in triggerObjects])
            # remove taus from the count
            for tau in event.taus:
                firedisomu24 -= any(to.hasFilterLabel('hltL3crIsoL1sMu22L1f0L2f10QL3f24QL3trkIsoFiltered0p09') for to in tau.tos)
            # if the only object that fired IsoMu24 is a tau and there's only a tau, then the event is biassed, return false
            if firedisomu24 == 0:
                print 'the only tau in the event fired IsoMu24... neglect this event'
                return False
        
        for i_tau, tau in enumerate(event.taus):
                
            if i_tau > self.maxNTaus: break
            
            self.tree.reset()
        
            self.fillEvent(self.tree, event)

            self.fillTau(self.tree, 'tau', tau, fill_extra=True)
            #self.fill(self.tree, 'trigger_matched_looseisotau20', any(to.hasFilterLabel('hltPFTau20TrackLooseIsoAgainstMuon') for to in tau.tos))
            self.fill(self.tree, 'trigger_matched_vlooseisotau140', any(to.hasFilterLabel('hltPFTau140TrackPt50LooseAbsOrRelVLooseIso') for to in tau.tos))

            self.fill(self.tree, 'trigger_vlooseisotau140'   , any('HLT_VLooseIsoPFTau140_Trk50_eta2p1_v'                    in name for name in fired_triggers))
            self.fill(self.tree, 'trigger_mctau20'           , any('MC_LooseIsoPFTau20_v'                                    in name for name in fired_triggers))

#             self.fill(self.tree, 'trigger_isomu22'           , any('HLT_IsoMu22_v'                                           in name for name in fired_triggers))
#             self.fill(self.tree, 'trigger_isotkmu22'         , any('HLT_IsoTkMu22_v'                                         in name for name in fired_triggers))
#             self.fill(self.tree, 'trigger_isomu24  '         , any('HLT_IsoMu24_v'                                           in name for name in fired_triggers))
#             self.fill(self.tree, 'trigger_isotkmu24'         , any('HLT_IsoTkMu24_v'                                         in name for name in fired_triggers))
#             self.fill(self.tree, 'trigger_mu50'              , any('HLT_Mu50_v'                                              in name for name in fired_triggers))
#             self.fill(self.tree, 'trigger_tkmu50'            , any('HLT_TkMu50_v'                                            in name for name in fired_triggers))
#             self.fill(self.tree, 'trigger_isomu22eta2p1'     , any('HLT_IsoMu22_eta2p1_v'                                    in name for name in fired_triggers))
#             self.fill(self.tree, 'trigger_isotkmu22eta2p1'   , any('HLT_IsoTkMu22_eta2p1_v'                                  in name for name in fired_triggers))
#             self.fill(self.tree, 'trigger_isomu19medisotau32', any('HLT_IsoMu19_eta2p1_LooseIsoPFTau20_SingleL1_v'           in name for name in fired_triggers))
#             self.fill(self.tree, 'trigger_isomu21medisotau32', any('HLT_IsoMu21_eta2p1_LooseIsoPFTau20_SingleL1_v'           in name for name in fired_triggers))
#             self.fill(self.tree, 'trigger_ele25tighteta2p1'  , any('HLT_Ele25_eta2p1_WPTight_Gsf_v'                          in name for name in fired_triggers))
#             self.fill(self.tree, 'trigger_ele27tight'        , any('HLT_Ele27_WPTight_Gsf_v'                                 in name for name in fired_triggers))
#             self.fill(self.tree, 'trigger_ele27looseeta2p1'  , any('HLT_Ele27_eta2p1_WPLoose_Gsf_v'                          in name for name in fired_triggers))
#             self.fill(self.tree, 'trigger_ele45loosetauseed' , any('HLT_Ele45_WPLoose_Gsf_L1JetTauSeeded'                    in name for name in fired_triggers))
#             self.fill(self.tree, 'trigger_ele115'            , any('HLT_Ele115_CaloIdVT_GsfTrkIdT_v'                         in name for name in fired_triggers))
#             self.fill(self.tree, 'trigger_ele24tau20singleL1', any('HLT_Ele24_eta2p1_WPLoose_Gsf_LooseIsoPFTau20_SingleL1_v' in name for name in fired_triggers))
#             self.fill(self.tree, 'trigger_ele24tau20'        , any('HLT_Ele24_eta2p1_WPLoose_Gsf_LooseIsoPFTau20_v'          in name for name in fired_triggers))
#             self.fill(self.tree, 'trigger_ele24tau30'        , any('HLT_Ele24_eta2p1_WPLoose_Gsf_LooseIsoPFTau30_v'          in name for name in fired_triggers))
#             self.fill(self.tree, 'trigger_doubletau35'       , any('HLT_DoubleMediumIsoPFTau35_Trk1_eta2p1_Reg_v'            in name for name in fired_triggers))
#             self.fill(self.tree, 'trigger_doubletau35comb'   , any('HLT_DoubleMediumCombinedIsoPFTau35_Trk1_eta2p1_Reg_v'    in name for name in fired_triggers))

            if hasattr(tau, 'genp') and tau.genp:
                self.fillGenParticle(self.tree, 'tau_gen', tau.genp)
                if hasattr(tau, 'genJet') and tau.genJet():
                    self.fillGenParticle(self.tree, 'tau_gen_vis', tau.genJet())
                    self.fill(self.tree, 'tau_gen_decayMode', tauDecayModes.genDecayModeInt(tau.genJet()))

            if hasattr(tau, 'L1matches') and len(tau.L1matches):
                self.fillL1object(self.tree, 'tau_L1', tau.L1matches[0])

            # Leading CH part
            if tau.signalChargedHadrCands().size() == 0:
                print 'Uh, tau w/o charged hadron???'
            
            leading_ch = tau.signalChargedHadrCands()[0].get()
            self.fillTrackInfo(leading_ch, 'tau_lead_ch')
                        
            self.fillTree(event)





