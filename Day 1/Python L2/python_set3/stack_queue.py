from queue import Queue

class StackUsingQueue:
    def __init__(self):
        self.queue = Queue()

    def push(self, value):
        # Add the new element to the queue
        self.queue.put(value)
        # Move all existing elements in the queue before the new element
        for _ in range(self.queue.qsize() - 1):
            self.queue.put(self.queue.get())

    def pop(self):
        if not self.queue.empty():
            return self.queue.get()
        else:
            return None

# Example usage:
stack = StackUsingQueue()
output = []

output.append(stack.push(1))
output.append(stack.push(2))
output.append(stack.pop())
output.append(stack.push(3))
output.append(stack.pop())
output.append(stack.pop())

print(output)
