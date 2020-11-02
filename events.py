class Events:
    """Class to add, track, delete, and manage events
    """
    def __init__(self, events: list):
        self.events = events
    
    def add_event(self, new_event: str):
        """Adds a new event to the events class
        """
        self.events.append(new_event)
