import os
from urllib.parse import parse_qs

MP3_FILE_PATH = "./your_audio.mp3"  # Replace with your actual file path

def app(environ, start_response):
    method = environ['REQUEST_METHOD']

    if method == 'GET':
        # Display form
        response_body = """
            <html>
                <body>
                    <h2>Enter something to download the MP3</h2>
                    <form method="post">
                        <input type="text" name="input_text" />
                        <button type="submit">Download</button>
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

        # -- Simulated logic with input --
        print(f"Received input from user: {user_input}")

        # -- Serve the MP3 file for download --
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
