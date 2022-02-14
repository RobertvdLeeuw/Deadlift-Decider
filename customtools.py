from pathlib import Path
from time import time


def CheckFile(function):  # Requires the first argument (no keyword) to be  the filepath (str).
	def wrapper(*args, **kwargs):
		filePath = args[0]

		file = Path(filePath)

		if file.exists():
			'''if file.is_file:
				output = function(*args, **kwargs)

				return output
			else:
				print(f"ERROR: '{filePath}' is not a file.")'''

			output = function(*args, **kwargs)
			return output
		else:
			print(f"ERROR: '{filePath}'not found.")

	return wrapper


def Timer(function):
	def wrapper(*args, **kwargs):
		preTime = time()

		output = function(*args, **kwargs)

		postTime = time()

		print(f"TIME: {postTime - preTime}.")
		return output

	return wrapper
