from itertools import product

import PhysicsTools.HeppyCore.framework.config as cfg

from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
from PhysicsTools.Heppy.physicsobjects.Tau import Tau
from PhysicsTools.HeppyCore.utils.deltar import deltaR, deltaR2

from CMGTools.H2TauTau.proto.analyzers.HTTGenAnalyzer import HTTGenAnalyzer
from CMGTools.H2TauTau.proto.analyzers.DiLeptonAnalyzer import DiLeptonAnalyzer

 
class TauAnalyzer( Analyzer ):

    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(TauAnalyzer, self).__init__(cfg_ana, cfg_comp, looperName)

    def declareHandles(self):
        super(TauAnalyzer, self).declareHandles()

        self.handles['taus']           = AutoHandle('slimmedTaus'   , 'std::vector<pat::Tau>'         )
        self.handles['puppi_met']      = AutoHandle('pfMetPuppi'    , 'std::vector<reco::PFMET>'      )
        self.handles['pfmet']          = AutoHandle('slimmedMETs'   , 'std::vector<pat::MET>'         )

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

        self.mchandles['genParticles'] = AutoHandle('prunedGenParticles', 'std::vector<reco::GenParticle>')
        self.mchandles['genJets']      = AutoHandle('slimmedGenJets'    , 'std::vector<reco::GenJet>'     )

    def process(self, event):
        self.readCollections(event.input)

        # Take the pre-sorted vertices from miniAOD
        event.goodVertices = event.vertices
        
        event.taus = self.buildTaus(event)
        event.taus = [tau for tau in event.taus if self.testTau(tau)]
        
        if not event.taus:
            return False

        event.triggerObjects = self.handles['triggerObjects'].product()

        if not event.input.eventAuxiliary().isRealData():
            event.genParticles = self.mchandles['genParticles'].product()

            event.genleps    = [p for p in event.genParticles if abs(p.pdgId()) in [11, 13] and p.statusFlags().isPrompt()]
            event.gentauleps = [p for p in event.genParticles if abs(p.pdgId()) in [11, 13] and p.statusFlags().isDirectPromptTauDecayProduct()]
            event.gentaus    = [p for p in event.genParticles if abs(p.pdgId()) == 15 and p.statusFlags().isPrompt() and not any(abs(HTTGenAnalyzer.getFinalTau(p).daughter(i_d).pdgId()) in [11, 13] for i_d in xrange(HTTGenAnalyzer.getFinalTau(p).numberOfDaughters()))]

            for tau in event.taus:
                HTTGenAnalyzer.genMatch(event, tau, event.gentauleps, event.genleps, [], dR=0.2, matchAll=True)

        for tau in event.taus:
            self.trigMatching(event, tau)

        #import pdb ; pdb.set_trace()
        
        return True
            
    def buildTaus(self, event):
        taus = map( Tau, self.handles['taus'].product() )
        for tau in taus:
            tau.associatedVertex = event.goodVertices[0]
        return taus

    def testTauVertex(self, tau):
        '''Tests vertex constraints, for tau'''
        isPV = abs(tau.leadChargedHadrCand().dz()) < 0.2
        return isPV

    def testTau(self, tau):
        ptcut  = 20.
        etacut = 2.3
        skipDM = False
        isocut = -999
        
        if hasattr(self.cfg_ana, 'ptcut'):
            ptcut = self.cfg_ana.ptcut

        if hasattr(self.cfg_ana, 'etacut'):
            etacut = self.cfg_ana.etacut

        if hasattr(self.cfg_ana, 'skipDM'):
            idcut = self.cfg_ana.skipDM

        if hasattr(self.cfg_ana, 'isocut'):
            isocut = self.cfg_ana.isocut
    
        passed  = tau.tauID('byVLooseIsolationMVArun2v1DBoldDMwLT') > isocut # pass VLoose WP
        passed *= (skipDM or (tau.tauID('decayModeFindingNewDMs') > 0) )     # pass new DM
        passed *= abs(tau.eta()) < etacut and tau.pt() > ptcut               # kinematics
        passed *= self.testTauVertex(tau)                                    # take the tau from PV
        return passed
    
    def trigMatching(self, event, tau, ptMin=0., etaMax=9999.):
        '''
        this does not select, just appends matched trigger objects
        '''
        tau.tos = []
        if hasattr(self.cfg_ana, 'filtersToMatch'):
            for it in self.cfg_ana.filtersToMatch:
                for item in product(event.triggerObjects, [it]):
                    to, filter = item
                    if to.pt() < ptMin or abs(to.eta()) > etaMax: continue
                    if not to.hasFilterLabel(filter): continue
                    #import pdb ; pdb.set_trace()
                    if self.trigObjMatched(to, [tau]):
                        setattr(tau, filter, to)
                        tau.tos.append(to)
                    
                # RIC: assign as trigger object the one with the highest pt
                if tau.tos:
                    tau.to = sorted(tau.tos, key=lambda x: x.pt(), reverse=True)[0]
                            
    def trigObjMatched(self, to, legs, names=None, dR2Max=0.25, relaxIds=[11, 15]):  # dR2Max=0.089999
        '''Returns true if the trigger object is matched to one of the given
        legs'''
        eta = to.eta()
        phi = to.phi()
        pdgId = abs(to.pdgId())
        to.matched = False
        matchedLegs = []
        for leg in legs:
            # JAN - Single-ele trigger filter has pdg ID 0, to be understood
            # RIC - same seems to happen with di-tau
            # JAN - If it's two triggers, there's a logical flaw in the e-tau
            # channel, so maybe we'll have to move to explicit but not very
            # general requirements (for now added option to relax explicitly)
            if pdgId == abs(leg.pdgId()) or \
               (pdgId == 0 and abs(leg.pdgId()) in relaxIds):
                if deltaR2(eta, phi, leg.eta(), leg.phi()) < dR2Max:
                    to.matched = True
                    matchedLegs.append(leg)
                    if hasattr(leg, 'triggerobjects'):
                        if to not in leg.triggerobjects:
                            leg.triggerobjects.append(to)
                    else:
                        leg.triggerobjects = [to]

                    if names:
                        if hasattr(leg, 'triggernames'):
                            leg.triggernames.update(names)
                        else:
                            leg.triggernames = set(names)

        return to.matched, matchedLegs


