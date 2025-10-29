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
    filename = file.filename
    ext = os.path.splitext(filename)[1].lower() 

    # Default to .png if unknown
    if ext not in [".png", ".jpg", ".jpeg",".webp"]:
        ext = ".png"

    k = int(request.form.get('k', 8))
    s = int(request.form.get('s', 8))

    # Create temp files with the same extension
    temp_in = tempfile.NamedTemporaryFile(delete=False, suffix=ext)
    temp_out = tempfile.NamedTemporaryFile(delete=False, suffix=ext)

    # Save upload
    file.save(temp_in.name)

    # Run your compression logic
    main(temp_in.name, temp_out.name, k, s)

    # Determine correct MIME type
    mime_type = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".webp":  "image/webp"
    }.get(ext, "application/octet-stream")

    # Return the processed file
    return send_file(temp_out.name, mimetype=mime_type)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
