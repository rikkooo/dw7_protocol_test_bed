import sys
import traceback

def approve(self, needs_research=False, allow_failures=False):
    try:
        # Validate the current stage before advancing.
        # The stage module's `validate` method should return True on success
        # and False on failure, which we convert to an exception.
        if hasattr(self.stage_module, 'validate'):
            if not self.stage_module.validate():
                # This exception will be caught and handled as a failure.
                raise Exception(f"Validation failed for stage {self.current_stage_name}.")

        # If execution is successful, advance to the next stage
        self.kernel.advance_stage(needs_research=needs_research)
        print(f"--- Governor: Stage '{self.state.get('CurrentStage')}' approved and advanced. ---")
        self.state.save()

    except Exception as e:
        if allow_failures:
            print(f"--- Governor: Stage execution failed, but failure was allowed. Error: {e} ---", file=sys.stderr)
            self.kernel.advance_stage(needs_research=needs_research)
        else:
            print(f"--- Governor: Stage execution failed. Error: {e} ---", file=sys.stderr)
            traceback.print_exc(file=sys.stderr)
            self.kernel._handle_failure(e)
