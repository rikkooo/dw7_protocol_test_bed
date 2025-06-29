def increment(self, key):
    current_value = int(self.get(key, 0))
    new_value = current_value + 1
    self.set(key, new_value)
    self.save()
    return new_value
