"""
Projects blueprint for the projects/publications route.
Handles the /projects route displaying M1 project information.
"""

from flask import Blueprint, render_template

# Create blueprint for projects routes
projects_bp = Blueprint('projects', __name__)

@projects_bp.route('/projects')
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
