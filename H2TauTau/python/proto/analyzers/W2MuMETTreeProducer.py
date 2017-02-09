from CMGTools.H2TauTau.proto.analyzers.W2LepMETTreeProducer import W2LepMETTreeProducer

class W2MuMETTreeProducer(W2LepMETTreeProducer):

    '''
    '''

    def __init__(self, *args):
        super(W2MuMETTreeProducer, self).__init__(*args)

    def declareVariables(self, setup):
        super(W2MuMETTreeProducer, self).declareVariables(setup)

        self.bookMuon(self.tree, 'muon')

    def process(self, event):
        super(W2MuMETTreeProducer, self).process(event)
        
#         import pdb ; pdb.set_trace()
        # fill muon
        self.fillMuon(self.tree, 'muon', event.leptonMET.lep())

        self.fillTree(event)
