from flask import Flask, request, jsonify, send_file, render_template
from pytube import YouTube
from moviepy.editor import VideoFileClip
import os
import uuid

app = Flask(__name__)

# グローバルな変数
DOWNLOAD_FOLDER = 'downloads'
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    url = request.form['url']
    format_type = request.form['format']
    
    try:
        yt = YouTube(url)
        video_stream = yt.streams.filter(progressive=True, file_extension='mp4').first()
        video_file = video_stream.download(output_path=DOWNLOAD_FOLDER, filename='video.mp4')
        
        if format_type == 'mp3':
            audio_clip = VideoFileClip(video_file).audio
            audio_file = os.path.join(DOWNLOAD_FOLDER, f'{uuid.uuid4()}.mp3')
            audio_clip.write_audiofile(audio_file)
            audio_clip.close()
            os.remove(video_file)
            return send_file(audio_file, as_attachment=True)
        
        elif format_type == 'wav':
            audio_clip = VideoFileClip(video_file).audio
            audio_file = os.path.join(DOWNLOAD_FOLDER, f'{uuid.uuid4()}.wav')
            audio_clip.write_audiofile(audio_file)
            audio_clip.close()
            os.remove(video_file)
            return send_file(audio_file, as_attachment=True)
        
        elif format_type == 'mp4':
            video_file_out = os.path.join(DOWNLOAD_FOLDER, f'{uuid.uuid4()}.mp4')
            os.rename(video_file, video_file_out)
            return send_file(video_file_out, as_attachment=True)
        
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/thumbnail', methods=['POST'])
def thumbnail():
    url = request.form['url']
    try:
        yt = YouTube(url)
        thumbnail_url = yt.thumbnail_url
        return jsonify({'thumbnail_url': thumbnail_url})
    except Exception as e:
        return jsonify({'error': str(e)})
    
@app.route('/video_info', methods=['POST'])
def video_info():
    url = request.form['url']
    try:
        yt = YouTube(url)
        info = {
            'thumbnail_url': yt.thumbnail_url,
            'title': yt.title
        }
        return jsonify(info)
    except Exception as e:
        return jsonify({'error': str(e)})


if __name__ == '__main__':
    app.run(debug=True)
