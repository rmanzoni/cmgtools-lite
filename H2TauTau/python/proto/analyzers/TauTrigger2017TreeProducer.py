import ROOT

from PhysicsTools.Heppy.physicsutils.TauDecayModes import tauDecayModes
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle

from CMGTools.H2TauTau.proto.analyzers.H2TauTauTreeProducerBase import H2TauTauTreeProducerBase
from CMGTools.H2TauTau.proto.analyzers.H2TauTauTreeProducerTauMu import H2TauTauTreeProducerTauMu

from CMGTools.H2TauTau.proto.analyzers.HTTGenAnalyzer import HTTGenAnalyzer

class TauTrigger2017TreeProducer(H2TauTauTreeProducerBase):
    ''' Tree producer for tau POG study.
    '''

    def __init__(self, *args):
        super(TauTrigger2017TreeProducer, self).__init__(*args)
        self.maxNTaus = 99

    def declareVariables(self, setup):

        self.bookEvent(self.tree)
        self.bookTau(self.tree, 'tau', fill_extra=True)
        self.bookGenParticle(self.tree, 'tau_gen')
        self.bookGenParticle(self.tree, 'tau_gen_vis')
        self.bookL1object(self.tree, 'tau_L1')
        self.bookParticle(self.tree, 'tau_L2')
        self.bookParticle(self.tree, 'tau_trigger_object')
        self.var(self.tree, 'tau_L2_iso')
        self.var(self.tree, 'tau_gen_decaymode', int)
        self.var(self.tree, 'trigger_matched_openisotau20')
        self.var(self.tree, 'tau_gen_decayMode')
        self.bookTrackInfo('tau_lead_ch')

        self.var(self.tree, 'tau_trigger_charged3hits')
        self.var(self.tree, 'tau_trigger_charged5hits')
        self.var(self.tree, 'tau_trigger_charged8hits')
        self.var(self.tree, 'tau_trigger_neutral'     )
        self.var(self.tree, 'tau_trigger_photons'     )

        if hasattr(self.cfg_ana, 'addParticles'):
            for particle in self.cfg_ana.addParticles:
                self.bookParticle(self.tree, 'l2_%s' %particle)
        

    def bookTrackInfo(self, name):
        H2TauTauTreeProducerTauMu.bookTrackInfo(self, name)

    def fillTrackInfo(self, track, name='tau_track'):
        H2TauTauTreeProducerTauMu.fillTrackInfo(self, track, name)

    def process(self, event):
        super(TauTrigger2017TreeProducer, self).process(event)

        # needed when doing handle.product(), goes back to
        # PhysicsTools.Heppy.analyzers.core.Analyzer
        self.readCollections(event.input)

        if not eval(self.skimFunction):
            return False

        fired_triggers = [info.name for info in getattr(event, 'trigger_infos', []) if info.fired]

        #import pdb ; pdb.set_trace()
        
        for i_tau, tau in enumerate(event.taus):
                
            if i_tau > self.maxNTaus: break
            
            self.tree.reset()
        
            self.fillEvent(self.tree, event)

            self.fillTau(self.tree, 'tau', tau, fill_extra=True)
            self.fill(self.tree, 'trigger_matched_openisotau20', any(to.hasFilterLabel('hltPFTau20TrackPt1Reg') for to in tau.tos))

            if hasattr(tau, 'to'):
                self.fillParticle(self.tree, 'tau_trigger_object', tau.to)

            if hasattr(tau, 'genp') and tau.genp:
                self.fillGenParticle(self.tree, 'tau_gen', tau.genp)
                if hasattr(tau, 'genJet') and tau.genJet():
                    self.fillGenParticle(self.tree, 'tau_gen_vis', tau.genJet())
                    self.fill(self.tree, 'tau_gen_decayMode', tauDecayModes.genDecayModeInt(tau.genJet()))

            if hasattr(tau, 'L1matches') and len(tau.L1matches):
                self.fillL1object(self.tree, 'tau_L1', tau.L1matches[0])

            if hasattr(tau, 'L2'):
                self.fillParticle(self.tree, 'tau_L2', tau.L2)
                self.fill(self.tree, 'tau_L2_iso', tau.L2.L2iso)

            # Leading CH part
            if tau.signalChargedHadrCands().size() == 0:
                print 'Uh, tau w/o charged hadron???'
            
            leading_ch = tau.signalChargedHadrCands()[0].get()
            self.fillTrackInfo(leading_ch, 'tau_lead_ch')

            for disc in ['trigger_charged3hits', 'trigger_charged5hits', 'trigger_charged8hits', 'trigger_neutral', 'trigger_photons']:
                if hasattr(tau, disc):
                    self.fill(self.tree, 'tau_'+disc, getattr(tau, disc))
                        
            self.fillTree(event)





