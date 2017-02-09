import math
import ROOT

from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.HeppyCore.utils.deltar import bestMatch

from PhysicsTools.Heppy.physicsobjects.PhysicsObject import PhysicsObject
from PhysicsTools.Heppy.physicsobjects.GenParticle import GenParticle

from CMGTools.H2TauTau.proto.analyzers.TauGenTreeProducer import TauGenTreeProducer
from CMGTools.H2TauTau.proto.analyzers.HTTGenAnalyzer import HTTGenAnalyzer

class W2LepMETGenAnalyzer(HTTGenAnalyzer):

    '''Add generator information to hard leptons.
    '''

    def process(self, event):
        event.genmet_pt  = -99.
        event.genmet_eta = -99.
        event.genmet_e   = -99.
        event.genmet_px  = -99.
        event.genmet_py  = -99.
        event.genmet_phi = -99.
        event.weight_gen = 1.

        if self.cfg_comp.isData:
            return True

        self.readCollections(event.input)
        event.genJets      = self.mchandles['genJets'].product()
        event.jets         = self.handles['jets'].product()
        event.genParticles = self.mchandles['genParticles'].product()

        event.genleps    = [p for p in event.genParticles if abs(p.pdgId()) in [11, 13] and p.statusFlags().isPrompt()]
        event.gentauleps = [p for p in event.genParticles if abs(p.pdgId()) in [11, 13] and p.statusFlags().isDirectPromptTauDecayProduct()]
        event.gentaus    = [p for p in event.genParticles if abs(p.pdgId()) == 15 and p.statusFlags().isPrompt() and not any(abs(self.getFinalTau(p).daughter(i_d).pdgId()) in [11, 13] for i_d in xrange(self.getFinalTau(p).numberOfDaughters()))]
        event.genVboson  = [p for p in event.genParticles if abs(p.pdgId()) in [23, 24] and p.status()==22] # from hard scattering
        self.getGenTauJets(event)

        event.weight_gen = self.mchandles['genInfo'].product().weight()
        event.eventWeight *= event.weight_gen

        # gen MET as sum of the neutrino 4-momenta
        neutrinos = [p for p in event.genParticles if abs(p.pdgId()) in (12, 14, 16) and p.status() == 1]

        genmet = ROOT.math.XYZTLorentzVectorD()
        for nu in neutrinos:
            genmet += nu.p4()

        event.genmet = genmet
        event.genmet_pt  = genmet.pt()
        event.genmet_eta = genmet.eta()
        event.genmet_e   = genmet.e()
        event.genmet_px  = genmet.px()
        event.genmet_py  = genmet.py()
        event.genmet_phi = genmet.phi()

        ptcut = 0.
        # you can apply a pt cut on the gen leptons, electrons and muons
        # in HIG-13-004 it was 8 GeV
        if hasattr(self.cfg_ana, 'genPtCut'):
            ptcut = self.cfg_ana.genPtCut

        self.ptSelGentauleps = [lep for lep in event.gentauleps if lep.pt() > ptcut]
        self.ptSelGenleps    = [lep for lep in event.genleps if lep.pt() > ptcut]
        self.ptSelGenSummary = []
        # self.ptSelGenSummary = [p for p in event.generatorSummary if p.pt() > ptcut and abs(p.pdgId()) not in [6, 11, 13, 15, 23, 24, 25, 35, 36, 37]]
        # self.ptSelGentaus    = [ lep for lep in event.gentaus    if lep.pt()
        # > ptcut ] # not needed

        self.lep = event.lepton
        self.met = event.met

        self.genMatch(event, self.lep, self.ptSelGentauleps, self.ptSelGenleps, self.ptSelGenSummary)

        self.attachGenStatusFlag(self.lep)

        if hasattr(event, 'selectedTaus'):
            for tau in event.selectedTaus:
                self.genMatch(event, tau, self.ptSelGentauleps, self.ptSelGenleps, self.ptSelGenSummary)

        if self.cfg_comp.name.find('TT') == -1 or self.cfg_comp.name.find('TTH') != -1:
            self.getTopPtWeight(event)

        return True
