from node import Node


class Head:

	def __init__(self):
		self.indexX = 0
		self.indexY = 0
		self.lastX = 0
		self.lastY = 0
		self.node = None

	def move(self, valueX, valueY):
		self.lastX = self.indexX
		self.lastY = self.indexY
		self.indexX += valueX
		self.indexY += valueY

		if self.node is not None:
			self.node.move(self.lastX, self.lastY)

	def attach(self):
		buffer = self.node
		while buffer.node is not None:
			buffer = buffer.node

		node = Node()
		node.indexX = buffer.lastX
		node.indexY = buffer.lastY
		buffer.node = node
