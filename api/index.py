import sys
import os

# Asegurar que la raiz del proyecto este en el PATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app
