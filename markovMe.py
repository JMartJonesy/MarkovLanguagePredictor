"""
	Predict DAT Word
	Jesse Martinez
	AI HW #6
"""
englishPairs = dict()
croatianPairs = dict()
firstLetterFreqs = [dict(), dict()]

blanky = "+"

def readFile(fileName, freqIndex, english = True):
	dictionary = croatianPairs
	firsty = firstLetterFreqs[0]
	if english:
		dictionary = englishPairs
		firsty = firstLetterFreqs[1]

	for line in open(fileName):
		splitty = line.strip().split()
		frequency = float(splitty[freqIndex])
		lookyWord = blanky + splitty[freqIndex - 1] + blanky
		for i in range(len(lookyWord) - 1):
			addMe = lookyWord[i] + lookyWord[i + 1]

			if addMe not in dictionary:
				dictionary[addMe] = [0, 0]

			dictionary[addMe][0] += frequency
			dictionary[addMe][1] += 1
			if addMe[0] not in firsty:
				firsty[addMe[0]] = [0, 0]
			firsty[addMe[0]][0] += frequency
			firsty[addMe[0]][1] += 1
				
	#Normalize
	for word, _ in dictionary.items():
		dictionary[word][0] /= firsty[word[0]][0]
		dictionary[word][1] /= firsty[word[0]][1]

def predictWord(word, weighted = False):
	englishProb = 1
	croatianProb = 1
	word = blanky + word + blanky
	for i in range(len(word) - 1):
		lookUpMe = word[i] + word[i + 1]
		if lookUpMe not in englishPairs and lookUpMe not in croatianPairs:
			englishProb *= 0
			croatianProb *= 0
		elif lookUpMe not in englishPairs:
			englishProb *= 0
			if weighted:
				croatianProb *= croatianPairs[lookUpMe][0]
			else:
				croatianProb *= croatianPairs[lookUpMe][1]
		elif lookUpMe not in croatianPairs:
			croatianProb *= 0
			if weighted:
				englishProb *= englishPairs[lookUpMe][0]
			else:
				englishProb *= englishPairs[lookUpMe][1]
		else:
			if weighted:
				englishProb *= englishPairs[lookUpMe][0]
				croatianProb *= croatianPairs[lookUpMe][0]
			else:
				englishProb *= englishPairs[lookUpMe][1]
				croatianProb *= croatianPairs[lookUpMe][1]
	
	return (englishProb, croatianProb)

def prettyPrediction(word):
	englishWeighted, croatianWeighted = predictWord(word, True)
	englishUnWeighted, croatianUnWeighted = predictWord(word, False)
	
	if englishUnWeighted > croatianUnWeighted:
		print("Unweighted prediction: English", englishUnWeighted, ">", croatianUnWeighted)
	else:
		print("Unweighted prediction: Croatian", croatianUnWeighted, ">", englishUnWeighted)

	if englishWeighted > croatianWeighted:
		print("Weighted prediction: English", englishWeighted, ">", croatianWeighted)
	else:
		print("Weighted prediction: Croatian", croatianWeighted, ">", englishWeighted)

if __name__ == "__main__":
	readFile("croatian.txt", 1, False)
	readFile("english.txt", 2, True)
	while(True):
		word = input("Input dat word:")
		prettyPrediction(word)
