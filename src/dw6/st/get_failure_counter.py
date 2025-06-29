def get_failure_counter(self, stage, counter_name="default"):
    key = f"FailureCounters.{stage}.{counter_name}"
    return int(self.get(key, 0))
