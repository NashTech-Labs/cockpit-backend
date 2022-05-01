from django.core.mail import send_mail

def get_mail_body(  platform,
                    platform_dns_record=None,
                    guacamole_sharing_url=None
                ):
    try:
        if platform_dns_record is not None and guacamole_sharing_url is not None:
            pass
        else:
            pass
    except Exception as e:
        print("Error in get_mail_body")

