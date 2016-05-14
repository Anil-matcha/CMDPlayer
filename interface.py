import subprocess, sys, random, os

videoformats = [".mp4", ".MP4", ".avi", ".MPG", ".mpg", ".flv", ".mkv"]	
audioformats = [".mp3"]

def removebracket(list, br, brinv):
    bracketlist = []
    for d in list:
        if("(" in d and ")" in d):
            subbracketlist1 = d.split(br)
            for s in subbracketlist1:
                bracketlist.extend(s.split(brinv))
        else:
            bracketlist.append(d)
    list = [x for x in bracketlist if x!=""]
    return list
	
def removechar(list, char):
    charlist = []
    for s in list:
        _sublist = s.split(char)
        for sub in _sublist:
            charlist.append(sub)
    return charlist
	
def splitall(str):
    returnlist = []
    spacelist = str.split()
    _list = removechar(spacelist, "_")
    dotlist = removechar(_list, ".")    			
    bracketlist = removebracket(dotlist, "(", ")")
    flbracketlist = removebracket(bracketlist, "{", "}")
    sqbracketlist = removebracket(flbracketlist, "[", "]")
    return sqbracketlist

def getdiff(str1, str2):
    count = 0
    for i in range(len(str1)):
        if(str1[i] in str2):
            str2 = str2.replace(str1[i],"",1)
        else:
            count+=1
    count+=len(str2)
    return count
	
def strdiff(str1, str2):
    if(len(str1)-len(str2)>3):
        return 10000
    else:
        return getdiff(str1, str2)
			
def compare_strings(filename, searchname, song):
    filename = filename.lower()
    searchname = searchname.lower() 
    if(song):
        filename = filename.replace(".mp3", "")
    else:
        for v in videoformats:
            if(v in filename):
                filename = filename.replace(v, "")
    filearray = splitall(filename)
    searcharray = splitall(searchname)
    count = 0
    for s in searcharray:
        min = 10000
        for f in filearray:
            if(strdiff(s,f)<=int(2*len(s)/4)):
                if(min > strdiff(s,f)):
                    min = strdiff(s,f)
        if(min!=10000):
            count += 2*(3-min)
    return count


def play_file(str, song):
    counts = []
    if(song):
        for s in songsnames:
            counts.append(compare_strings(s, str, song))
    else:
        for v in videosnames:
            counts.append(compare_strings(v, str, song))
    max = 0
    index = -1
    for i in range(len(counts)):
        if(counts[i]>max):
            max = counts[i]
            index = i
    print(counts.count(max))
    return index


	
songs = []
videos = []
songsnames = []
videosnames = []

def add_all_files(list, loc):
    for l in list:
        if(os.path.isdir(loc+"\\"+l)):
            process = subprocess.Popen(['ls', loc+"\\"+l], stdout=subprocess.PIPE)
            out, err = process.communicate()
            list = out.decode("utf-8").split("\n")
            list.pop()
            list = out.decode("utf-8").split("\n")
            list.pop()
            add_all_files(list, loc+"\\"+l)
        elif(os.path.isfile(loc+"\\"+l)):
            if any(word in l for word in videoformats):
               videosnames.append(l)
               videos.append(loc+"\\"+l)			
            elif any(word in l for word in audioformats):			
               songsnames.append(l)
               songs.append(loc+"\\"+l)

locations = ["location1", "location2", "location3", "location4", "location5"]


vlcpath = 'C:\\Program Files (x86)\\VideoLAN\\VLC\\vlc.exe'

for loc in locations:
    process = subprocess.Popen(['ls', loc], stdout=subprocess.PIPE)
    out, err = process.communicate()
    list = out.decode("utf-8").split("\n")
    list.pop()
    add_all_files(list, loc)
	
run = True	
while run:
    print("Enter a command")
    s = input()
    if("random" in s and "song" in s):
        if(process!=None):
            process.terminate()
        i = random.randint(0,len(songs)-1)
        process = subprocess.Popen([vlcpath, songs[i]])
    elif("random" in s and "video" in s):
        if(process!=None):
            process.terminate()
        i = random.randint(0,len(videos)-1)
        process = subprocess.Popen([vlcpath, videos[i]])
    elif("play" in s and "song" in s):
        cmd = s.split()
        songname = " ".join(cmd[2:])	
        if(process!=None):
            process.terminate()
        i = play_file(songname, True)
        if(i==-1):
            print("Can't find any song")
        else:
            process = subprocess.Popen([vlcpath, songs[i]])   
    elif("play" in s and "video" in s):
        cmd = s.split()
        videoname = " ".join(cmd[2:])	
        if(process!=None):
            process.terminate()
        i = play_file(videoname, False)
        if(i==-1):
            print("Can't find any video")
        else:
            process = subprocess.Popen([vlcpath, videos[i]]) 
    elif("exit" in s):
        run = False