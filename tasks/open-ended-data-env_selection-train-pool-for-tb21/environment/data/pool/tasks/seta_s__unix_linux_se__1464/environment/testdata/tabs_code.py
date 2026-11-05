class Calculator:
	def __init__(self):
		self.memory = 0
		self.history = []

	def add(self, x, y):
		result = x + y
		self.history.append(result)
		return result

	def subtract(self, x, y):
		result = x - y
		self.history.append(result)
		return result

	def multiply(self, x, y):
		result = x * y
		self.history.append(result)
		return result

	def divide(self, x, y):
		if y == 0:
			raise ValueError("division by zero")
		result = x / y
		self.history.append(result)
		return result

	def get_history(self):
		return list(self.history)

	def clear(self):
		self.memory = 0
		self.history = []
