from os import listdir

from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC

import numpy as np
import pandas as pd


def Homogenize(input: list) -> np.array:  # Homogenizing nested lists
	maxLength = max([len(x) for x in input])

	output = list()

	for item in input:
		lengthDif = maxLength - len(item)

		zeroes = [0] * lengthDif
		newItem = np.append(item, zeroes)
		print(len(newItem))
		output.append(newItem)
	return input


def Run(trainData: pd.DataFrame, testData: pd.DataFrame):
	model = SVC()

	# trainFrames = np.array([d.frames for d in trainData['Frames']], dtype=int)
	# testFrames = np.array([d.frames for d in testData['Frames']], dtype=int)

	trainFrames = Homogenize([d.frames for d in trainData['Frames']])
	testFrames = Homogenize([d.frames for d in testData['Frames']])

	model.fit(trainFrames, trainData['Outcome'])

	pred = model.predict(testFrames)

	acc = accuracy_score(pred, testData['Outcome'])
	print(acc)

	print(classification_report(testData['Outcome'], pred, zero_division=0))


if __name__ == '__main__':
	pass
