import cv2 as cv
import numpy as np



def main():
	chess_games = [
		cv.imread("./chess-games/1.jpeg"),
		cv.imread("./chess-games/2.jpeg"),
		cv.imread("./chess-games/3.jpeg"),
		cv.imread("./chess-games/4.jpeg")

	]
	print(len(chess_games[0][0][0]))

	filename = 0
	for chess_game in chess_games:
		for begin_z in range(0, len(chess_game), 360):
			for begin_x in range(0, len(chess_game[0]), 360):

				image = np.ndarray((360, 360, 3))
				for i in range(begin_z, begin_z + 360):
					for j in range(begin_x, begin_x + 360):
						image[i - begin_z][j - begin_x][0] = chess_game[i][j][0]
						image[i - begin_z][j - begin_x][1] = chess_game[i][j][1]
						image[i - begin_z][j - begin_x][2] = chess_game[i][j][2]

				cv.imwrite("./chess-cards/" + str(filename) + ".png", image)
				filename = filename + 1



if __name__ == "__main__":
	main()
