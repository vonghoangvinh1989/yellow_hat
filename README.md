# Ethical Hacking Web Application

## README

This document provides an overview of the Ethical Hacking Web Application, including its features, installation instructions, usage guidelines, Docker setup, contribution details, and contact information.

## Project Description

The Ethical Hacking Web Application is a comprehensive platform built on the Django framework that streamlines and enhances the penetration testing process. It integrates tools for all phases of ethical hacking, including:

* Planning
* Reconnaissance (passive and active)
* Exploitation
* Post-exploitation
* Reporting

This platform aims to provide a unified interface for:

* Cybersecurity professionals
* Educators
* Students

It facilitates conducting thorough and efficient penetration tests while offering educational resources to support learning and skill development in ethical hacking.

## Features

* **Tool Integration:** Seamlessly integrates various open-source ethical hacking tools (e.g., Nmap, Volatility, WhoIs, NsLookup) into one platform.
* **User Authentication:** Secure user authentication and authorization system using Django's built-in capabilities.
* **Phase Coverage:** Covers all phases of ethical hacking: planning, reconnaissance, exploitation, post-exploitation, and reporting.
* **User-Friendly Interface:** Intuitive UI/UX design for ease of use, suitable for both beginners and experienced professionals.
* **Educational Resources:** Provides tutorials, guides, and interactive learning modules to support users in learning ethical hacking techniques.
* **Security:** Implements robust security measures to protect user data and ensure the platform's integrity.
* **Scalability:** Designed to handle large datasets and multiple users simultaneously.

## Installation

This section outlines the installation process for both Docker Compose and manual methods.

### Prerequisites

* Python 3.8 or higher
* Django 3.2 or higher
* SQLite (or another preferred database system)
* Git
* Virtualenv
* Docker (optional)
* Docker Compose (optional)

### Using Docker Compose

**1. Clone the Repository**

```bash
git clone https://github.com/vonghoangvinh1989/yellow_hat
cd yellow_hat
```

**2. Create an .env File**

Create a file named `.env` in the project's root directory with the following environment variables (replace placeholders with your actual values):

```env
# API_KEY
SECURITY_TRAILS = "your_api_key_here"
HUNTER_IO = "your_api_key_here"

# GMAIL ACCOUNT
EMAIL_HOST_USER = "your_host_email"
EMAIL_HOST_PASSWORD = "your_host_email_password"
DEFAULT_FROM_EMAIL = "your_host_email_that_you_use_to_send"

# GOOGLE ACCOUNT
GOOGLE_CLIENT_ID = "google_account_client_id"
GOOGLE_SECRET_KEY = "google_account_secret_key"

# FACEBOOK ACCOUNT
FACEBOOK_CLIENT_ID = "facebook_account_client_id"
FACEBOOK_SECRET_KEY = "facebook_account_secret_key"
```

**3. Build and Run the Containers**

```bash
docker-compose up --build -d
```

This command will build the Docker image, run Django migrations, and start the Django development server on port 8000 (accessible at http://localhost:8000).

**4. Stopping the Containers**

```bash
docker-compose down
```

**5. Rebuilding the Containers**

If you make changes to the Dockerfile or dependencies, use this command:

```bash
docker-compose up --build
```

### Manual Installation

**1. Set Up Virtual Environment**

```bash
virtualenv venv
source venv/bin/activate
```

**2. Install Dependencies**

```bash
pip install -r requirements.txt
```

**3. Configure the Database**

Update the `DATABASES` setting in `settings.py` to match your database configuration.

**4. Apply Migrations**

```bash
python manage.py migrate
```

**5. Create Superuser**

```bash
python manage.py createsuperuser
```

**6. Run the Development Server**

```bash
python manage.py runserver
```

## Usage

**1. Access the Application**

Open your web browser and navigate to http://localhost:8000.

**2. Login**

Use the credentials of the superuser created during installation to log in.

**3. Explore Features**

Navigate through the various sections of the application, including planning, reconnaissance, exploitation, post-exploitation, and reporting.

**4. Educational Resources**

Access tutorials and guides from the "Resources" section to enhance your learning experience in ethical hacking.

## Contributing

We welcome contributions from the community! Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch (e.g., `git checkout -b feature-branch`).
3. Make your changes and commit them (e.g., `git commit -m 'Add new feature'`).
4. Push to the branch (e.g., `git push origin feature-branch`).
5. Create a pull request detailing your changes.

## License

This project is licensed under the MIT License. See the LICENSE file for more information.

## Acknowledgments
We would like to thank the open-source community for providing the tools and resources that made this project possible.

## Contact
For any questions or inquiries, please contact us at:
Email: vonghoangvinh1989@gmail.com
GitHub: https://github.com/vonghoangvinh1989/yellow_hat