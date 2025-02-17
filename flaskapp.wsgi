import sys
import os

# Add the application directory to the PYTHONPATH
sys.path.insert(0, '/home/ubuntu/ec2FlaskApp/')

from app import app as application  # Adjust this if your app filename is different
