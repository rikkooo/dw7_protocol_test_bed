def delete(self, key):
    if key in self.data:
        del self.data[key]
