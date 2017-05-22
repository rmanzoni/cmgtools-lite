from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle

import PhysicsTools.HeppyCore.framework.config as cfg


class EventAnalyzer(Analyzer):
    '''
    '''
    
    def declareHandles(self):
        super(EventAnalyzer, self).declareHandles()

        self.handles['hltFixedGridRhoFastjetAllCaloForMuons'] = AutoHandle(
            'hltFixedGridRhoFastjetAllCaloForMuons',
            'double',
            mayFail=True,
            disableAtFirstFail=False,
        )

        self.handles['hltFixedGridRhoFastjetAllCalo'] = AutoHandle(
            'hltFixedGridRhoFastjetAllCalo',
            'double',
            mayFail=True,
            disableAtFirstFail=False,
        )

        self.handles['hltFixedGridRhoFastjetAll'] = AutoHandle(
            'hltFixedGridRhoFastjetAll',
            'double',
            mayFail=True,
            disableAtFirstFail=False,
        )

        self.handles['hltFixedGridRhoFastjetAllPFReg'] = AutoHandle(
            'hltFixedGridRhoFastjetAllPFReg',
            'double',
            mayFail=True,
            disableAtFirstFail=False,
        )


    def process(self, event):
        self.readCollections(event.input)
        
        event.run     = event.input.eventAuxiliary().id().run()
        event.lumi    = event.input.eventAuxiliary().id().luminosityBlock()
        event.eventId = event.input.eventAuxiliary().id().event()

        try:
            event.hlt_calo_rho_eta2p5 = self.handles['hltFixedGridRhoFastjetAllCaloForMuons'].product()[0]
        except:
            event.hlt_calo_rho_eta2p5 = -99.
            
        try:
            event.hlt_calo_rho = self.handles['hltFixedGridRhoFastjetAllCalo'].product()[0]
        except:
            event.hlt_calo_rho = -99.
    
        try:
            event.hlt_pf_rho = self.handles['hltFixedGridRhoFastjetAll'].product()[0]
        except:
            event.hlt_pf_rho = -99.

        try:
            event.hlt_pf_rho_reg = self.handles['hltFixedGridRhoFastjetAllPFReg'].product()[0]
        except:
            event.hlt_pf_rho_reg = -99.

        return True
