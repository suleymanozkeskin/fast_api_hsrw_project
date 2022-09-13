from pydantic import BaseSettings


class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"


settings = Settings()



# we are creating an instance of Settings class  and pydantic will read all of the environment variables listed in the Settings class 
                      # and its going to perform validations 

