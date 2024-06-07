from flask import Flask, render_template, request, send_file
from pytube import YouTube
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    if request.method == 'POST':
        url = request.form['url']
        start_time = request.form['start_time']
        end_time = request.form['end_time']
        try:
            yt = YouTube(url)
            stream = yt.streams.get_highest_resolution()
            output_path = './downloads/'
            filename = stream.default_filename
            stream.download(output_path)
            original_file_path = os.path.join(output_path, filename)
            clipped_filename = f"{filename.split('.')[0]}_clip.mp4"
            clipped_file_path = os.path.join(output_path, clipped_filename)
            clip_command = f'ffmpeg -i "{original_file_path}" -ss {start_time} -to {end_time} -c copy "{clipped_file_path}"'
            os.system(clip_command)
            return send_file(clipped_file_path, as_attachment=True)
        except Exception as e:
            return str(e)

if __name__ == "__main__":
    app.run(debug=True)
