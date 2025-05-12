# Photo Tracker

A web application that allows you to send photos to users and track their location when they open them.

## Features

- Upload photos and get a shareable link
- Track viewer's location when they open the photo
- View location on an interactive map
- Secure and private photo sharing

## Setup

1. Install Python 3.7 or higher
2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Get a Google Maps API key from the [Google Cloud Console](https://console.cloud.google.com/)
4. Replace `YOUR_GOOGLE_MAPS_API_KEY` in `templates/view.html` with your actual API key
5. Run the application:
   ```bash
   python app.py
   ```
6. Open your browser and go to `http://localhost:5000`

## Usage

1. On the home page, click "Choose a photo" to select an image
2. Click "Upload Photo" to upload the image
3. Copy the generated link and share it with others
4. When someone opens the link:
   - They'll see the photo
   - Their location will be automatically tracked
   - The location will be displayed on a map

## Security Notes

- The application requires user permission to access location
- Location data is stored securely in a SQLite database
- Each photo has a unique ID for secure sharing

## Requirements

- Flask
- Flask-SQLAlchemy
- Pillow
- python-dotenv
- Google Maps API key 