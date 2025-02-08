from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

def get_video_info(url):
    ydl_opts = {'quiet': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return info

@app.route('/download', methods=['GET'])
def download_video():
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'Masukkan URL YouTube'}), 400

    try:
        info = get_video_info(url)
        formats = [
            {'format_id': f['format_id'], 'ext': f['ext'], 'resolution': f.get('height', 'audio'), 'url': f['url']}
            for f in info['formats']
        ]
        return jsonify({'title': info['title'], 'thumbnail': info['thumbnail'], 'formats': formats})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
