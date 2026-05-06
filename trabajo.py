class PrintTask:

    def __init__(self, task_id, pages, arrival_time):
        self.task_id = task_id
        self.pages = pages
        self.arrival_time = arrival_time
        self.start_time = None
  
        self.wait_time = None

    def __repr__(self):
        return f"PrintTask(id={self.task_id!r}, pages={self.pages}, arrival={self.arrival_time})"
