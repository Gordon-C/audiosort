import os, shutil, mutagenx.easyid3, mutagenx.flac, mutagenx.easymp4

global viableExtensions, failedFiles
failedFiles = []
viableExtensions = ('.mp3', '.flac', '.m4a')

def sortAudioFiles():
	#get the directories from the user
	userInput = getDirs()
	indir = userInput[0]
	outdir = userInput[1]
	#gets all music files in all subdirectories with extensions in viableExtensions
	musicFiles = []
	for (path, dirs, files) in os.walk(indir):
		musicFiles += [(path,f) for f in files if os.path.isfile(os.path.join(path,f)) and os.path.splitext(os.path.join(path,f))[1] in viableExtensions]	
	#sorts music files into directories in this format: \artist\album\songfile
	for f in musicFiles:
		src = os.path.join(f[0],f[1])
		try:
			dst = os.path.join(outdir, getInfo(os.path.join(f[0],f[1]), 'artist'), getInfo(os.path.join(f[0],f[1]), 'album'))
			placeFile(src, dst)
		except:
			failedFiles.append(src)
	if failedFiles != []:
		print("The following files failed and music be moved manually")
		for f in failedFiles:
			print(f)
	print("Completed! Press enter to close.")
	input()

def getDirs():
	print("Enter the source directory below:")
	indir = input('> ')
	print("Enter the destination directory below (must be empty and not a sub-directory of the source directory):")
	outdir = input('> ')
	return (indir, outdir)

def getInfo(f, infoType):
	#gets the mutagen object and accesses the specified info, and returns that after replacing all characters that the windows filesystem does not allow in directory names
	return getFileObject(f)[infoType][0].replace('/', '').replace('\\', '').replace(':', '').replace('?', '').replace('"', '').replace('<', '').replace('>', '').replace('|', '')

def getFileObject(f):
	fileExt = os.path.splitext(f)[1]
	if fileExt == '.mp3': return mutagenx.easyid3.EasyID3(f)
	elif fileExt == '.flac': return mutagenx.flac.FLAC(f)
	elif fileExt == '.m4a': return mutagenx.easymp4.EasyMP4(f)
		
def placeFile(src, dst):
	if os.path.exists(dst):
		shutil.copy2(src, dst)
	else:
		os.makedirs(dst)
		shutil.copy2(src, dst)
		
if __name__ == "__main__":
	sortAudioFiles()
