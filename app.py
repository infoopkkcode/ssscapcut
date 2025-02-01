from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)

CORS(app, resources={r"/process-link": {"origins": ["https://humbletricks.com", "https://ssscapcut.pro", "https://api.ssscapcut.pro"]}})

@app.route('/process-link', methods=['POST'])
def process_link():
    domain = request.headers.get('Origin')
    link = request.json.get('link')

    # Handling request from https://ssscapcut.pro
    if domain == "https://ssscapcut.pro":
        try:
            from cc import get_download_link
            download_link = get_download_link(link)
            if download_link:
                return jsonify({'download_link': download_link})
        except ImportError:
            pass


    # Handling requests from other domains
    else:
        try:
            import online
            app_info = online.get_app_info(link)
            if app_info:
                return jsonify(app_info)
        except ImportError:
            pass

    return jsonify({'error': 'Failed to process the request or unsupported domain'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
