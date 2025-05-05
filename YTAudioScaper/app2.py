import os
import subprocess
from urllib.parse import parse_qs

MP3_FILE_PATH = "./your_audio.mp3"  # Adjust as needed
SCRIPT_PATH = "./process.sh"        # Your local Bash script

def app(environ, start_response):
    method = environ['REQUEST_METHOD']

    if method == 'GET':
        response_body = """
            <html>
                <body>
                    <h2>Enter something to process and download MP3</h2>
                    <form method="post">
                        <input type="text" name="input_text" />
                        <button type="submit">Run & Download</button>
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
        user_input = post_data.get('input_text', [''])[0]

        # 🔧 Run Bash script with input
        try:
            result = subprocess.run(
                [SCRIPT_PATH, user_input],
                capture_output=True,
                text=True,
                check=True
            )
            print("Script output:", result.stdout)
        except subprocess.CalledProcessError as e:
            start_response('500 Internal Server Error', [('Content-Type', 'text/plain')])
            return [f"Script failed: {e.stderr}".encode('utf-8')]

        # 🎵 Serve MP3 file
        if os.path.exists(MP3_FILE_PATH):
            with open(MP3_FILE_PATH, 'rb') as f:
                mp3_data = f.read()

            headers = [
                ('Content-Type', 'audio/mpeg'),
                ('Content-Disposition', f'attachment; filename="{os.path.basename(MP3_FILE_PATH)}"'),
                ('Content-Length', str(len(mp3_data)))
            ]
            start_response('200 OK', headers)
            return [mp3_data]
        else:
            start_response('404 Not Found', [('Content-Type', 'text/plain')])
            return [b'MP3 file not found.']

    else:
        start_response('405 Method Not Allowed', [('Content-Type', 'text/plain')])
        return [b'Only GET and POST methods are allowed.']
