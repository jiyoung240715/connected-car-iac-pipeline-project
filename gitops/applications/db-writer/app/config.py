import os


class Settings:
    # RabbitMQ
    RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "192.168.10.36")
    RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT", "5672"))
    RABBITMQ_USER = os.getenv("RABBITMQ_USER", "admin")
    RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD", "654321")
    RABBITMQ_VHOST = os.getenv("RABBITMQ_VHOST", "/")

    QUEUE_POSITION = os.getenv("QUEUE_POSITION", "v2x.vehicle.position")
    QUEUE_STATUS = os.getenv("QUEUE_STATUS", "v2x.vehicle.status") 

    PREFETCH_COUNT = int(os.getenv("PREFETCH_COUNT", "20"))

    MYSQL_HOST = os.getenv("MYSQL_HOST", "172.16.10.25")
    MYSQL_PORT = int(os.getenv("MYSQL_PORT", "3306"))
    MYSQL_USER = os.getenv("MYSQL_USER", "user5")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "1234")
    MYSQL_DB = os.getenv("MYSQL_DB", "cits_data")
    MYSQL_POOL_MIN = int(os.getenv("MYSQL_POOL_MIN", "2"))
    MYSQL_POOL_MAX = int(os.getenv("MYSQL_POOL_MAX", "10"))

    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")


settings = Settings()
