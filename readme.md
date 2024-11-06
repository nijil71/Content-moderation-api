# AI-Powered Content Moderation API 🛡️

A scalable Flask-based API that leverages advanced AI models to detect and filter inappropriate content, including hate speech, NSFW material, spam, and offensive content across various media types (text, images, and videos).

## 🌟 Features

- **Multi-Modal Content Analysis**
  - Text moderation using BERT-based models
  - Image classification for NSFW content
  - Video frame analysis
  - Real-time processing capabilities

- **Security & Performance**
  - JWT authentication
  - Rate limiting
  - Multi-threaded video processing
  - Configurable batch processing

- **Comprehensive Analysis**
  - Toxic content detection
  - Spam identification
  - Sentiment analysis
  - NSFW content detection
  - Frame-by-frame video analysis

## 🚀 Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/content-moderation-api.git
cd content-moderation-api
```

2. Create and activate a virtual environment:
```bash
python -m venv env
source env/bin/activate  # On Windows: .\env\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
export SECRET_KEY='your-secret-key'  # On Windows: set SECRET_KEY=your-secret-key
export FLASK_APP=app.py
```

## 🔧 Configuration

The API can be configured through environment variables or the `config.py` file:

- `SECRET_KEY`: JWT signing key
- `MAX_CONTENT_LENGTH`: Maximum file size (default: 16MB)
- `RATE_LIMIT_REQUESTS`: Maximum requests per minute (default: 60)
- `MAX_TEXT_SIZE`: Maximum text length (default: 5000 characters)

## 📝 API Usage

### Authentication

Get JWT token:
```bash
POST /api/auth/token
Content-Type: application/json

{
    "username": "test_user",
    "password": "test_password"
}
```

### Text Moderation

```bash
POST /api/moderate/text
Authorization: Bearer <your_token>
Content-Type: application/json

{
    "text": "Text content to moderate"
}
```

Example Response:
```json
{
    "toxic": {
        "label": "non-toxic",
        "score": 0.9876
    },
    "sentiment": {
        "label": "POSITIVE",
        "score": 0.8765
    },
    "spam": {
        "score": 0.0,
        "is_spam": false,
        "reasons": []
    },
    "moderation_result": {
        "is_flagged": false,
        "reason": "Content appears to be safe"
    }
}
```

### Image Moderation

```bash
POST /api/moderate/image
Authorization: Bearer <your_token>
Content-Type: multipart/form-data

file: <image_file>
```

### Video Moderation

```bash
POST /api/moderate/video
Authorization: Bearer <your_token>
Content-Type: multipart/form-data

file: <video_file>
```

## 🧪 Testing

1. Start the Flask server:
```bash
python app.py
```

2. Use Thunder Client or any API testing tool to test the endpoints.

Example test cases are provided in the `tests` directory.

## 🛠️ Tech Stack

- Python 3.x
- Flask
- PyTorch
- Transformers (Hugging Face)
- OpenCV
- PIL (Python Imaging Library)

## ⚡ Performance

- Text moderation: ~100ms per request
- Image moderation: ~500ms per image
- Video moderation: ~1s per second of video
- Supports concurrent requests through multi-threading

## 🔒 Security Features

- JWT authentication
- Rate limiting
- File type validation
- Content size validation
- Secure file handling
- Error logging

## 📈 Scaling Considerations

- Implements batch processing for efficient model inference
- Supports multi-threading for video processing
- Can be deployed with multiple workers
- Compatible with cloud services (AWS, Azure, GCP)

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/new-feature`
3. Commit your changes: `git commit -m 'Add new feature'`
4. Push to the branch: `git push origin feature/new-feature`
5. Submit a pull request

#

## 🙏 Acknowledgements

- [Hugging Face](https://huggingface.co/) for providing pre-trained models
- [Flask](https://flask.palletsprojects.com/) for the web framework
- [OpenCV](https://opencv.org/) for image and video processing capabilities

## 📞 Support

For support and queries:
- Create an issue in the GitHub repository
- Email: nmnijilkhan@gmail.com

---
Made with ❤️ by Nijil N m