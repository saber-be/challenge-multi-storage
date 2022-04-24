from stack.CustomExceptions import EmptyStackException,NoneElementException

class Element:
	def __init__(self, value):
		if value is None:
			raise NoneElementException()
		self.value = value
		self.next = None

class Stack:
	_size : int = 0
	def __init__(self):
		self.head = Element("head")
		self._size = 0

	def __str__(self):
		""" String representation of the stack """
		cur = self.head.next
		out = ""
		while cur:
			out += str(cur.value) + "->"
			cur = cur.next
		return out[:-2]

	def size(self) -> int:
		"""Returns an integer representing the total number of items in the stack."""
		return self._size

	def push(self, value):
		"""
		Pushes the element onto the top of the stack.
		Throws a custom NullElementException if the supplied element is null.
		"""
		node = Element(value)
		node.next = self.head.next
		self.head.next = node
		self._size += 1

	# Remove a value from the stack and return.
	def pop(self):
		"""
		Removes the top element from the stack and returns its value.
		Throws a custom EmptyStackException if the stack is empty when this method is called.
		"""
		if self.empty():
			raise EmptyStackException("Popping from an empty stack")
		remove = self.head.next
		self.head.next = self.head.next.next
		self._size -= 1
		return remove.value

	def peek(self):
		"""
		Retrieves the top element from the stack without removing it, and returns its value.
		Throws a custom EmptyStackException if the stack is empty when this method is called.
		"""
		if self.empty():
			raise EmptyStackException("Peeking from an empty stack")
		return self.head.next.value

	def empty(self) -> bool:
		"""Tests whether the stack is empty."""
		return self.size() == 0


# Driver Code
if __name__ == "__main__": # pragma: no cover
	stack = Stack()
	stack.push(None)
	for i in range(1, 11):
		stack.push(i)
	print(f"Stack: {stack}")

	for _ in range(1, 6):
		remove = stack.pop()
		print(f"Pop: {remove}")
	print(f"Stack: {stack}")
