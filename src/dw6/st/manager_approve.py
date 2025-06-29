import sys
import traceback

def approve(self, needs_research=False, allow_failures=False):
    try:
        stage_being_approved = self.current_stage_name

        # Validate the current stage before advancing.
        if hasattr(self.stage_module, 'validate'):
            if not self.stage_module.validate():
                raise Exception(f"Validation failed for stage {stage_being_approved}.")

        # If validation is successful, advance to the next stage.
        self.kernel.advance_stage(needs_research=needs_research)
        
        # Get the new stage name for the log message.
        new_stage = self.state.get('CurrentStage')
        print(f"--- Governor: Stage '{stage_being_approved}' approved. Workflow advanced to '{new_stage}'. ---")
        self.state.save()

    except Exception as e:
        if allow_failures:
            print(f"--- Governor: Stage execution failed, but failure was allowed. Error: {e} ---", file=sys.stderr)
            self.kernel.advance_stage(needs_research=needs_research)
        else:
            print(f"--- Governor: Stage execution failed. Error: {e} ---", file=sys.stderr)
            traceback.print_exc(file=sys.stderr)
            self.kernel._handle_failure(e)
