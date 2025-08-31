# Waste Collection & Management System

A comprehensive Django REST API system for managing waste collection operations, designed to streamline the entire waste management workflow from citizen requests to route optimization and billing.

## 🌟 Project Overview

This system provides a complete solution for waste collection management, featuring:

- **Citizen Portal**: Request waste collection services
- **Driver Management**: Track drivers, vehicles, and assignments  
- **Route Optimization**: Efficient collection route planning
- **Real-time Tracking**: Monitor collection progress
- **Analytics Dashboard**: Comprehensive reporting and insights
- **Billing System**: Automated invoicing and payment tracking
- **Notification System**: Real-time updates for all stakeholders

## 🏗️ System Architecture

The system is built using Django REST Framework with the following apps:

```
├── accounts/          # User management and authentication
├── locations/         # Address and zone management
├── waste/            # Collection requests and waste types
├── fleet/            # Vehicle and driver management
├── routing/          # Route planning and optimization
├── tracking/         # Real-time tracking functionality
├── notifications/    # User notification system
├── collection/       # Pickup requests and scheduling
├── analytics/        # Reporting and dashboard
└── billing/          # Invoicing and payment management
```

## 🚀 Features

### Core Functionality
- **Multi-role Authentication**: Citizens, Drivers, Dispatchers, and Admins
- **Collection Request Management**: Create, schedule, and track waste collection requests
- **Fleet Management**: Manage vehicles, drivers, and their assignments
- **Route Optimization**: Intelligent routing for efficient collection
- **Real-time Tracking**: GPS-based vehicle and collection tracking
- **Notification System**: Email, SMS, and push notifications
- **Analytics & Reporting**: Comprehensive dashboard with insights
- **Billing Integration**: Automated invoicing based on completed collections

### User Roles & Permissions
- **Citizens**: Create collection requests, view status, receive notifications
- **Drivers**: View assigned routes, update collection status, track progress
- **Dispatchers**: Manage routes, assign drivers, monitor operations
- **Admins**: Full system access, user management, system configuration

## 📋 Prerequisites

- Python 3.8+
- PostgreSQL 12+
- Redis (for caching and notifications)
- Virtual environment (recommended)

## ⚙️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/ALX-Capstone_project.git
cd ALX-Capstone_project
```

### 2. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
Create a `.env` file in the project root:
```env
DEBUG=True
SECRET_KEY=your-secret-key-here
DB_NAME=waste_db
DB_USER=waste_user
DB_PASSWORD=waste_pass
DB_HOST=localhost
DB_PORT=5432
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
SIMPLE_JWT_SECRET_KEY=your-jwt-secret-key
```

### 5. Database Setup
```bash
# Create PostgreSQL database
createdb waste_db

# Run migrations
python manage.py makemigrations
python manage.py migrate


# Create superuser
python manage.py createsuperuser
```

### 6. Start Development Server
```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/`

## 🧪 Testing the System

### 1. API Documentation
Visit the interactive API documentation:
- **Swagger UI**: `http://localhost:8000/api/docs/`
- **API Schema**: `http://localhost:8000/api/schema/`

### 2. Authentication Testing

#### Register a New User
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123",
    "role": "CITIZEN"
  }'
```

#### Login and Get Token
```bash
curl -X POST http://localhost:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "testpass123"
  }'
```

Save the returned `access` token for authenticated requests.

### 3. Core Functionality Testing

#### Create a Collection Request
```bash
curl -X POST http://localhost:8000/api/waste/collection-requests/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "address": 1,
    "waste_type": 1,
    "quantity_kg": 25.5,
    "preferred_date": "2025-09-01",
    "notes": "Large furniture items included"
  }'
```

#### List Collection Requests
```bash
curl -X GET http://localhost:8000/api/waste/collection-requests/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

#### Create a Vehicle (Admin/Dispatcher only)
```bash
curl -X POST http://localhost:8000/api/fleet/vehicles/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "plate_number": "WC-001",
    "capacity_kg": 5000,
    "status": "AVAILABLE"
  }'
```

