# Internship_w3_Assignment6


# Development of a Property Management System Using Django Internship Project A6
# Table of Contents 
1. [Overview](#overview) 
2. [Key Features](#key-features) 
3.  [Technologies Used](#technologies-used) 
4. [Usage for Admin/User](#usage-for-admin/user)
5. [Development Setup](#development-setup) 
6. [Project Structure](#project-structure) 
7. [Author](#author)


## Overview
This an web-app that involves creating a Django application to manage property information through the
Django Admin interface. The goal is to set up a robust data storage solution using PostgreSQL
with PostGIS extensions, allowing geospatial data handling and integration for property locations.

--- 
## Key Features 
- **Django Admin Integration**: Manage property, location, and accommodation data efficiently through the admin panel. 
- **Geospatial Data Handling**: Use PostGIS to store and query location data with geospatial capabilities.
 - **CSV Import**: Upload location data via CSV files directly in the admin panel. 
- **Access Control**: Property owners can view, edit, and update only their data, with restrictions for non-admin users.
 - **Localization**: Support for multiple languages in property descriptions and policies. 
 - **Custom Sitemap Generator**: Command-line tool to generate location-based sitemaps in JSON format. 
 - **User Groups and Permissions**: Configurable permissions for property owners and admins. 


---

## Technologies Used

- **Framework**: [Django ](https://www.djangoproject.com/)
- **Database**: [PostgreSQL](https://www.postgresql.org/) with [PostGIS](https://postgis.net/)
- **Front-End**: Django Admin (customized)
- **Geospatial Library**: GeoDjango
- **Testing**: Python `unittest` with mocked functions
- **Language Detection**: [LangDetect](https://pypi.org/project/langdetect/)
- **Containerization**: Docker (optional for PostgreSQL setup)

---

## Usage for Admin/User

### For Admin Users: 
1. Log in to the Django admin panel using your credentials. 
2. Manage Locations: - Create new locations manually or import them via CSV. 
3. Manage Accommodations: - Add, edit, delete, and view accommodations with geospatial data and amenities. 
4. Localize Accommodations: - Add descriptions and policies in multiple languages. 

### For Regular Users: 
1. Submit property sign-up requests through the signup page. 
2. Manage personal property data as per access permissions. 

--- 
## Development Setup

### Prerequisites

Ensure the following are installed on your system:

- Python 3.10 or higher
- Django
- PostgreSQL with PostGIS extension 
- Docker 

### Steps: 1. Clone the repository:
 ```bash 
git clone https://github.com/Rubayet09/Internship_w3_Assignment6.git cd Internship_w3_Assignment6
 ```

### Steps: 2. Create venv and install dependencies:
 ```bash 
python3 -m venv venv 
source venv/bin/activate

pip install -r requirements.txt

 ```

### Steps: 3. Run migrations:
 ```bash 
python manage.py makemigrations 
python manage.py migrate
 ```
### Steps: 4. Create a superuser:
 ```bash 
python manage.py createsuperuser
 ```
 
### Steps: 5. Start the server:
 ```bash 
docker-compose up
 ```

## How to Use
1. Navigate to http://localhost:8000/admin/login/?next=/admin/
2. Input the Username and Password used to create the superuser.
3. Go to polls/Locations and click on import CSV button to import the csv files. Then, you can see the list of locations, Select and DELETE locations, Filter locations.
4. Go to polls/Accomodations then add by filling up all the fields accordingly, see the list of Accomodations, Select and DELETE, Filter.
5. Go to polls/Localize accomodations then add by filling up all the fields accordingly. If you choose Language 'bn', you need to write- 'Description:' 
``` bash
"পর্বতের মাঝে একটি আরামদায়ক কেবিন, যা একান্তে ছুটি কাটানোর জন্য আদর্শ।"
```
This field will not take "A cozy cabin in the mountains, ideal for a secluded getaway." for 'bn'. 
Also, for the 'Policy' input value-  
 ``` bash
 {"পশু": "পশু অনুমোদিত, তবে অতিরিক্ত পরিষ্কার করার জন্য ফি প্রযোজ্য।", 
 "চেক": "বিকাল ৩ টা", 
 "চেক-আউট": "দুপুর ১২ টা", 
 "বাতিলকরণ": "চেক-ইনের ৭ দিনের মধ্যে বাতিল করা হলে সম্পূর্ণ ফেরত।"} 
 ```
 and save. Then, see the list of Localize accomodations, Select and DELETE if needed.
6. For Regular user- navigate to http://localhost:8000/signup/ and input the required fields.
7. Then admin will authenticate the user and mark as staff and make him a property owner who can access his own properties to create, delete or edit.

### Steps: 6. Running Tests
```bash 
coverage run --source='.' manage.py test
coverage report
 ```
NB: The test covers 77% Code Coverage.

### Steps: 6. Generate a Sitemap
```bash 
python manage.py generate_sitemap
 ```

---
## Project Structure
```
DJANGO PROJECT
└── djangotutorial
    ├── mysite
    │   ├── __pycache__
    │   ├── __init__.py
    │   ├── asgi.py
    │   ├── settings.py
    │   ├── urls.py
    │   └── wsgi.py
    ├── polls
    │   └── __pycache__
	   ├── commands
    │   │	├── __init__.py
    │   │	├── generate_sitemap.py
    │   └── init.py
    ├── migrations
    │   ├── __init__.py
    │   └── 0001_initial.py
    ├── templates
    │   ├── signup.html
    │   └── admin
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── models.py
    ├── tests.py
    ├── urls.py
    └── views.py
	   ├── docker-compose.yml
    ├── Dockerfile
    ├── locatins-IN.csv
    ├── locations-BD.csv
    ├── locations-US.csv
    ├── manage.py
    ├── pytest.ini
    └── requirements.txt
```

## Author

Rubayet Shareen
SWE Intern, W3 Engineers
Dhaka, Bangladesh
