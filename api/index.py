from flask import Flask, request, send_file
from PIL import Image
import io

app = Flask(__name__)

@app.route('/', methods=['POST'])
def resize_image():
    # 1. Get binary from n8n
    file = request.data
    width = int(request.args.get('w', 800))
    
    # 2. Open and Resize
    img = Image.open(io.BytesIO(file))
    
    # Maintain aspect ratio
    w_percent = (width / float(img.size[0]))
    h_size = int((float(img.size[1]) * float(w_percent)))
    img = img.resize((width, h_size), Image.Resampling.LANCZOS)
    
    # 3. Convert to WebP in memory
    img_io = io.BytesIO()
    img.save(img_io, 'WEBP', quality=80)
    img_io.seek(0)
    
    return send_file(img_io, mimetype='image/webp')