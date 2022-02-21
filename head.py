from datapreprocesser import VideoToFrames, GetFrameData, GetCSVData, SortData, SplitData
from dataprocesser import Run

from time import sleep

styles = ['C', 'S']


if __name__ == '__main__':
	# VideoToFrames('Data/Clips')

	frameDataGenerator = GetFrameData(location='Data/Frames',  # Load empties here?
								threadLimit=128,
								splits=5)
	csvData = GetCSVData('Data/Data.csv')

	for frameData in frameDataGenerator:
		data = SortData(frameData, csvData)

		# del frameData, csvData  # We're not going to use these anymore and they take up a lot of space.

		for style in styles:
			for indices in SplitData(titles=data[data['Style'] == style]['Title'],
											splits=5,
											tests=5,  # Can't use SmallData.
											testSize=.3):
				Run(trainData=data[data['Title'].isin(indices[0])],
					testData=data[data['Title'].isin(indices[1])])
