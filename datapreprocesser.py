from os import getcwd, mkdir, listdir
from shutil import rmtree
from pathlib import Path
from threading import Lock

from customtools import CheckFile, Timer
from threadmanager import ThreadManager

from PIL import Image
import cv2

import numpy as np
import pandas as pd

# from numba import jit, cuda
# import cython

data = dict()


@CheckFile
def _GetResolution(videoPath: str) -> tuple:
	videoCapture = cv2.VideoCapture(videoPath)

	width = int(videoCapture.get(cv2.CAP_PROP_FRAME_WIDTH))
	height = int(videoCapture.get(cv2.CAP_PROP_FRAME_HEIGHT))

	return width, height


def _GetRelatedFileInfo(videoPath: str) -> tuple[str, str]:
	videoName = videoPath.split('/')[-1].split('.')[0]
	folder = getcwd().replace('\\', '/') + f"/Data/Frames/{videoName}"

	return folder, videoName


@CheckFile
def _GetFiles(folder: str) -> list:
	return [f"{folder}/{file}" for file in listdir(folder)]


@CheckFile
def _ExtractFrames(videoPath: str, fileType: str):
	videoCapture = cv2.VideoCapture(videoPath)
	success, frame = videoCapture.read()
	count = 0

	folder, videoName = _GetRelatedFileInfo(videoPath)

	if Path(folder).exists():  # Removing old frames.
		rmtree(folder)
	mkdir(folder)

	while success:
		cv2.imwrite(f"Data/Frames/{videoName}/%d.{fileType}" % count, frame)
		success, frame = videoCapture.read()
		count += 1
	print(f"VIDEO: {videoPath}, TOTAL FRAMES PROCESSED: {count}.")


@CheckFile
def _ExtractPixels(framePath: str) -> np.array:
	image = Image.open(framePath)
	output = np.array(image)  # This gets called ~9 billion times. Can we speed it up?

	return output


@CheckFile
def _LoadVideo(videoPath: str) -> tuple[list, str]:
	print(f"LOADING '{videoPath}'.")

	folder, videoName = _GetRelatedFileInfo(videoPath)

	videoData = list()

	frames = _GetFiles(folder)
	# resolution = GetResolution(videoPath)

	for index, frame in enumerate(frames):
		print(f"VIDEO: {videoPath}, FRAME {index}/{len(frames)}")

		frameData = _ExtractPixels(frame)
		videoData.append(frameData)
	print(f"LOADED '{videoPath}'.")
	return videoData, videoName


def _ThreadVideoLoader(threadLock: Lock, videoPath: str):
	global data

	videoData, videoName = _LoadVideo(videoPath)

	with threadLock:
		data[videoName] = videoData


def VideoToFrames(location: str):
	videos = _GetFiles(location)

	for video in videos:
		_ExtractFrames(video, 'png')


def GetFrameData(location: str, threadLimit: int) -> dict:
	global data

	videos = _GetFiles(location)
	threadManager = ThreadManager(threadLimit=threadLimit,  # 128
									dataQueue=videos,
									function=_ThreadVideoLoader,
									lock=Lock())
	threadManager.Start()

	return data


def GetCSVData(location: str) -> pd.DataFrame:
	df = pd.read_csv(location)

	del df['Notes'], df['Weight_class']

	return df


def SortData(frameData: dict, csv: pd.DataFrame) -> pd.DataFrame:
	frameDF = pd.DataFrame(list(frameData.items()), columns=['Title', 'Frames'])  # At this point we have 2 versions of the frames. Should something be done regarding RAM?

	sortedCsv = csv.merge(frameDF,
							how='inner',
							left_on='Title',
							right_on='Title',
							validate="one_to_one")

	return sortedCsv


if __name__ == '__main__':  # 'Data/Frames'
	# VideoToFrames('Data/Frames')

	# out = GetFrameData('Data/Frames')
	# print(f"DATA: {out}")

	out = GetCSVData('Data/Data.csv')
	print(out)
