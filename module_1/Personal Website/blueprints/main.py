"""
Main blueprint for the homepage route.
Handles the root route (/) displaying personal information and bio.
"""

from flask import Blueprint, render_template

# Create blueprint for main/homepage routes
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
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
