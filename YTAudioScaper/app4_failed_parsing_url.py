import os
import subprocess
from urllib.parse import parse_qs
from urllib.parse import quote

SCRIPT_PATH = "./your_script.sh"
DOWNLOAD_DIR = "./downloaded"

def app(environ, start_response):
    method = environ['REQUEST_METHOD']
    path = environ.get('PATH_INFO', '/')

    if method == 'GET' and path == '/':
        # Show initial form
        response_body = """
            <html>
                <body>
                    <h2>Enter YouTube URL</h2>
                    <form method="POST" action="/confirm">
                        <input type="text" name="input_text" placeholder="https://youtube.com/..." required />
                        <button type="submit">Continue</button>
                    </form>
                </body>
            </html>
        """
        start_response("200 OK", [("Content-Type", "text/html")])
        return [response_body.encode('utf-8')]

    elif method == 'POST' and path == '/confirm':
        # Extract submitted URL
        size = int(environ.get('CONTENT_LENGTH', 0))
        body = environ['wsgi.input'].read(size).decode('utf-8')
        post_data = parse_qs(body)
        user_input = post_data.get('input_text', [''])[0].strip()

        if not user_input:
            start_response('400 Bad Request', [('Content-Type', 'text/plain')])
            return [b"No input provided."]

        # Show confirmation page
        html = f"""
            <html>
                <body>
                    <p>Ready to download: <code>{user_input}</code></p>
                    <form method="POST" action="/download">
                        <input type="hidden" name="input_text" value="{quote(user_input)}" />
                        <button type="submit">Yes, download it</button>
                    </form>
                    <a href="/">Cancel</a>
                </body>
            </html>
        """
        start_response("200 OK", [("Content-Type", "text/html")])
        return [html.encode('utf-8')]

    elif method == 'POST' and path == '/download':
        # Extract again, then run the script
        size = int(environ.get('CONTENT_LENGTH', 0))
        body = environ['wsgi.input'].read(size).decode('utf-8')
        post_data = parse_qs(body)
        user_input = post_data.get('input_text', [''])[0]

        try:
            # Decode if quoted
            user_input = user_input.replace('+', ' ')

            # Run script with URL
            result = subprocess.run(
                [SCRIPT_PATH, user_input],
                capture_output=True,
                text=True,
                check=True
            )

            # Look for file path in stdout
            lines = result.stdout.strip().splitlines()
            downloaded_file = next((line for line in lines if line.startswith(DOWNLOAD_DIR) and os.path.exists(line.strip())), None)

            if not downloaded_file:
                start_response("500 Internal Server Error", [("Content-Type", "text/plain")])
                return [f"File not found. Script output:\n\n{result.stdout}".encode('utf-8')]

            downloaded_file = downloaded_file.strip()

            # Return file as download
            with open(downloaded_file, 'rb') as f:
                file_data = f.read()

            headers = [
                ('Content-Type', 'application/octet-stream'),
                ('Content-Disposition', f'attachment; filename="{os.path.basename(downloaded_file)}"'),
                ('Content-Length', str(len(file_data)))
            ]
            start_response('200 OK', headers)
            return [file_data]

        except subprocess.CalledProcessError as e:
            start_response('500 Internal Server Error', [('Content-Type', 'text/plain')])
            return [f"Script error:\n{e.stderr or e.stdout}".encode('utf-8')]

    else:
        start_response('404 Not Found', [('Content-Type', 'text/plain')])
        return [b"Not found"]
