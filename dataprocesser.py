# from dataclasses import dataclass
from os import listdir

from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC

import numpy as np
import pandas as pd


class DataSegment:
	x: list
	y: list


def Run(data: pd.DataFrame):
	train = DataSegment()
	test = DataSegment()

	train.x, train.y, test.x, test.y = train_test_split(data['Frames'], data['Red_flags'], test_size=.3, stratify=data['Red_flags'])
	del data

	# Not tested from here on out

	model = SVC()
	model.fit(train.x, train.y)

	pred = model.predict(test.x)

	acc = accuracy_score(pred, test.y)
	print(acc)

	print(classification_report(test.y, pred, zero_division=0))


if __name__ == '__main__':
	pass
