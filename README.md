# Wellify - Mental Wellness Platform

A comprehensive Django-based mental wellness platform for students with AI-powered chatbot, risk assessment, and counsellor support.

## Features

### For Students
- 🤖 AI Chatbot for instant mental health support
- 📋 PHQ-9 & GAD-7 Assessment tools
- 🧘 Guided meditation videos
- 🌬️ Breathing exercises
- ✍️ Personal journaling
- 💡 Motivational content
- 📅 Book counselling sessions

### For Counsellors
- 👥 View students by risk level (High/Medium/Low)
- 💬 Access student chat history
- 📊 View assessment scores (PHQ-9, GAD-7)
- 📅 Manage appointment requests
- 🚨 Automatic alerts for high-risk students

### For Admins
- 📈 Dashboard with system statistics
- 👤 User management
- 🔍 Monitor high-risk cases

## Tech Stack

- **Backend**: Django 4.2
- **Databases**: 
  - SQLite (User authentication & sessions)
  - MongoDB (Chat logs, assessments, wellness content)
- **Frontend**: HTML, CSS, JavaScript
- **AI**: Keyword-based stress detection with risk scoring

## Installation

### Prerequisites
- Python 3.8+
- MongoDB (local or Atlas)
- pip

### Setup Steps

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd Wellify
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env with your settings
```

5. **Run migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Populate wellness content**
```bash
python manage.py populate_wellness_content
```

7. **Create superuser (optional)**
```bash
python manage.py createsuperuser
```

8. **Run the development server**
```bash
python manage.py runserver
```

Visit `http://localhost:8000` in your browser.

## Environment Variables

Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

MONGODB_NAME=wellness_connect_db
MONGODB_URI=mongodb://localhost:27017/wellness_connect_db
```

For production, set `DEBUG=False` and update `ALLOWED_HOSTS` with your domain.

## Project Structure

```
Wellify/
├── accounts/           # User authentication & risk engine
├── student/            # Student features (chatbot, assessments, wellness)
├── counsellor/         # Counsellor dashboard & tools
├── admin_panel/        # Admin dashboard
├── templates/          # Shared templates
├── wellness_connect/   # Django settings & URLs
├── logs/               # Application logs
├── db.sqlite3          # SQLite database
└── manage.py           # Django management script
```

## User Roles

1. **Student**: Access chatbot, assessments, wellness tools, book sessions
2. **Counsellor**: View students, manage appointments, access chat history
3. **Admin**: System administration and monitoring

## Risk Assessment System

The platform uses a multi-factor risk engine:
- PHQ-9 score (depression): 0-27
- GAD-7 score (anxiety): 0-21
- Chat stress level: Low/Medium/High
- Final risk level: Low/Medium/High

High-risk students trigger automatic counsellor notifications.

## Security Features

- Environment-based configuration
- CSRF protection
- Password validation (min 8 characters)
- Secure session management
- Production-ready SSL/HTTPS settings
- Comprehensive logging

## Development

### Running Tests
```bash
python manage.py test
```

### Creating Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Accessing Admin Panel
```bash
python manage.py createsuperuser
# Visit http://localhost:8000/admin
```

## Deployment

For production deployment:

1. Set environment variables:
   - `DEBUG=False`
   - `SECRET_KEY=<strong-random-key>`
   - `ALLOWED_HOSTS=yourdomain.com`
   - `MONGODB_URI=<your-mongodb-atlas-uri>`

2. Collect static files:
```bash
python manage.py collectstatic
```

3. Use a production server (gunicorn, uwsgi)
4. Set up HTTPS/SSL certificates
5. Configure MongoDB backups

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is for educational purposes.

## Support

For issues or questions, please open an issue on GitHub.

## Acknowledgments

- Django framework
- MongoDB & MongoEngine
- Mental health assessment tools (PHQ-9, GAD-7)
