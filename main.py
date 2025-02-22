import yt_dlp
import os
from urllib.parse import urlparse, parse_qs

base_path = os.getcwd()
new_folder = 'videos'
new_folder_path = os.path.join(base_path, new_folder)
os.makedirs(new_folder_path, exist_ok=True)

def sanitize_youtube_url(url):
    parsed = urlparse(url)
    if parsed.hostname == 'youtu.be':
        video_id = parsed.path[1:] 
    else:
        query = parse_qs(parsed.query)
        video_id = query.get('v', [None])[0]
    
    return f'https://www.youtube.com/watch?v={video_id}' if video_id else url

def download_video(url):
    try:
        clean_url = sanitize_youtube_url(url)
        
        ydl_opts = {
            'outtmpl': os.path.join(new_folder_path, '%(title)s.%(ext)s'),
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'merge_output_format': 'mp4',
            'ignoreerrors': True,
            'quiet': False,
            'no_warnings': False,
            'progress_hooks': [lambda d: print_progress(d)],
            'cookiefile': 'cookies.txt',
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
                'Referer': 'https://www.youtube.com/',
            }
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            
            info = ydl.extract_info(clean_url, download=True)
            
            if info:
                print(f"\n✅ Successfully downloaded: {info['title']}")
                print(f"💾 Saved to: {os.path.join(new_folder_path, info['title'])}.mp4")
            else:
                print("🚨 Download failed")

    except Exception as e:
        print(f"🚨 Error: {str(e)}")

def print_progress(d):
    if d['status'] == 'downloading':
        progress = d.get('_percent_str', 'N/A')
        speed = d.get('_speed_str', 'N/A')
        eta = d.get('_eta_str', 'N/A')
        print(f"\r⏳ Downloading: {progress} | Speed: {speed} | ETA: {eta}", end='')

if __name__ == "__main__":
    link = input("🔗 Enter YouTube URL: ").strip()
    if link:
        download_video(link)
    else:
        print("❌ Invalid input.")
