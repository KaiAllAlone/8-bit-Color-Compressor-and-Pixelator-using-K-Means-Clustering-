from flask import Flask, render_template, request, send_file, jsonify
import tempfile, os
from main import main

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compress', methods=['POST'])
def compress():
    """
    Handles image uploads, runs compression, and returns the processed image.
    """
    # Get uploaded image
    file = request.files['image']
    k = int(request.form.get('k', 8))
    s=  int(request.form.get('s', 8))
    # Create temporary input/output files
    temp_in = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    temp_out = tempfile.NamedTemporaryFile(delete=False, suffix=".png")

    # Save upload to temp_in
    file.save(temp_in.name)
    # Run compression
    main(temp_in.name, temp_out.name,k, s)

    # Return the resulting image
    return send_file(temp_out.name, mimetype='image/png')

import os

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
