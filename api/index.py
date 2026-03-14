from flask import Flask, request, send_file, jsonify
from PIL import Image
import io
import sys

app = Flask(__name__)

@app.route('/', methods=['POST'])
def resize_image():
    try:
        image_bytes = request.data
        if not image_bytes:
            return jsonify({"error": "No image data received"}), 400

        # 1. Open the image to check dimensions
        img = Image.open(io.BytesIO(image_bytes))
        orig_w, orig_h = img.size

        # 2. Determine target width based on orientation
        if orig_w > orig_h:
            # Horizontal (Landscape)
            target_w = 1920
        else:
            # Vertical (Portrait) or Square
            target_w = 1080

        # 3. Only resize if the image is actually LARGER than our target
        # (This prevents pixelation of small images)
        if orig_w > target_w:
            w_percent = (target_w / float(orig_w))
            target_h = int((float(orig_h) * float(w_percent)))
            img = img.resize((target_w, target_h), Image.Resampling.LANCZOS)
        
        # 4. Save to WebP
        img_io = io.BytesIO()
        img.save(img_io, 'WEBP', quality=85) # High quality WebP
        img_io.seek(0)
        
        return send_file(img_io, mimetype='image/webp')

    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        return jsonify({"error": str(e)}), 500