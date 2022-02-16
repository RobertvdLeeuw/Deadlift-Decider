from datapreprocesser import VideoToFrames, GetFrameData, GetCSVData, SortData, SplitData
from dataprocesser import Run

styles = ['C', 'S']


if __name__ == '__main__':
	# VideoToFrames('Data/Clips')

	frameDataGenerator = GetFrameData(location='Data/Frames',
								threadLimit=128,
								splits=10)
	csvData = GetCSVData('Data/Data.csv')
	for frameData in frameDataGenerator:
		data = SortData(frameData, csvData)
		print(f"DATA: {data}.")

		# del frameData, csvData  # We're not going to use these anymore and they take up a lot of space.

		for style in styles:
			for indices in SplitData(titles=data[data['Style'] == style]['Title'],
										splits=5,
										tests=5,
										testSize=.3):
				print(1)
				Run(trainData=data[data['Title'].isin(indices[0])],
					testData=data[data['Title'].isin(indices[1])])
