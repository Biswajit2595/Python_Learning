class QueueUsingStack:
    def __init__(self):
        self.stack1=[]
        self.stack2=[]
        
    def enqueue(self,value):
        self.stack1.append(value)
        
    def dequeue(self):
        if not self.stack2:
            if not self.stack1:
                return None
            while self.stack1:
                self.stack2.append(self.stack1.pop())
        return self.stack2.pop()
    
queue = QueueUsingStack()
output = []

output.append(queue.enqueue(1))
output.append(queue.enqueue(2))
output.append(queue.dequeue())
output.append(queue.enqueue(3))
output.append(queue.dequeue())
output.append(queue.dequeue())

filtered_output = [str(item) for item in output if item is not None]
print(", ".join(filtered_output))

# print(", ".join(str(item) for item in output))