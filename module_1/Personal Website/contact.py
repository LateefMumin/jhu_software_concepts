"""
Contact blueprint for the contact information route.
Handles the /contact route displaying email and LinkedIn information.
"""

from flask import Blueprint, render_template

# Create blueprint for contact routes
contact_bp = Blueprint('contact', __name__)

@contact_bp.route('/contact')
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
