from PhysicsTools.HeppyCore.utils.deltar import deltaR, deltaPhi
from CMGTools.H2TauTau.proto.analyzers.TreeVariables import Variable

def default():
    return -999.

# event variables
event_vars = [
    Variable('run', type=int),
    Variable('lumi', type=int),
    Variable('event', lambda ev: ev.eventId, type=int),
    Variable('bx', lambda ev: (ev.input.eventAuxiliary().bunchCrossing() * ev.input.eventAuxiliary().isRealData()), type=int),
    Variable('orbit_number', lambda ev: (ev.input.eventAuxiliary().orbitNumber() * ev.input.eventAuxiliary().isRealData()), type=int),
    Variable('is_data', lambda ev: ev.input.eventAuxiliary().isRealData(), type=int),
    Variable('nPU', lambda ev: default() if getattr(ev, 'nPU', -1) is None else getattr(ev, 'nPU', -1), type=int),
    Variable('n_vertices', lambda ev : len(ev.vertices) if hasattr(ev, 'vertices') else default(), type=int),
    Variable('rho', lambda ev : ev.rho if hasattr(ev, 'vertices') else default()),
    Variable('hlt_calo_rho'),
    Variable('hlt_calo_rho_eta2p5'),
    Variable('hlt_pf_rho'),
    Variable('hlt_pf_rho_reg'),
]

# generic particle
physobj_vars = [
    Variable('pt', lambda p: p.pt()),
    Variable('eta', lambda p: p.eta()),
    Variable('phi', lambda p: p.phi()),
    Variable('charge', lambda p: p.charge() if hasattr(p, 'charge') else 0),  # charge may be non-integer for gen particles
    Variable('mass', lambda p: p.mass()),
]

# trig obj
trigobj_vars = [
    Variable('trigger_charged3hits', lambda p: p.trigger_charged3hits()),
    Variable('trigger_charged5hits', lambda p: p.trigger_charged5hits()),
    Variable('trigger_charged8hits', lambda p: p.trigger_charged8hits()),
    Variable('trigger_neutral', lambda p: p.trigger_neutral()),
    Variable('trigger_dbcorr0p2Cone0p8', lambda p: p.trigger_dbcorr0p2Cone0p8()),
    Variable('trigger_rhocorrCone0p5', lambda p: p.trigger_rhocorrCone0p5()),
    Variable('trigger_photons', lambda p: p.trigger_photons()),
]
