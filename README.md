# 🦷 Dudo Dent

A simple Django web application for dental clinic management, featuring Google Calendar integration, intelligent appointment scheduling, and asynchronous email notifications. Built with modern web technologies and deployed on DigitalOcean for reliable, scalable operations.

[![Django](https://img.shields.io/badge/Django-4.2+-092E20?style=flat&logo=django&logoColor=white)](https://djangoproject.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=flat&logo=postgresql&logoColor=white)](https://postgresql.org/)
[![Redis](https://img.shields.io/badge/Redis-DC382D?style=flat&logo=redis&logoColor=white)](https://redis.io/)
[![DigitalOcean](https://img.shields.io/badge/DigitalOcean-0080FF?style=flat&logo=digitalocean&logoColor=white)](https://digitalocean.com/)

🚀 **Live Demo:** [https://dudodent.online/)

## 📚 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Getting Started](#-getting-started)
- [User Roles](#-user-roles-and-permissions)
- [Appointment System](#-appointment-system)
- [Email Notifications](#-email-notifications)
- [API Documentation](#-api-documentation)
- [Deployment](#-deployment)
- [License](#-license)
- [Contact](#-contact)

## ✨ Features

### 🔐 **Role-Based Access Control**
- **Three distinct user roles**: Dentist, Nurse, and Patient
- Granular permissions system with role-specific capabilities
- Secure authentication and authorization

### 🗓️ **Google Calendar Integration**
- Automatic Google Calendar creation for each dentist
- Real-time synchronization of appointments
- OAuth2 authentication for secure API access

### 🕒 **Smart Scheduling System**
- 15-minute time slot precision
- Dentist availability management with recurring patterns
- Conflict prevention and double-booking protection
- Real-time availability checking

### 👥 **Patient Management**
- Automatic profile linking via email matching
- Comprehensive patient history tracking
- Visit records and appointment history

### 📊 **Interactive Calendar Interface**
- Modern FullCalendar.js implementation
- Multi-dentist filtering and views

### 📬 **Asynchronous Email System**
- Celery-powered background task processing
- SendGrid integration for reliable delivery
- Comprehensive notification system
- Email template customization

### 🌐 **Production-Ready Architecture**
- PostgreSQL database with optimized queries
- Redis caching and session management
- Cloudinary integration for image storage and optimization
- Scalable deployment on DigitalOcean
- Environment-based configuration

## 🛠 Tech Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Backend Framework** | Django 4.2+ | Web application framework |
| **Database** | PostgreSQL | Primary data storage |
| **Task Queue** | Celery | Asynchronous task processing |
| **Message Broker** | Redis | Task queue and caching |
| **Calendar Integration** | Google Calendar API | External calendar sync |
| **Frontend Calendar** | FullCalendar.js | Interactive calendar UI |
| **Email Service** | SendGrid Web API | Transactional emails |
| **Image Storage** | Cloudinary | Image upload and optimization |
| **Deployment** | DigitalOcean App Platform | Cloud hosting |
| **Authentication** | Django Auth + OAuth2 | User management |

## 🚀 Getting Started

### Prerequisites

Ensure you have the following installed:
- Python 3.10+
- PostgreSQL 12+
- Redis 6+
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/dudo-dent.git
   cd dudo-dent
   ```

2. **Set up Python environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   
   Create a `.env` file in the project root and add you local host at ALLOWED_HOSTS in settings.py:
   ```env
   # Django Settings
   DEBUG=True
   
   # Database
   DB_NAME=your_db_name
   DB_USER=your_db_user
   DB_PASSWORD=your_db_passowrd
   DB_HOST=your_db_host
   DB_PORT=your_db_port
   DB_SSLMODE=sslmode
   
   # Secret Key
   SECRET_KEY=your_django_secret_key
   
   # Cloudinary 
   CLOUDINARY_CLOUD_NAME=your_cloudinary_cloud_name
   API_KEY=your_cloudinary_api_key
   API_SECRET=your_cloudinary_api_secret
   
    # Google Calendar 
   GOOGLE_CLIENT_ID=your_google_client_id
   GOOGLE_CALENDAR_ID=your@calendar.id
   GOOGLE_ADMIN_EMAIL=your@admin.email
   
   # Celety + Redis
   CELERY_BROKER_URL=redis://redis:6379/0
   CELERY_RESULT_BACKEND=redis://redis:6379/0
   
   # Google SMTP Settings (for local setup)
   EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
   EMAIL_HOST=smtp.gmail.com 
   EMAIL_PORT=587 
   EMAIL_USE_TLS=True 
   EMAIL_HOST_USER=your@hostuser.com 
   EMAIL_HOST_PASSWORD=your_password
   
   # SendGrid Email
   SENDGRID_API_KEY=your_sendgrid_api_key
   DEFAULT_FROM_EMAIL=noreply@yourdomain.com
   ```

4. **Set up the database**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser
   ```

5. **Start Redis server**
   ```bash
   # Using Docker (recommended)
   docker run -d -p 6379:6379 --name redis-server redis:alpine
   
   # Or install locally and run
   redis-server
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

7. **Start Celery worker** (in a new terminal)
   ```bash
   celery -A dudo_dent worker -l info
   ```

Visit `http://localhost:8000` to access the application.

## 👥 User Roles and Permissions

### 🦷 **Dentist**
- Full clinic management capabilities
- Set availability and unavailability periods
- Manage patient visits and records
- Access to all appointment data
- Google Calendar automatically created
- Cannot delete other dentists (security measure)

### 👩‍⚕️ **Nurse**
- Similar permissions to dentist
- Patient management and scheduling
- Appointment coordination
- **Restrictions**: Cannot create dentist accounts or delete users

### 🧑‍⚕️ **Patient**
- Self-registration and profile management
- Book appointments with available dentists
- View personal appointment history
- Automatic profile linking via email matching

## 📅 Appointment System

### Key Features
- **15-minute precision**: All appointments scheduled in quarter-hour increments
- **Real-time availability**: Only available slots shown during booking

### Calendar Interface
- Modern FullCalendar.js implementation
- Multi-dentist view with filtering

## 📬 Email Notifications

All email communications are handled asynchronously using **Celery** and **Redis**, ensuring fast response times and reliable delivery through **SendGrid**.

### Automated Notifications
- ✅ **User Registration**: Welcome emails with account details
- 📅 **Appointment Booking**: Confirmation with calendar attachment
- ✏️ **Appointment Updates**: Change notifications to relevant parties
- ❌ **Appointment Cancellation**: Cancellation confirmations

## 🌐 Deployment

Dudo Dent is optimized for deployment on **DigitalOcean App Platform** with the following architecture:

### Production Setup
1. **Application**: Django app with Gunicorn WSGI server
2. **Database**: Managed PostgreSQL database
3. **Cache/Queue**: Managed Redis instance
4. **Worker**: Celery worker for background tasks
5. **Image Storage**: Cloudinary CDN for optimized image delivery
6. **Static Files**: CDN-served static assets

### Deployment Steps
1. Fork this repository to your GitHub account
2. Create a new app on DigitalOcean App Platform
3. Connect your GitHub repository
4. Configure environment variables in the dashboard
5. Add PostgreSQL and Redis managed databases
6. Deploy and configure custom domain (optional)

### Environment Variables for Production
```env
DEBUG=False
SECRET_KEY=your_production_secret_key
DATABASE_URL=your_managed_postgres_url
REDIS_URL=your_managed_redis_url
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
SENDGRID_API_KEY=your_sendgrid_key
DEFAULT_FROM_EMAIL=noreply@yourdomain.com
CLOUDINARY_CLOUD_NAME=your_cloudinary_cloud_name
CLOUDINARY_API_KEY=your_cloudinary_api_key
CLOUDINARY_API_SECRET=your_cloudinary_api_secret
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
GOOGLE_REDIRECT_URI=https://yourdomain.com/auth/google/callback/
```

## 🧪 Testing

Run the test suite:
```bash
python manage.py test
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📬 Contact

**Dudo Dent** - A modern dental clinic management solution

👨‍💻 **Created by**: [Branimir Anastasov]  
📧 **Email**: [branimir.anastassov@gmail.com]  
🔗 **GitHub**: [@Enarb1](https://github.com/Enarb1)  

---
