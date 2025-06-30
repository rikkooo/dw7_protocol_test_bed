import sys
import traceback

def approve(self, needs_research=False, allow_failures=False):
    try:
        # Step 1: Get current stage and requirement details
        stage_being_approved = self.current_stage_name
        event_details = self.get_current_event_details()
        if not event_details:
            raise Exception("Could not load current event details.")
        # Default to 'Sherlock' if type is not specified. This ensures all legacy
        # requirements are reviewed before execution.
        requirement_type = event_details.get('type', 'Sherlock')

        # Step 2: Perform validation for the current stage
        if hasattr(self.stage_module, 'validate'):
            if not self.stage_module.validate():
                raise Exception(f"Validation failed for stage {stage_being_approved}.")

        # Step 3: Define the final stage for each requirement type
        completion_stages = {
            'Sherlock': 'Researcher',
            'Execution': 'Validator',
            'Formalization': 'Deployer'
        }

        # Step 4: Advance the stage. The kernel will handle completion logic.
        # The 'needs_research' flag can be triggered by the user OR by the requirement type.
        should_research = needs_research or (requirement_type == 'Sherlock' and stage_being_approved == 'Engineer')
        self.kernel.current_event = event_details
        self.kernel.advance_stage(needs_research=should_research)
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
