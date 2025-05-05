import os
import subprocess
from urllib.parse import parse_qs

SCRIPT_PATH = "./ytmusic.sh"  # Replace with the actual name
DOWNLOAD_DIR = "./downloaded"

def app(environ, start_response):
    method = environ['REQUEST_METHOD']

    if method == 'GET':
        response_body = """
            <html>
                <body>
                    <h2>Enter a YouTube URL to download audio</h2>
                    <form method="post">
                        <input type="text" name="input_text" placeholder="https://youtube.com/..." />
                        <button type="submit">Download MP3</button>
                    </form>
                </body>
            </html>
        """
        start_response("200 OK", [("Content-Type", "text/html")])
        return [response_body.encode("utf-8")]

    elif method == 'POST':
        try:
            size = int(environ.get('CONTENT_LENGTH', 0))
        except (ValueError):
            size = 0

        body = environ['wsgi.input'].read(size).decode('utf-8')
        post_data = parse_qs(body)
        user_input = post_data.get('input_text', [''])[0].strip()

        if not user_input:
            start_response('400 Bad Request', [('Content-Type', 'text/plain')])
            return [b"No input provided."]

        try:
            # 🔧 Call the script with the user input (YouTube URL)
            result = subprocess.run(
                [SCRIPT_PATH, user_input],
                capture_output=True,
                text=True,
                check=True
            )
            output_lines = result.stdout.strip().splitlines()
            downloaded_path = next((line for line in output_lines if line.endswith('.webm') or line.endswith('.mp3') or line.endswith('.m4a')), None)

            if not downloaded_path or not os.path.exists(downloaded_path):
                start_response('500 Internal Server Error', [('Content-Type', 'text/plain')])
                return [f"File not found or download failed.\n\n{result.stdout}".encode('utf-8')]

            # ✅ Serve the downloaded MP3 (or other audio format)
            with open(downloaded_path, 'rb') as f:
                file_data = f.read()

            headers = [
                ('Content-Type', 'audio/mpeg'),
                ('Content-Disposition', f'attachment; filename="{os.path.basename(downloaded_path)}"'),
                ('Content-Length', str(len(file_data)))
            ]
            start_response('200 OK', headers)
            return [file_data]

        except subprocess.CalledProcessError as e:
            start_response('500 Internal Server Error', [('Content-Type', 'text/plain')])
            return [f"Script error:\n{e.stderr}".encode('utf-8')]

    else:
        start_response('405 Method Not Allowed', [('Content-Type', 'text/plain')])
        return [b'Only GET and POST methods are allowed.']
