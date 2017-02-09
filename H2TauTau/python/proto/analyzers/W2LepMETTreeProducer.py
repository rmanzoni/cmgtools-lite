from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle

from CMGTools.H2TauTau.proto.analyzers.H2TauTauTreeProducerBase import H2TauTauTreeProducerBase
from CMGTools.H2TauTau.proto.analyzers.TreeVariablesWToLNu      import leptonMET_vars, event_vars, p4_vars, met_vars

class W2LepMETTreeProducer(H2TauTauTreeProducerBase):

    '''
    '''

    def __init__(self, *args):
        super(W2LepMETTreeProducer, self).__init__(*args)

    def declareHandles(self):
        super(W2LepMETTreeProducer, self).declareHandles()
            
    def declareVariables(self, setup):
        
        # book event
        self.bookEvent(self.tree)
        
        # book top pt reweighing
        self.bookTopPtReweighting(self.tree)
        
        # book leptonMET
        self.bookLepMET(self.tree, 'lepmet')
        
        # book gen info
        self.bookGenInfo(self.tree)

        # book gen vector boson
        self.bookGenParticle(self.tree, 'genVboson')

        # book jets & HT
        self.bookJet(self.tree, 'jet1')
        self.bookJet(self.tree, 'jet2')

        self.bookJet(self.tree, 'bjet1')
        self.bookJet(self.tree, 'bjet2')

        self.var(self.tree, 'HT_allJets')
        self.var(self.tree, 'HT_jets')
        self.var(self.tree, 'HT_bJets')
        self.var(self.tree, 'HT_cleanJets')
        self.var(self.tree, 'HT_jets30')
        self.var(self.tree, 'HT_cleanJets30')

    def process(self, event):

        self.readCollections(event.input)

        self.tree.reset()

        if not eval(self.skimFunction):
            return False
        
        # Top-reweighting need to come befor fillEvent, to include this into event weight
        self.fillTopPtReweighting(self.tree, event)

        # fill event
        self.fillEvent(self.tree, event)

        # fill leptonMET
        self.fillLepMET(self.tree, 'lepmet', event.leptonMET)
        
        # fill gen info
        self.fillGenInfo(self.tree, event)
        if len(event.genVboson)==1:
            self.fillGenParticle(self.tree, 'genVboson', event.genVboson[0])
        
        # fill jets & HT
        self.fill(self.tree, 'HT_allJets', event.HT_allJets) 
        self.fill(self.tree, 'HT_jets', event.HT_jets) 
        self.fill(self.tree, 'HT_bJets', event.HT_bJets)
        self.fill(self.tree, 'HT_cleanJets', event.HT_cleanJets)
        self.fill(self.tree, 'HT_jets30', event.HT_jets30)
        self.fill(self.tree, 'HT_cleanJets30', event.HT_cleanJets30) 
        
        for i, jet in enumerate(event.cleanJets[:2]):
            self.fillJet(self.tree, 'jet{n}'.format(n=str(i + 1)), jet, fill_extra=hasattr(self.cfg_ana, 'addMoreJetInfo') and self.cfg_ana.addMoreJetInfo)

        for i, jet in enumerate(event.cleanBJets[:2]):
            self.fillJet(self.tree, 'bjet{n}'.format(n=str(i + 1)), jet, fill_extra=hasattr(self.cfg_ana, 'addMoreJetInfo') and self.cfg_ana.addMoreJetInfo)

        # fill tree
        if type(self) is W2LepMETTreeProducer:
            self.fillTree(event)
       

    
    # lep-met
    def bookLepMET(self, tree, p_name):
        self.bookGeneric(tree, leptonMET_vars, p_name)

    def fillLepMET(self, tree, p_name, lm):
        self.fillGeneric(tree, leptonMET_vars, lm, p_name)

    # event
    def bookEvent(self, tree):
        self.bookGeneric(tree, event_vars)

    def fillEvent(self, tree, event):
        self.fillGeneric(tree, event_vars, event)

    # 4-vector
    def book4Vector(self, tree):
        self.bookGeneric(tree, p4_vars)

    def fill4Vector(self, tree, p_name, p4):
        self.fillGeneric(tree, p4_vars, p4, p_name)

    # met
    def bookMET(self, tree, p_name):
        self.bookGeneric(tree, met_vars)

    def fillMET(self, tree, p_name, met):
        self.fillGeneric(tree, met_vars, met, p_name)
    
    
    
