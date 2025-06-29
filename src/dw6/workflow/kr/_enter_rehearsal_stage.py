import sys

def _enter_rehearsal_stage(self, exception):
    print("--- Governor: Entering Rehearsal stage for deep reflection. ---", file=sys.stderr)
    self._create_red_flag_requirement(exception)
    self.state.set("PreviousStage", self.current_stage)
    self.state.set("CurrentStage", "Rehearsal")
    self.state.save()
    self.current_stage = "Rehearsal"
