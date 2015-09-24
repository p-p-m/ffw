def send_emails_on_order_creation(sender, instance=None, created=False, **kwargs):
    if created:
        instance.send_customer_email()
        instance.send_admin_email()
