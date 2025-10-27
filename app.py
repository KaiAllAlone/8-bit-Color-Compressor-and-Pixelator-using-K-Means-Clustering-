from flask import Flask, request, send_file
import tempfile, os
from main import main

app = Flask(__name__)

@app.route('/')
def home():
    """
    Displays a simple HTML upload form.
    """
    return '''
    <h2>8-Bit Image Compressor</h2>
    <form action="/compress" method="post" enctype="multipart/form-data">
        <input type="file" name="image" accept="image/*" required><br><br>
        <label>Number of colors (k):</label>
        <input type="number" name="k" value="8" min="2" max="64"><br><br>
        <button type="submit">Compress</button>
    </form>
    '''

@app.route('/compress', methods=['POST'])
def compress():
    """
    Handles image uploads, runs compression, and returns the processed image.
    """
    # Get uploaded image
    file = request.files['image']
    k = int(request.form.get('k', 8))

    # Create temporary input/output files
    temp_in = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    temp_out = tempfile.NamedTemporaryFile(delete=False, suffix=".png")

    # Save upload to temp_in
    file.save(temp_in.name)

    # Run compression
    main(temp_in.name, temp_out.name, k)

    # Return the resulting image
    return send_file(temp_out.name, mimetype='image/png')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
