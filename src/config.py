from sqlalchemy import create_engine
import os

class Config:
    TESTING = False
    DEBUG = False
    DATABASE_URL = os.getenv("postgresql://neondb_owner:npg_sjlh74tPTLYE@ep-steep-snow-adfay1a5-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require")

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True

class ProductionConfig(Config):
    pass

config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}
