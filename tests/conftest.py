import os

os.environ["WORK_ORDER_ENVIRONMENT"] = "test"
os.environ["WORK_ORDER_DATABASE_URL"] = (
    "postgresql+asyncpg://work_order_test:"
    "work_order_test_password@127.0.0.1:5434/work_order_test"
)
