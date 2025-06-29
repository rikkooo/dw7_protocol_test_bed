def reset_failure_counter(self, stage, counter_name="default"):
    key = f"FailureCounters.{stage}.{counter_name}"
    if self.get(key) is not None:
        self.set(key, 0)
        self.save()
        print(f"--- Governor: Failure counter {stage}.{counter_name} reset to 0. ---")
