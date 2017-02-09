import ROOT

from PhysicsTools.Heppy.physicsutils.TauDecayModes import tauDecayModes
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle

from CMGTools.H2TauTau.proto.analyzers.H2TauTauTreeProducerBase import H2TauTauTreeProducerBase

from CMGTools.H2TauTau.proto.analyzers.HTTGenAnalyzer import HTTGenAnalyzer

class TauTriggerTreeProducer(H2TauTauTreeProducerBase):
    ''' Tree producer for tau POG study.
    '''

    def __init__(self, *args):
        super(TauTriggerTreeProducer, self).__init__(*args)
        self.maxNTaus = 99

    def declareHandles(self):
        super(TauTriggerTreeProducer, self).declareHandles()


    def declareVariables(self, setup):

        self.bookTau(self.tree, 'tau')
        self.bookGenParticle(self.tree, 'tau_gen')
        self.bookParticle(self.tree, 'tau_gen_vis')
        self.var(self.tree, 'tau_gen_decaymode', int)
        self.var(self.tree, 'trigger_looseisotau20')
        self.var(self.tree, 'trigger_matched_looseisotau20')

        if hasattr(self.cfg_ana, 'addParticles'):
            for particle in self.cfg_ana.addParticles:
                self.bookParticle(self.tree, 'l2_%s' %particle)


    def process(self, event):
        # needed when doing handle.product(), goes back to
        # PhysicsTools.Heppy.analyzers.core.Analyzer
        self.readCollections(event.input)

        if not eval(self.skimFunction):
            return False


#         ptcut = 8.
#         ptSelGentauleps = [lep for lep in event.gentauleps if lep.pt() > ptcut]
#         ptSelGenleps = [lep for lep in event.genleps if lep.pt() > ptcut]
#         ptSelGenSummary = [p for p in event.generatorSummary if p.pt() > ptcut and abs(p.pdgId()) not in [6, 23, 24, 25, 35, 36, 37]]
# 
#         for tau in event.selectedTaus:
#             HTTGenAnalyzer.genMatch(event, tau, ptSelGentauleps,
#                                         ptSelGenleps, ptSelGenSummary)


        fired_triggers = [info.name for info in getattr(event, 'trigger_infos', []) if info.fired]
        self.fill(self.tree, 'trigger_looseisotau20', any('MC_LooseIsoPFTau20_v' in name for name in fired_triggers))

#         matched_paths = getattr(event.diLepton, 'matchedPaths', [])
#         self.fill(self.tree, 'trigger_matched_looseisotau20', any('MC_LooseIsoPFTau20_v' in name for name in matched_paths))

        for i_tau, tau in enumerate(event.inclusiveTaus):
            
            if i_tau > self.maxNTaus: break
            
            self.tree.reset()
            self.fillTau(self.tree, 'tau', tau)
            if tau.genp:
                self.fillGenParticle(self.tree, 'tau_gen', tau.genp)
                if tau.genJet():
                    self.fillGenParticle(self.tree, 'tau_gen_vis', tau.genJet())
                    self.fill(self.tree, 'tau_gen_decayMode', tauDecayModes.genDecayModeInt(tau.genJet()))

        
            self.fillTree(event)





