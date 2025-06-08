"""
Central routes module for the Flask portfolio website.
Contains all route definitions organized by functionality.
"""

from flask import render_template
from app import app

# Homepage route
@app.route('/')
def index():
    """
    Homepage route displaying personal information, bio, and profile picture.
    Bio text is displayed on the left, image on the right as per requirements.
    """
    # Personal information
    personal_info = {
        'name': 'Lateef Mumin',
        'position': 'Artificial Intelligence Student',
        'bio': '''I am a passionate artificial intelligence student with a strong foundation in 
                 machine learning, data science, and AI technologies. Currently pursuing my degree 
                 while working on various projects that combine technical skills with innovative 
                 problem-solving. I enjoy developing intelligent systems and exploring cutting-edge 
                 AI technologies to create transformative solutions.''',
        'profile_image': 'images/profile.jpg'
    }
    
    return render_template('index.html', 
                         personal_info=personal_info,
                         current_page='home')

# Contact page route
@app.route('/contact')
def contact():
    """
    Contact page route displaying email address and LinkedIn information.
    """
    # Contact information
    contact_info = {
        'email': 'lateefmumin2024@gmail.com',
        'linkedin_url': 'https://www.linkedin.com/in/lateefmumin',
        'linkedin_display': 'www.linkedin.com/in/lateefmumin'
    }
    
    return render_template('contact.html', 
                         contact_info=contact_info,
                         current_page='contact')

# Projects page route
@app.route('/projects')
def projects():
    """
    Projects page route displaying M1 Project GitHub link, title, and details.
    """
    # M1 Project information
    project_info = {
        'title': 'Personal Portfolio Website - M1 Project',
        'github_url': 'https://github.com/LateefMumin/jhu_software_concepts',
        'github_display': 'github.com/LateefMumin/jhu_software_concepts',
        'description': '''This project is a Flask-based personal portfolio website developed as part 
                         of the M1 assignment for Software Concepts course. The application demonstrates 
                         proficiency in web development using Flask framework, HTML templating with Jinja2, 
                         CSS styling with Bootstrap, and modular code organization using Flask blueprints.
                         
                         Key features include a responsive navigation system, professional layout design, 
                         and clean code structure following best practices for maintainability and scalability.''',
        'technologies': ['Flask', 'Python 3.10+', 'HTML5', 'CSS3', 'Bootstrap 5', 'Jinja2 Templates'],
        'features': [
            'Responsive navigation bar with current page highlighting',
            'Professional homepage with bio and profile image',
            'Contact information page with email and LinkedIn',
            'Projects showcase with detailed descriptions',
            'Modular code organization using Flask blueprints',
            'Clean, accessible design with dark theme support'
        ]
    }
    
    return render_template('projects.html', 
                         project_info=project_info,
                         current_page='projects')