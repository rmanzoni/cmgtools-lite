import operator

from itertools import product, combinations
from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
from PhysicsTools.Heppy.physicsobjects.PhysicsObjects import Lepton
from PhysicsTools.HeppyCore.utils.deltar import deltaR, deltaR2

from CMGTools.H2TauTau.proto.physicsobjects.ObjectMET import LeptonMET

class LeptonMETAnalyzer(Analyzer):

    """    """

    LeptonMETClass = LeptonMET
    LeptonClass = Lepton 
    LeptonVeto1Class = Lepton
    LeptonVeto2Class = Lepton

    def beginLoop(self, setup):
        super(LeptonMETAnalyzer, self).beginLoop(setup)
        self.counters.addCounter('LeptonMET')
        count = self.counters.counter('LeptonMET')
        count.register('all events')
        count.register('> 0 lepton')
        count.register('second lepton veto flavour 1')
        count.register('second lepton veto flavour 2')
        count.register('Z veto')
        count.register('lepton offline cuts passed')
        count.register('met offline cuts passed')
        count.register('trig matched')
        count.register('exactly 1 good lepton')

    def declareHandles(self):
        super(LeptonMETAnalyzer, self).declareHandles()
        self.handles['triggerObjects'] =  AutoHandle(
            'selectedPatTrigger',
            'std::vector<pat::TriggerObjectStandAlone>'
        )

    def buildLeptonMET(self, cmgLeptons, event):
        '''Creates python DiLeptons from the di-leptons read from the disk.
        to be overloaded if needed.'''
        met = self.handles['met'].product()[0]
        return map(self.__class__.LeptonMETClass, cmgLeptons, [met for i in range(len(cmgLeptons))])

    def buildLeptons(self, cmgLeptons, event):
        '''Creates python Leptons from the leptons read from the disk.
        to be overloaded if needed.'''
        return map(self.__class__.LeptonClass, cmgLeptons)

    def buildLeptonsVeto1(self, cmgLeptons, event):
        '''Creates python Leptons from the leptons read from the disk.
        to be overloaded if needed.'''
        return map(self.__class__.LeptonVeto1Class, cmgLeptons)

    def buildLeptonsVeto1(self, cmgLeptons, event):
        '''Creates python Leptons from the leptons read from the disk.
        to be overloaded if needed.'''
        return map(self.__class__.LeptonVeto2Class, cmgLeptons)

    def process(self, event, fillCounter=False):
        self.readCollections(event.input)
        
        event.leptons = self.buildLeptons(self.handles['leptons'].product(), event)

        event.LeptonMETs   = self.buildLeptonMET(event.leptons, event)

        event.leptonsVeto1 = self.buildLeptonsVeto1(self.handles['leptonVeto1'].product(), event)
        event.leptonsVeto2 = self.buildLeptonsVeto2(self.handles['leptonVeto2'].product(), event)

        return self.selectionSequence(event)

    def selectionSequence(self, event):

        self.counters.counter('LeptonMET').inc('all events')

        # check there's at least one lepton (MET is always present)
        selLeptonMET = event.LeptonMETs
        if len(selLeptonMET) == 0:
            return False
        self.counters.counter('LeptonMET').inc('> 0 lepton')
        
        # testing lepton
        #import pdb ; pdb.set_trace()
        selLeptonMET = [lm for lm in selLeptonMET if self.testLep(lm.lep())]
        if len(selLeptonMET) == 0:
            return False
        self.counters.counter('LeptonMET').inc('lepton offline cuts passed')

        # testing met
        selLeptonMET = [lm for lm in selLeptonMET if self.testMET(lm.met())]
        if len(selLeptonMET) == 0:
            return False
        self.counters.counter('LeptonMET').inc('met offline cuts passed')
        
        # lepton veto flavour 1
        if not self.veto1(event.leptonsVeto1):
            return False
        self.counters.counter('LeptonMET').inc('second lepton veto flavour 1')

        # lepton veto flavour 1
        if not self.veto2(event.leptonsVeto2):
            return False
        self.counters.counter('LeptonMET').inc('second lepton veto flavour 2')

        # Z veto
        if not self.passZtoLLveto(event.leptons):
            return False
        self.counters.counter('LeptonMET').inc('Z veto')

        # Trigger matching
        require_match = len(self.cfg_comp.triggers) > 0
        if hasattr(self.cfg_ana, 'noTrigMatching') and self.cfg_ana.noTrigMatching:
            require_match = False

        if require_match:
            selDiLeptons = [lm for lm in selLeptonMET if self.trigMatched(event, lm)]
            if len(selDiLeptons) == 0:
                return False
            self.counters.counter('LeptonMET').inc('trig matched')

        
        event.selLeptonMET = selLeptonMET

        event.leptonMET = self.bestLeptonMET(selLeptonMET)
        event.lepton = event.leptonMET.lep()
        event.met = event.leptonMET.met()

        return True

    def passZtoLLveto(self, leptons, mass=(84., 100.)):
        '''
        reject Z to ll events
        '''
        opposite_charge = lambda dil : dil[0].charge() * dil[1].charge() < 0
        dil_mass = lambda dil : (dil[0].p4() + dil[1].p4()).mass()
        zs = [dil for dil in combinations(leptons, 2) if opposite_charge and dil_mass > mass[0] and dil_mass < mass[1]]
        return (len(zs) == 0) 
        
    def veto1(self, leptons):
        '''Should implement a default version running on event.leptons.'''
        return True

    def veto2(self, leptons):
        '''Should implement a default version running on event.leptons.'''
        return True

    def testLep(self, leg, isocut=None):
        '''returns testLeg1ID && testLeg1Iso && testLegKine for leg1'''
        return self.testLepID(leg) and \
               self.testLepIso(leg, isocut) and \
               self.testLepKine(leg, self.cfg_ana.ptlep, self.cfg_ana.etalep)

    def testLepKine(self, leg, ptcut, etacut):
        '''Tests pt and eta.'''
        return leg.pt() > ptcut and \
            abs(leg.eta()) < etacut

    def testLepID(self, leg):
        '''Always return true by default, overload in your subclass'''
        return True

    def testLepIso(self, leg, isocut):
        '''Always return true by default, overload in your subclass'''
        return True

    def testMET(self, leg):
        '''Always return true by default, overload in your subclass'''
        return True

    def bestLeptonMET(self, selLeptonMET):
        '''Returns the best diLepton (most isolated lepton).'''
        return max(selLeptonMET, key=lambda x : (-x.lep().relIso(0.5), x.dR))

    def trigMatched(self, event, lm, requireAllMatched=False, ptMin=None,  etaMax=None, relaxIds=[11, 15], onlyLeg1=False, checkBothLegs=False):
        '''Check that at least one trigger object per pgdId from a given trigger 
        has a matched leg with the same pdg ID. If requireAllMatched is True, 
        requires that each single trigger object name given in the sample
        cfg has a match.'''
        matched = False
        lep = lm.lep()
        lm.matchedPaths = set()

        if hasattr(self.cfg_ana, 'filtersToMatch'):
            for filtersToMatch in self.cfg_ana.filtersToMatch:
                lep.tos = []
                triggerObjects = self.handles['triggerObjects'].product()
                for item in product(triggerObjects, filtersToMatch):
                    to     = item[0]
                    filter = item[1]

                    if not to.hasFilterLabel(filter):
                        continue
                    
                    # RIC: this does not mean that the last filter is fired!
                    #      you need to make sure the filter you're requiring
                    #      *is* the last filter, regardless of its position
                    #      in the collection
                    # print to.filterLabels()[-1], to.filterLabels()[-1] != filter
                    #if to.filterLabels()[-1] != filter:
                    #    continue

                    if self.trigObjMatched(to, [leg]):
                        setattr(leg, filter, to)
                        leg.tos.append(to)
                    
                # RIC: assign as trigger object the one with the highest pt
                if leg.tos:
                    leg.to = sorted(leg.tos, key=lambda x: x.pt(), reverse=True)[0]
                    

        for info in event.trigger_infos:
            
            if not info.fired:
                continue

            matchedIds = []
            matchedLegs = []
            
            for to, to_names in zip(info.objects, info.object_names):
                if ptMin and to.pt() < ptMin:
                    continue
                if etaMax and abs(to.eta()) > etaMax:
                    continue
                toMatched, objMatchedLegs = self.trigObjMatched(to, [lep], names=to_names, relaxIds=relaxIds)
                if requireAllMatched:
                    objMatchedLegs = [mleg for mleg in objMatchedLegs if set(self.cfg_comp.triggerobjects) == mleg.triggernames]

                else:
                    matchedLegs += objMatchedLegs
                if toMatched:
                    matchedIds.append(abs(to.pdgId()))

            if set(matchedIds) == info.objIds and \
               len(matchedIds) >= len(legs) * sameFlavour:
                if checkBothLegs:
                    if all(l in matchedLegs for l in legs):
                        matched = True
                        lm.matchedPaths.add(info.name)
                    else:
                        matched = False
                else:
                    matched = True
                    lm.matchedPaths.add(info.name)
        
        return matched

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
