import heapq
import math
from priority_queue_node import PriorityQueueNode


class PriorityQueue:
    def __init__(self):
        self.queue = []

    def push(self, state):
        priority = state.f_value
        if state.goal_state():
            priority = -math.inf
        heapq.heappush(self.queue, PriorityQueueNode(priority, state))

    def pop(self):
        return heapq.heappop(self.queue)

    def is_empty(self):
        return len(self.queue) != 0
