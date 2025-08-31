# Django Settings Configuration Guide

This project uses a modular settings configuration to separate concerns between different environments (development, production) while maintaining a shared base configuration.

## 📁 Settings Structure

```
config/
├── settings/
│   ├── __init__.py
│   ├── base.py          # Shared base settings
│   ├── development.py   # Development-specific settings
│   └── production.py    # Production-specific settings
├── wsgi.py             # Production WSGI configuration
├── asgi.py             # Production ASGI configuration
└── urls.py
```

## 🔧 Configuration Files

### `base.py` - Shared Base Settings
Contains all common settings used across environments:
- Django core configuration
- Installed apps and middleware
- Database configuration (with environment variables)
- Authentication and JWT settings
- Static/media file settings
- Logging configuration
- Email configuration base
- Security settings base

### `development.py` - Development Settings
Inherits from base and adds/overrides:
- `DEBUG = True`
- Relaxed security settings
- Console email backend
- Local memory caching
- Debug toolbar integration (if installed)
- Browsable API renderer
- Extended file upload limits
- Detailed logging to console

### `production.py` - Production Settings
Inherits from base and adds/overrides:
- `DEBUG = False`
- Strict security settings (HTTPS, HSTS, secure cookies)
- Redis caching configuration
- SMTP email backend
- Static file compression
- Rate limiting
- Error tracking (Sentry integration)
- Celery configuration
- Performance optimizations

## 🚀 Usage

### Development Environment
The project is configured to use development settings by default:

```bash
# Default - uses development settings
python manage.py runserver

# Explicit development settings
DJANGO_SETTINGS_MODULE=config.settings.development python manage.py runserver

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

### Production Environment
For production deployment, set the environment variable:

```bash
# Set environment variable
export DJANGO_SETTINGS_MODULE=config.settings.production

# Or use it directly
DJANGO_SETTINGS_MODULE=config.settings.production python manage.py collectstatic
DJANGO_SETTINGS_MODULE=config.settings.production python manage.py migrate
```

### Testing Environment
You can create a separate testing configuration if needed:

```bash
# Use development settings for testing
python manage.py test

# Or create config/settings/testing.py and use:
DJANGO_SETTINGS_MODULE=config.settings.testing python manage.py test
```

## 🔐 Environment Variables

### Required for All Environments
```env
SECRET_KEY=your-secret-key-here
DB_NAME=waste_db
DB_USER=waste_user
DB_PASSWORD=waste_pass
DB_HOST=localhost
DB_PORT=5432
```

### Development Specific
```env
DEBUG=True
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

### Production Specific
```env
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgresql://user:pass@host:port/dbname  # Optional, overrides individual DB settings
REDIS_URL=redis://localhost:6379/1
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
SENTRY_DSN=https://your-sentry-dsn  # Optional
```

## 🐳 Docker Configuration

### Development Docker
```dockerfile
ENV DJANGO_SETTINGS_MODULE=config.settings.development
```

### Production Docker
```dockerfile
ENV DJANGO_SETTINGS_MODULE=config.settings.production
```

## 📊 Key Features by Environment

### Development Features
- ✅ Debug mode enabled
- ✅ Django Debug Toolbar (if installed)
- ✅ Browsable API interface
- ✅ Console email backend
- ✅ Relaxed CORS settings
- ✅ Local memory caching
- ✅ Detailed console logging

### Production Features
- ✅ Security hardening (HTTPS, HSTS, secure cookies)
- ✅ Redis caching and session storage
- ✅ SMTP email backend
- ✅ Static file compression
- ✅ Rate limiting
- ✅ File logging with rotation
- ✅ Error tracking integration
- ✅ Performance optimizations
- ✅ Celery task queue support

## 🔄 Switching Between Environments

### Method 1: Environment Variable
```bash
export DJANGO_SETTINGS_MODULE=config.settings.production
python manage.py runserver
```

### Method 2: Command Line
```bash
DJANGO_SETTINGS_MODULE=config.settings.development python manage.py shell
```

### Method 3: IDE Configuration
In your IDE, set the environment variable:
- PyCharm: Run Configuration → Environment Variables
- VS Code: launch.json configuration

## 🧪 Testing the Configuration

### Verify Development Settings
```bash
python manage.py shell
>>> from django.conf import settings
>>> print(settings.DEBUG)  # Should be True
>>> print(settings.ALLOWED_HOSTS)  # Should include '*'
```

### Verify Production Settings
```bash
DJANGO_SETTINGS_MODULE=config.settings.production python manage.py shell
>>> from django.conf import settings
>>> print(settings.DEBUG)  # Should be False
>>> print(settings.SECURE_SSL_REDIRECT)  # Should be True
```

## 📝 Adding New Settings

### For All Environments
Add to `config/settings/base.py`

### Environment-Specific
Add to the respective environment file (`development.py` or `production.py`)

### Override Base Settings
```python
# In development.py or production.py
from .base import *

# Override or extend base settings
MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
] + MIDDLEWARE

# Update existing settings
REST_FRAMEWORK.update({
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
})
```

## 🚨 Important Notes

1. **Never commit sensitive data** - Use environment variables for secrets
2. **Test both environments** - Ensure your code works in both dev and prod settings
3. **Keep base.py environment-agnostic** - Only put truly shared settings there
4. **Use appropriate defaults** - Provide sensible fallbacks for environment variables
5. **Document new settings** - Update this guide when adding new configuration options

## 🔍 Troubleshooting

### Common Issues

**Settings module not found:**
```bash
ModuleNotFoundError: No module named 'config.settings.development'
```
Solution: Ensure the `__init__.py` file exists in the settings directory.

**Environment variable not loaded:**
```bash
# Check if .env file exists and is in the correct location
ls -la .env
# Verify environment variables are loaded
python -c "import os; print(os.getenv('SECRET_KEY'))"
```

**Database connection issues:**
- Verify database credentials in environment variables
- Ensure PostgreSQL is running
- Check database exists and user has permissions

This modular approach provides flexibility, security, and maintainability for different deployment scenarios while keeping the configuration organized and easy to manage.
