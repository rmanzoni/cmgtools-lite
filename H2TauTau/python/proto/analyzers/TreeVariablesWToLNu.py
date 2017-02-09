from PhysicsTools.HeppyCore.utils.deltar import deltaR, deltaPhi

from CMGTools.H2TauTau.proto.analyzers.tauIDs import tauIDs, tauIDs_extra

class Variable():
    def __init__(self, name, function=None, type=float):
        self.name = name
        self.function = function
        if function is None:
            # Note: works for attributes, not member functions
            self.function = lambda x : getattr(x, self.name, -999.) 
        self.type = type

def default():
    return -999.

# event variables
event_vars = [
    Variable('run', type=int),
    Variable('lumi', type=int),
    Variable('event', lambda ev : ev.eventId, type=int),
    Variable('bx', lambda ev : (ev.input.eventAuxiliary().bunchCrossing() * ev.input.eventAuxiliary().isRealData()), type=int),
    Variable('orbit_number', lambda ev : (ev.input.eventAuxiliary().orbitNumber() * ev.input.eventAuxiliary().isRealData()), type=int),
    Variable('is_data', lambda ev: ev.input.eventAuxiliary().isRealData(), type=int),
    Variable('nPU', lambda ev : -99 if getattr(ev, 'nPU', -1) is None else getattr(ev, 'nPU', -1)),
    Variable('n_jets', lambda ev : len(ev.cleanJets30), type=int),
    Variable('n_jets_puid', lambda ev : sum(1 for j in ev.cleanJets30 if j.puJetId()), type=int),
    Variable('n_jets_20', lambda ev : len(ev.cleanJets), type=int),
    Variable('n_jets_20_puid', lambda ev : sum(1 for j in ev.cleanJets if j.puJetId()), type=int),
    Variable('n_bjets', lambda ev : len(ev.cleanBJets), type=int),
    Variable('n_jets_csvl', lambda ev : sum(1 for jet in ev.cleanJets if jet.btagWP('CSVv2IVFL')), type=int),
    Variable('n_vertices', lambda ev : len(ev.vertices), type=int),
    Variable('rho', lambda ev : ev.rho),
    Variable('hlt_calo_rho'),
    Variable('hlt_calo_rho_eta2p5'),
    Variable('hlt_pf_rho'),
    Variable('hlt_pf_rho_reg'),
    Variable('weight', lambda ev : ev.eventWeight),
    Variable('weight_vertex', lambda ev : ev.puWeight),
    # # Add back for embedded samples once needed
    # Variable('weight_embed', lambda ev : getattr(ev, 'embedWeight', 1.)),
#     Variable('weight_njet', lambda ev : -99 * (not hasattr(ev, 'NJetWeight')) + hasattr(ev, 'NJetWeight') * getattr(ev, 'NJetWeight')),
    # # Add back the following only for ggH samples once needed
    # Variable('weight_hqt', lambda ev : getattr(ev, 'higgsPtWeight', 1.)),
    # Variable('weight_hqt_up', lambda ev : getattr(ev, 'higgsPtWeightUp', 1.)),
    # Variable('weight_hqt_down', lambda ev : getattr(ev, 'higgsPtWeightDown', 1.)),
    # Variable('weight_njet', lambda ev : ev.NJetWeight),
    # Variable('delta_phi_dil_jet1', lambda ev : deltaPhi(ev.diLepton.p4().phi(), ev.cleanJets[0].phi()) if len(ev.cleanJets)>0 else -999.),
    # Variable('delta_phi_dil_met', lambda ev : deltaPhi(ev.diLepton.p4().phi(), ev.diLepton.met().phi())),
    # Variable('delta_phi_dil_jet2', lambda ev : deltaPhi(ev.diLepton.p4().phi(), ev.cleanJets[1].phi()) if len(ev.cleanJets)>1 else -999.),
    # Variable('delta_eta_dil_jet1', lambda ev : abs(ev.diLepton.p4().eta() - ev.cleanJets[0].eta()) if len(ev.cleanJets)>0 else -999.),
    # Variable('delta_eta_dil_jet2', lambda ev : abs(ev.diLepton.p4().eta() - ev.cleanJets[1].eta()) if len(ev.cleanJets)>1 else -999.),
]

# lep-met object variables
leptonMET_vars = [
    Variable('mass', lambda lm : lm.mass() ),
    Variable('pt', lambda lm : lm.p4().pt()),
    Variable('pz', lambda lm : lm.p4().pz()),
    Variable('px', lambda lm : lm.p4().px()),
    Variable('py', lambda lm : lm.p4().py()),
    Variable('e', lambda lm : lm.p4().energy()),
    Variable('dR', lambda lm : lm.dR()),
    Variable('dPhi', lambda lm : lm.dPhi()),
    Variable('dEta', lambda lm : lm.dEta()),
    Variable('mt', lambda lm : lm.mt()),
#     Variable('met_cov00', lambda lm : lm.mvaMetSig(0, 0) if lm.mvaMetSig else 0.),
#     Variable('met_cov10', lambda lm : lm.mvaMetSig(1, 0) if lm.mvaMetSig else 0.),
#     Variable('met_cov11', lambda lm : lm.mvaMetSig(1, 1) if lm.mvaMetSig else 0.),
    Variable('met_phi', lambda lm : lm.met().phi()),
    Variable('met_px', lambda lm : lm.met().px()),
    Variable('met_py', lambda lm : lm.met().py()),
    Variable('met_pt', lambda lm : lm.met().pt()),
]

met_vars = [
    Variable('pt' , lambda met : met.pt()),
    Variable('phi', lambda met : met.phi()),
    Variable('px' , lambda met : met.px()),
    Variable('py' , lambda met : met.py()),
]

p4_vars = [
    Variable('mass', lambda lm : lm.mass() ),
    Variable('pt', lambda lm : lm.p4().pt()),
    Variable('pz', lambda lm : lm.p4().pz()),
    Variable('px', lambda lm : lm.p4().px()),
    Variable('py', lambda lm : lm.p4().py()),
    Variable('e', lambda lm : lm.p4().energy()),
]
