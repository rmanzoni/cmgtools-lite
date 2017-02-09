import math

from PhysicsTools.Heppy.physicsobjects.PhysicsObjects import Muon, Tau
from PhysicsTools.Heppy.physicsobjects.Electron import Electron
from PhysicsTools.HeppyCore.utils.deltar import deltaR, deltaPhi
from ROOT import TVector3

from CMGTools.H2TauTau.proto.physicsobjects.DiObject import DiObject, DiTau

class LeptonMET(DiObject):

    '''    '''

    def __init__(self, lep, met):
        self.lep_ = lep
        self.met_ = met
        self.p4_ = (lep.p4() + met.p4())

    def mass(self):
        return self.p4_.mass()

    def p4(self):
        return self.p4_

    def lep(self):
        return self.lep_

    def met(self):
        return self.met_

    def leg1(self):
        return self.lep_

    def leg2(self):
        return self.met_

    def dR(self):
        return deltaR(self.met_, self.lep_)

    def dPhi(self):
        return deltaPhi(self.met_.phi(), self.lep_.phi())

    def dEta(self):
        return abs(self.met_.eta() - self.lep_.eta())

    # This is the default transverse mass by convention
    def mt(self):
        return DiTau.calcMT(self.lep_, self.met_)

    def __getattr__(self, name):
        '''Redefine getattr to original version.'''
        raise AttributeError


class MuonMET(LeptonMET):
    def __init__(self, lep, met):
        super(MuonMET, self).__init__(lep, met)
        self.mu = Muon(super(MuonMET, self).lep())

    def lep(self):
        return self.mu


class ElectronMET(LeptonMET):
    def __init__(self, lep, met):
        super(ElectronMET, self).__init__(lep, met)
        self.ele = Electron(super(ElectronMET, self).lep())

    def lep(self):
        return self.ele


class TauMET(LeptonMET):
    def __init__(self, lep, met):
        super(TauMET, self).__init__(lep, met)
        self.tau = Tau(super(TauMET, self).lep())

    def lep(self):
        return self.tau
