import youtube_dl

link = [input("Enter Link: ")]
print(link)

format = input("Press 1 for High Quality Video\nPress 2 for Normal Video\nPress 3 for Audio only \n")
if format == '1':
    ydl = youtube_dl.YoutubeDL({'format':'bestvideo+bestaudio'})
    ydl.download(link)
    print("Done")

if format == '2':
    ydl = youtube_dl.YoutubeDL({'format':'mp4'})
    ydl.download(link)
    print("Done")

if format == '3':
    ydl = youtube_dl.YoutubeDL({'format':'bestaudio'})
    ydl.download(link)
    print("Done")


