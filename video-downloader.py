from pytube import YouTube
from flask import Flask, render_template, request, send_file

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/result', methods=['POST', 'GET'])
def result():
    if request.method == 'POST':
        result = request.form['url']
        query = YouTube(result)
        videoFilter = query.streams.filter(progressive=True)
        audioFilter = query.streams.filter(adaptive=True, only_audio=True)
        return render_template('result.html', result=result, videoFilter=videoFilter, audioFilter=audioFilter)
    return render_template('index.html')


@app.route('/download_audio', methods=['POST'])
def download_audio():
    if request.method == 'POST':
        audio_tag = request.form['audio-tag']
        query = request.form['query']
        selected_file = YouTube(query)
        selected_file.streams.get_by_itag(audio_tag).download(output_path='DownloadedFiles', filename='your file')
        return send_file("DownloadedFiles/your file.mp4", mimetype='audio/mp4', as_attachment=True)
    return render_template('index.html')


@app.route('/download_video', methods=['POST'])
def download_video():
    if request.method == 'POST':
        video_tag = request.form['video-tag']
        query = request.form['query']
        selected_file = YouTube(query)
        selected_file.streams.get_by_itag(video_tag).download(output_path='DownloadedFiles', filename='your file')
        return send_file("DownloadedFiles/your file.mp4", mimetype='video/mp4', as_attachment=True)
    return render_template('index.html')


@app.errorhandler(500)
def server_error(error):
    return render_template('errorpage.html'), 500


@app.errorhandler(400)
def bad_request_error(error):
    return render_template('errorpage.html'), 400


if __name__ == '__main__':
    app.run()
