from CMGTools.H2TauTau.proto.analyzers.W2LepMETTreeProducer import W2LepMETTreeProducer
from PhysicsTools.Heppy.physicsutils.TauDecayModes import tauDecayModes

class W2TauMETTreeProducer(W2LepMETTreeProducer):

    '''
    '''

    def __init__(self, *args):
        super(W2TauMETTreeProducer, self).__init__(*args)

    def declareVariables(self, setup):
        super(W2TauMETTreeProducer, self).declareVariables(setup)

        self.bookTau(self.tree, 'tau')
        self.bookGenParticle(self.tree, 'tau_gen')
        self.var(self.tree, 'tau_gen_lepfromtau', int)
        self.bookParticle(self.tree, 'tau_gen_vis')
        self.var(self.tree, 'tau_gen_decaymode', int)

    def process(self, event):
        super(W2TauMETTreeProducer, self).process(event)
        
        tau = event.leptonMET.lep()

        import pdb ; pdb.set_trace()    
        
        # fill tau
        self.fillTau(self.tree, 'tau', tau)
        if hasattr(tau, 'genp') and tau.genp:
            self.fillGenParticle(self.tree, 'tau_gen', tau.genp)
            self.fill(self.tree, 'tau_gen_lepfromtau', tau.isTauLep)

        # save the p4 of the visible tau products at the generator level
        if tau.genJet() and hasattr(tau, 'genp') and tau.genp and abs(tau.genp.pdgId()) == 15:
            self.fillParticle(self.tree, 'tau_gen_vis', tau.physObj.genJet())
            tau_gen_dm = tauDecayModes.translateGenModeToInt(tauDecayModes.genDecayModeFromGenJet(tau.physObj.genJet()))
            self.fill(self.tree, 'tau_gen_decaymode', tau_gen_dm)
            if tau_gen_dm in [1, 2, 3, 4]:
                pt_neutral = 0.
                pt_charged = 0.
                for daughter in tau.genJet().daughterPtrVector():
                    id = abs(daughter.pdgId())
                    if id in [22, 11]:
                        pt_neutral += daughter.pt()
                    elif id not in [11, 13, 22] and daughter.charge():
                        if daughter.pt() > pt_charged:
                            pt_charged = daughter.pt()
        
        
        self.fillTree(event)
