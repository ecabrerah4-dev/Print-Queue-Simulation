class Printer:

    def __init__(self, seconds_per_page):
        self.seconds_per_page = seconds_per_page
        self._busy_until = None
        self._current_task = None

    def is_busy(self, current_time):
        if self._busy_until is None:
            return False
        return current_time < self._busy_until

    def start_printing(self, task, current_time):
        task.start_time = current_time
        duration = task.pages * self.seconds_per_page
        self._busy_until = current_time + duration
        self._current_task = task

    def finish_if_due(self, current_time):
        if self._busy_until is not None and current_time >= self._busy_until:
            finished = self._current_task
            self._busy_until = None
            self._current_task = None
            return finished
        return None

    def get_busy_until(self):
        return self._busy_until