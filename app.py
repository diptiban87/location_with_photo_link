from flask import Flask, render_template, request, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import uuid

app = Flask(__name__)

# PythonAnywhere specific paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(BASE_DIR, "photos.db")}'
app.config['UPLOAD_FOLDER'] = os.path.join(BASE_DIR, 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

db = SQLAlchemy(app)

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

class Photo(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    locations = db.relationship('Location', backref='photo', lazy=True)

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    photo_id = db.Column(db.String(36), db.ForeignKey('photo.id'), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_photo():
    if 'photo' not in request.files:
        return jsonify({'error': 'No photo provided'}), 400
    
    file = request.files['photo']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Generate unique ID for the photo
    photo_id = str(uuid.uuid4())
    filename = f"{photo_id}_{file.filename}"
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    # Save photo info to database
    photo = Photo(
        id=photo_id,
        filename=filename,
        original_filename=file.filename
    )
    db.session.add(photo)
    db.session.commit()

    # Use request.host_url to get the correct domain
    base_url = request.host_url.rstrip('/')
    return jsonify({
        'success': True,
        'photo_id': photo_id,
        'view_url': f'{base_url}/view/{photo_id}',
        'admin_url': f'{base_url}/admin/{photo_id}'
    })

@app.route('/view/<photo_id>')
def view_photo(photo_id):
    photo = Photo.query.get_or_404(photo_id)
    return render_template('view.html', photo=photo)

@app.route('/admin/<photo_id>')
def admin_view(photo_id):
    photo = Photo.query.get_or_404(photo_id)
    return render_template('admin.html', photo=photo)

@app.route('/photo/<photo_id>')
def get_photo(photo_id):
    photo = Photo.query.get_or_404(photo_id)
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], photo.filename))

@app.route('/track/<photo_id>', methods=['POST'])
def track_location(photo_id):
    photo = Photo.query.get_or_404(photo_id)
    data = request.get_json()
    
    location = Location(
        photo_id=photo_id,
        latitude=data['latitude'],
        longitude=data['longitude']
    )
    db.session.add(location)
    db.session.commit()
    
    return jsonify({'success': True})

@app.route('/locations/<photo_id>')
def get_locations(photo_id):
    photo = Photo.query.get_or_404(photo_id)
    locations = Location.query.filter_by(photo_id=photo_id).order_by(Location.timestamp.asc()).all()
    return jsonify([{
        'latitude': loc.latitude,
        'longitude': loc.longitude,
        'timestamp': loc.timestamp.isoformat()
    } for loc in locations])

# This is for local development only
if __name__ == '__main__':
    app.run(debug=False) 