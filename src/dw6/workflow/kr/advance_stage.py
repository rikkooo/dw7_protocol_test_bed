from datetime import datetime, timezone

def advance_stage(self, needs_research=False):
    """
    Advances the workflow to the next stage based on the current stage and event type.
    This method implements the core state machine logic of the DW8 protocol,
    including handling for the Protocol Update Interrupt.
    """
    # --- Protocol Update Interrupt Handling ---
    if self.state.get("is_protocol_update"):
        print("--- Governor: Protocol Update Interrupt detected. Engaging specialized workflow. ---")
        if self.current_stage == "Engineer":
            next_stage = "Coder"
        elif self.current_stage == "Coder":
            next_stage = "Validator"
        elif self.current_stage == "Validator":
            # A successful validation of a protocol update completes the cycle.
            next_stage = "Engineer"
        else:
            # This case should not be reached in a protocol update cycle.
            # It indicates a state corruption or manual override.
            raise Exception(f"Invalid stage {self.current_stage} for Protocol Update workflow.")
    else:
        # --- Standard Workflow Logic ---
        if self.current_stage == "Rehearsal":
            next_stage = self.state.get("PreviousStage", "Engineer")
            self.state.delete("PreviousStage")  # Clean up state
        elif self.current_stage == "Engineer":
            next_stage = "Researcher" if needs_research else "Coder"
        elif self.current_stage == "Researcher":
            next_stage = "Coder"
        elif self.current_stage == "Coder":
            next_stage = "Validator"
        elif self.current_stage == "Validator":
            next_stage = "Deployer" if self.current_event and self.current_event.get("type") == "Deployment" else "Engineer"
        elif self.current_stage == "Deployer":
            next_stage = "Engineer"
        else:
            raise Exception(f"Unknown stage transition from {self.current_stage}")

    # Log stage transition timings
    timestamp = datetime.now(timezone.utc).isoformat()
    stats = self.state.get("statistics", {})
    req_id = self.current_event.get("id") if self.current_event else None

    if req_id:
        stats.setdefault("timings", {}).setdefault(req_id, {})
        
        # Log end time for current stage and calculate duration
        current_stage_stats = stats["timings"][req_id].setdefault(self.current_stage, {})
        current_stage_stats["end_time"] = timestamp

        if "start_time" in current_stage_stats:
            start = datetime.fromisoformat(current_stage_stats["start_time"])
            end = datetime.fromisoformat(timestamp)
            duration_seconds = (end - start).total_seconds()
            current_stage_stats["duration_seconds"] = round(duration_seconds, 2)

        # Log start time for next stage
        stats["timings"][req_id].setdefault(next_stage, {})["start_time"] = timestamp
        self.state.set("statistics", stats)

    self._reset_failure_counters(self.current_stage)

    # If we are transitioning back to Engineer, it means a cycle is complete.
    if next_stage == "Engineer":
        print("--- Governor: Requirement cycle complete. ---")
        self.state.increment("CycleCounter")
        self._advance_requirement_pointer()
        self._perform_context_refresh()

    # If we are entering the Coder stage, record the starting commit hash.
    if next_stage == "Coder":
        from ...git_handler import get_latest_commit_hash
        commit_hash = get_latest_commit_hash()
        if commit_hash:
            self.state.set("CoderStartCommitSHA", commit_hash)
            print(f"--- Governor: Coder stage starting at commit {commit_hash[:7]}. ---")

    self.state.set("CurrentStage", next_stage)
    self.state.save()
    print(f"--- Governor: Stage advanced from {self.current_stage} to {next_stage}. ---")
    self.current_stage = next_stage  # Update the kernel's internal state
