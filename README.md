# IvyNet: Ivy League Opportunity Intelligence & Student Competency Network

IvyNet is an AI-driven real-time system designed to bridge the gap between students and high-quality Ivy League opportunities. It features a personalized opportunity feed, an intelligent competency scoring system (InCoScore), and a social academic community.

## Core Features
1. **Real-Time Opportunity Extraction**: Continuously monitors and extracts live updates from Ivy League platforms like Harvard, Yale, and UPenn using integrated web scrapers.
2. **AI-Based Domain Classification**: Automatically categorizes opportunities into domains like AI, Law, and Engineering using NLP-inspired keyword analysis.
3. **InCoScore Ranking Engine**: A unique scoring algorithm that ranks students based on their achievements (hackathons, internships, research).
4. **Student Academic Social Network**: A platform for networking, sharing achievements, and professional interaction.
5. **Personalized Feed**: Smart recommendations based on student performance and interests.

## Tech Stack
- **Backend**: Django 5.x
- **Frontend**: Vanilla CSS (Premium Glassmorphism), Bootstrap 5, Google Fonts (Outfit)
- **Intelligence**: Python-based Scraper Simulation & Rule-based NLP Classifier

## How to Run
1. **Install Dependencies**:
   ```bash
   pip install django beautifulsoup4 requests django-bootstrap5
   ```
2. **Setup Database**:
   ```bash
   python manage.py makemigrations accounts opportunities community
   python manage.py migrate
   ```
3. **Create Superuser**:
   ```bash
   python manage.py createsuperuser
   ```
4. **Start Server**:
   ```bash
   python manage.py runserver
   ```
5. **Access the App**: Open [http://127.0.0.1:8000](http://127.0.0.1:8000)

## Project Structure
- `accounts/`: User profiles, achievement logging, and InCoScore logic.
- `opportunities/`: Opportunity scraping, intelligent classification, and application system.
- `community/`: Social feed, posts, likes, and academic networking.
- `static/css/style.css`: Premium dark-themed design system.
