from flask import Flask, render_template, request, send_file
import tempfile, os
from main import main, convert_to_supported_format

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compress', methods=['POST'])
def compress():
    file = request.files['image']
    filename = file.filename
    ext = os.path.splitext(filename)[1].lower()

    # Convert unsupported files (like HEIC → JPEG)
    try:
        input_path = convert_to_supported_format(file)
        ext = ".jpeg"
    except Exception:
        temp_in = tempfile.NamedTemporaryFile(delete=False, suffix=ext)
        file.save(temp_in.name)
        input_path = temp_in.name

    k = int(request.form.get('k', 8))
    s = int(request.form.get('s', 8))

    temp_out = tempfile.NamedTemporaryFile(delete=False, suffix=ext)
    main(input_path, temp_out.name, k, s)

    mime_type = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".webp": "image/webp"
    }.get(ext, "application/octet-stream")

    return send_file(temp_out.name, mimetype=mime_type)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
