from pytubefix import Playlist, YouTube
import csv  # newly imported to handle CSV file writing

playlist = Playlist("https://www.youtube.com/playlist?list=PLsGl9GczcgBs6TtApKKK-L_0Nm6fovNPk")

# Print out the list of video URLs
print("Number of videos in playlist:", len(playlist.video_urls))
for url in playlist.video_urls:
    print(url)

print("Number of videos in playlist:", len(playlist.video_urls))

# Open CSV file to save the info
with open("yt_links.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    # Write header: "YT Link" for the URL, "Texture Description" for the title
    writer.writerow(["YT Link", "Texture Description"])

    # Loop over video URLs, printing details and saving them to the CSV
    for video_url in playlist.video_urls:
        yt = YouTube(video_url)  # This makes a request per video
        print("Title:", yt.title)
        print("Link:", video_url)
        print("-" * 40)
        writer.writerow([video_url, yt.title])