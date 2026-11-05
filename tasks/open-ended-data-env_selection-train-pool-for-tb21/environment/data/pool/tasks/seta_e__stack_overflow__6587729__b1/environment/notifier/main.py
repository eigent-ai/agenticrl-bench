from notifier.services.email_service import EmailService
from notifier.utils.text_utils import TextUtils
from notifier.utils.config_loader import ConfigLoader


def main():
    service = EmailService("smtp.example.com", 587)
    message = TextUtils.truncate(
        "Hello, this is a test notification for the system!", 50
    )
    service.send_notification(message)
    print(f"Service: {service.get_service_name()}")
    print(f"Max connections: {ConfigLoader.get_max_connections()}")


if __name__ == "__main__":
    main()
