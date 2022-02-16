from os import listdir

from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC

import numpy as np
import pandas as pd


def Run(trainData: pd.DataFrame, testData: pd.DataFrame):
	model = SVC()
	model.fit(trainData['Frames'], trainData['Outcome'])

	pred = model.predict(testData['Frames'])

	acc = accuracy_score(pred, testData['Outcome'])
	print(acc)

	print(classification_report(testData['Outcome'], pred, zero_division=0))


if __name__ == '__main__':
	pass
