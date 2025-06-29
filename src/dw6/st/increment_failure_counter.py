def increment_failure_counter(self, stage, counter_name="default"):
    key = f"FailureCounters.{stage}.{counter_name}"
    current_value = self.get_failure_counter(stage, counter_name)
    new_value = current_value + 1
    self.set(key, new_value)
    self.save()
    print(f"--- Governor: Failure counter {stage}.{counter_name} incremented to {new_value}. ---")
    return new_value
