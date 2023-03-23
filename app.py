from flask import Flask, Response, render_template  # Flask web framework and response classes
import pyscreenshot as ImageGrab  # library for capturing screenshots
from io import BytesIO  # library for handling byte streams
import os  # library for interacting with the operating system

app = Flask(__name__)

@app.route('/')
def home():
    # Render the index.html template
    return render_template('index.html')

@app.route('/screenshot')
def screenshot():
    def generate():
        while True:
            # Check if the stop.txt file exists
            if os.path.exists("stop.txt"):
                # If it does, remove the file and return from the function to stop the screen sharing
                os.remove("stop.txt")
                return

            # Grab a screenshot of the entire screen
            im = ImageGrab.grab()

            # Convert the image to PNG format
            im_io = BytesIO()
            im.save(im_io, 'PNG')
            im_io.seek(0)

            # Yield the image data as a part of the multipart response
            yield (b'--frame\r\n'
                   b'Content-Type: image/png\r\n\r\n' + im_io.getvalue() + b'\r\n')

    # Return the multipart response with the appropriate headers
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/stop')
def stop():
    # Kill the Flask app process
    os.kill(os.getpid(), 9)
    return "Screen sharing stopped."

if __name__ == '__main__':
    # Start Flask app with threaded option
    app.run(host='0.0.0.0', threaded=True)
