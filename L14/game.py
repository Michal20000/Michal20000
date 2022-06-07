from globals import *
from head import Head
import threading


class GameRoom:

	def __init__(self, client):
		self.game = uuid()
		self.running = True
		self.clientH = clients[client]
		self.clientH._game(self.game)
		self.clientG = None
		self.board = list()
		waiting_rooms[self.game] = self
		# todo: joinH, joinG

	def join(self, client):
		self.clientG = clients[client]
		self.clientG._game(self.game)
		waiting_rooms.pop(self.game, None)
		during_game_rooms[self.game] = self
		thread = threading.Thread(target = self.run)
		thread.start()

	def leave(self, client):
		if self.clientH is not None and self.clientG is not None:
			self.running = False
			during_game_rooms.pop(self.game, None)

			if self.clientH.client == client:
				self.clientG._wins(1)
				self.clientH._losses(1)
				# todo: clientG wins
				self.clientH._game()
				self.clientG._game()

			elif self.clientG.client == client:
				self.clientH._wins(1)
				self.clientG._losses(1)
				# todo: clientH wins
				self.clientH._game()
				self.clientG._game()

		elif self.clientH is not None:
			waiting_rooms.pop(self.game, None)
			self.clientH._game()

	def run(self):
		self.clientH._direction()
		self.clientG._direction()

		for i in range(0, 20):
			self.board.append(list())
			for j in range(0, 20):
				self.board[i].append(0)

		headH = Head()
		headH.indexX = 1
		headH.indexY = 1
		headG = Head()
		headG.indexX = 18
		headG.indexY = 18

		foods = list()

		# todo: sleep some time

		while self.board[headH.indexX][headH.indexY] not in [HOST_NODE, GUEST_HEAD, GUEST_NODE] and self.board[headG.indexX][headG.indexY] not in [HOST_HEAD, HOST_NODE, GUEST_NODE] and self.running:
			# todo: sleep some time

			if self.clientH.direction == DIRECTION_LEFT:
				headH.move(-1, 0)
			elif self.clientH.direction == DIRECTION_UPWARD:
				headH.move(0, -1)
			elif self.clientH.direction == DIRECTION_RIGHT:
				headH.move(1, 0)
			elif self.clientH.direction == DIRECTION_DOWNWARD:
				headH.move(0, 1)

			if self.clientG.direction == DIRECTION_LEFT:
				headG.move(-1, 0)
			elif self.clientG.direction == DIRECTION_UPWARD:
				headG.move(0, -1)
			elif self.clientG.direction == DIRECTION_RIGHT:
				headG.move(1, 0)
			elif self.clientG.direction == DIRECTION_DOWNWARD:
				headG.move(0, 1)

			if self.board[headH.indexX][headH.indexY] == FOOD:
				headH.attach()
			if self.board[headG.indexX][headG.indexY] == FOOD:
				headG.attach()
			# todo: check maybe something else
			# todo: if it is some action
			self.generate(headH, headG, foods)
			# todo: emit to room


		# todo: someone wins
		if self.running:
			self.clientH._game()
			self.clientG._game()
			during_game_rooms.pop(self.game, None)
		print("Game is finished!")


		# todo: running update
		# todo: rooms-list update
		# todo: results update
		# todo: client-game is None


		# todo: join when 0 create-game  -- Wait
		# todo: join when 1 join-game -- Start Game
		# todo: leave when 1 waiting-game -- Delete Room
		# todo: leave when 2 during-game -- Lose Game
		# todo: room is id or pointer?
		# todo: loop checks if someone left

	def generate(self, headH, headG, foods):
		for i in range(0, 20):
			for j in range(0, 20):
				self.board[i][j] = 0
		for food in foods:
			self.board[food.indexX][food.indexY] = FOOD

		self.board[headH.indexX][headH.indexY] = HOST_HEAD
		self.board[headG.indexX][headG.indexY] = GUEST_HEAD

		buffer = headH.node
		while buffer.node is not None:
			self.board[buffer.indexX][buffer.indexY] = HOST_NODE
			buffer = buffer.node
		buffer = headG.node
		while buffer.node is not None:
			self.board[buffer.indexX][buffer.indexY] = GUEST_NODE
			buffer = buffer.node

	def __repr__(self):
		return F"<GameRoom game: {self.game} host: {self.clientH}, guest: {self.clientG}>"
