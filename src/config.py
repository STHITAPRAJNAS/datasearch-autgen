import yaml
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    bedrock_client: str
    model_id: str
    embedding_model_id: str
    database_host: str
    database_port: str
    database_user: str
    database_password: str
    database_name: str
    log_level: str
    
    model_config = SettingsConfigDict(env_file=".env")

def load_config(config_file="config.yaml"):
    """Load configuration from a YAML file."""
    with open(config_file, 'r') as f:
        config = yaml.safe_load(f)
    return config

# Load configuration
config = load_config()

# Create settings object
settings = Settings(
    bedrock_client=config['bedrock']['client'],
    model_id=config['bedrock']['model_id'],
    embedding_model_id=config['bedrock']['embedding_model_id'],
    database_host=config['database']['host'],
    database_port=config['database']['port'],
    database_user=config['database']['user'],
    database_password=config['database']['password'],
    database_name=config['database']['name'],
    log_level=config['application']['log_level'],
)

settings = Settings()