#### Get Analytics Dashboard (Admin/Dispatcher only)
```bash
curl -X GET http://localhost:8000/api/analytics/analytics/dashboard/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 4. Advanced Testing Scenarios

#### Schedule a Collection Request
```bash
curl -X POST http://localhost:8000/api/waste/collection-requests/1/schedule/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "scheduled_date": "2025-09-01"
  }'
```

#### Create Route from Requests
```bash
curl -X POST http://localhost:8000/api/routing/routes/create-from-requests/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "request_ids": [1, 2, 3],
    "driver_id": "driver-uuid",
    "vehicle_id": "vehicle-uuid"
  }'
```

#### Track Active Routes
```bash
curl -X GET http://localhost:8000/api/tracking/tracking/active-routes/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## 📊 API Endpoints Overview

### Authentication Endpoints
- `POST /api/auth/register/` - User registration
- `POST /api/auth/token/` - Login/obtain token
- `POST /api/auth/token/refresh/` - Refresh access token

### Waste Management
- `GET|POST /api/waste/collection-requests/` - Collection requests
- `GET|POST /api/waste/waste-types/` - Waste type management
- `GET|POST /api/waste/issue-reports/` - Issue reporting

### Fleet Management
- `GET|POST /api/fleet/vehicles/` - Vehicle management
- `GET|POST /api/fleet/drivers/` - Driver management
- `POST /api/fleet/vehicles/{id}/change-status/` - Update vehicle status

### Collection Operations
- `GET|POST /api/collection/pickup-requests/` - Pickup scheduling
- `GET|POST /api/collection/addresses/` - Address management
- `POST /api/collection/pickup-requests/{id}/assign-driver/` - Driver assignment

### Route Management
- `GET|POST /api/routing/routes/` - Route management
- `POST /api/routing/routes/create-from-requests/` - Create optimized routes
- `POST /api/routing/routes/{id}/optimize/` - Route optimization

### Tracking & Monitoring
- `GET /api/tracking/tracking/active-routes/` - Active route tracking
- `GET /api/tracking/tracking/vehicle-status/` - Vehicle status monitoring
- `GET /api/tracking/tracking/driver-dashboard/` - Driver dashboard

### Analytics & Reporting
- `GET /api/analytics/analytics/dashboard/` - System dashboard
- `GET /api/analytics/analytics/collection-stats/` - Collection statistics
- `GET /api/analytics/analytics/vehicle-utilization/` - Vehicle utilization

### Notifications
- `GET|POST /api/notifications/notifications/` - Notification management
- `POST /api/notifications/notifications/mark-all-read/` - Mark notifications read
- `GET /api/notifications/notifications/unread-count/` - Unread count

### Billing
- `GET|POST /api/billing/invoices/` - Invoice management
- `GET|POST /api/billing/payments/` - Payment tracking
- `POST /api/billing/invoices/generate-from-pickups/` - Generate invoices

## 🔧 Development & Testing

### Running Tests
```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test apps.waste

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

### Code Quality
```bash
# Check code style
flake8 .

# Format code
black .

# Type checking
mypy .
```

### Database Management
```bash
# Create new migration
python manage.py makemigrations app_name

# Apply migrations
python manage.py migrate

# Reset database (development only)
python manage.py flush
```

## 🚀 Deployment

### Production Setup
1. Set `DEBUG=False` in environment variables
2. Configure production database settings
3. Set up Redis for caching and notifications
4. Configure email backend for notifications
5. Set up proper static file serving
6. Use a production WSGI server (gunicorn)

### Docker Deployment
```bash
# Build and run with Docker Compose
docker-compose up --build

# Run in production mode
docker-compose -f docker-compose.prod.yml up
```

## 📝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Support

For support and questions:
- Create an issue on GitHub
- Contact the development team
- Check the API documentation at `/api/docs/`

## 🎯 Future Enhancements

- Mobile application integration
- IoT sensor integration for smart bins
- Machine learning for route optimization
- Real-time GPS tracking
- Advanced analytics and reporting
- Multi-language support
- Payment gateway integration