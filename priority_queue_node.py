class PriorityQueueNode:
    def __init__(self, priority, state):
        self.priority = priority
        self.state = state

    def __lt__(self, other):
        return self.priority < other.priority

    def __gt__(self, other):
        return self.priority > other.priority

    def __eq__(self, other):
        return self.state.board.grid == other.state.board.grid
