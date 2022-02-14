from datapreprocesser import VideoToFrames, GetFrameData, GetCSVData, SortData
from dataprocesser import Run


if __name__ == '__main__':
	frameData = GetFrameData('Data/Frames', 128)
	csvData = GetCSVData('Data/Data.csv')

	data = SortData(frameData, csvData)

	del frameData, csvData  # We're not going to use there anymore and they take up a lot of space.

	Run(data)
