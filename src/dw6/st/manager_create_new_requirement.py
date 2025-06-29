def create_new_requirement(self, requirement_id, title, description, acceptance_criteria, event_type="Standard", priority="Normal"):
    self.kernel.create_new_requirement(requirement_id, title, description, acceptance_criteria, event_type, priority)
