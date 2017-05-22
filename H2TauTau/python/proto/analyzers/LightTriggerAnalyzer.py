from itertools import combinations

from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
from PhysicsTools.HeppyCore.utils.deltar import deltaR

import PhysicsTools.HeppyCore.framework.config as cfg


class LightTriggerAnalyzer(Analyzer):
    '''Access to trigger information, and trigger selection. The required
    trigger names need to be attached to the components.'''

    def declareHandles(self):
        super(LightTriggerAnalyzer, self).declareHandles()

        if hasattr(self.cfg_ana, 'triggerResultsHandle'):
            myhandle = self.cfg_ana.triggerResultsHandle
            self.handles['triggerResultsHLT'] = AutoHandle(
                (myhandle[0], myhandle[1], myhandle[2]),
                'edm::TriggerResults'
                )
        else:    
            trig_proc_name = 'HLT2' if 'reHLT' in self.cfg_comp.dataset else 'HLT'
            self.handles['triggerResultsHLT'] = AutoHandle(
                ('TriggerResults', '', trig_proc_name),
                'edm::TriggerResults'
                )


 
    def beginLoop(self, setup):
        super(LightTriggerAnalyzer,self).beginLoop(setup)

        self.triggerList     = self.cfg_comp.triggers
        self.vetoTriggerList = self.cfg_comp.vetoTriggers if hasattr(self.cfg_comp, 'vetoTriggers') else None

        self.counters.addCounter('LightTrigger')
        self.counters.counter('LightTrigger').register('All events')
        self.counters.counter('LightTrigger').register('Pass PU bin selection')
        self.counters.counter('LightTrigger').register('HLT')

        for trigger in self.triggerList:
            self.counters.counter('LightTrigger').register(trigger)


    def process(self, event):
        self.readCollections(event.input)
        
        event.run     = event.input.eventAuxiliary().id().run()
        event.lumi    = event.input.eventAuxiliary().id().luminosityBlock()
        event.eventId = event.input.eventAuxiliary().id().event()

        triggerBits   = self.handles['triggerResultsHLT'].product()
        names         = event.input.object().triggerNames(triggerBits)

        self.counters.counter('LightTrigger').inc('All events')

        if hasattr(self.cfg_ana, 'minPU') and hasattr(self.cfg_ana, 'maxPU'):
            if event.nPU < self.cfg_ana.minPU or event.nPU > self.cfg_ana.maxPU:
                return False
        self.counters.counter('LightTrigger').inc('Pass PU bin selection')

        trigger_passed = False

        if not self.triggerList:
            return True

        trigger_infos = []
        triggers_fired = []

        # which HLT paths are included?
        # for i in range(names.size()): print names.triggerName(i)
        # import pdb ; pdb.set_trace()
        
        for trigger_name in self.triggerList:
            index = names.triggerIndex(trigger_name)
            if index == len(triggerBits):
                continue

            if triggerBits.accept(index) and trigger_name in self.triggerList:
                self.counters.counter('LightTrigger').inc(trigger_name)            
                if trigger_name in self.triggerList:
                    trigger_passed = True
            triggers_fired.append(trigger_name)
            

        if self.cfg_ana.requireTrigger:
            if not trigger_passed:
                return False
        
        if self.cfg_ana.verbose:
            print 'run %d, lumi %d,event %d' %(event.run, event.lumi, event.eventId) , 'Triggers_fired: ', triggers_fired  

        self.counters.counter('LightTrigger').inc('HLT')        
        return True

    def __str__(self):
        tmp = super(LightTriggerAnalyzer,self).__str__()
        triglist = str(self.triggerList)
        return '\n'.join([tmp, triglist])

setattr(LightTriggerAnalyzer, 'defaultConfig', 
    cfg.Analyzer(
        class_object=LightTriggerAnalyzer,
        requireTrigger=True,
        # vetoTriggers=[],
    )
)
