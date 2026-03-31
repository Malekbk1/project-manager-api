import os 
from dotenv import load_dotenv


load_dotenv()

class Config:
    """Classe de configuration pour l'application Flask."""
    
    # Clé secrète pour les sessions et la sécurité
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # Durée de validité des tokens JWT (en secondes)
    
class DevelopmentConfig(Config):
    """Configuration spécifique pour le développement."""
    DEBUG = True    
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")  

class TestingConfig(Config):
    """Configuration spécifique pour les tests."""
    TESTING = True    
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"  # Utilisation d'une base de données en mémoire pour les tests
class ProductionConfig(Config):
    """Configuration spécifique pour la production."""
    DEBUG = False    
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")     

config = {
    "development": DevelopmentConfig,   
    "testing": TestingConfig,
    "production": ProductionConfig,
}              