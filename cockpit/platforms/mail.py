from django.core.mail import send_mail

def __get_message_body(  platform,user_name,
                    platform_dns_record=None,
                    guacamole_sharing_url=None
                ):
    try:
        if platform_dns_record is not None and guacamole_sharing_url is not None:
            message="""Dear {1},\nRequested for Platform {0}.\n\n{0} URL: {2}.\nServer Access URL: {3}.\n\nRegards\nCockpit Team\nKnoldus Inc""".format(platform,user_name,platform_dns_record,guacamole_sharing_url)
            return message
        else:
            message ="""Dear {0},\nYour Request was not processed please contact Cockpit Support Team.\n\nRegards\nCockpit Team\nKnoldus Inc""".format(user_name)
            return message
    except Exception as e:
        print("Error in get_mail_body {}".format(e))
        message ="""Dear {0},\nYour Request was not processed please contact Cockpit Support Team.\n\nRegards\nCockpit Team\nKnoldus Inc""".format(user_name)
        return message        
        
def send_cockpit_mail(details):
    try:
        platform=details['platform']
        user_name=details['user_name']
        platform_dns_record=details['platform_dns_record']
        guacamole_sharing_url=details['guacamole_sharing_url']
        user_email=details['user_email']
        message=__get_message_body(
            platform,
            user_name,
            platform_dns_record,
            guacamole_sharing_url
        )
        exit_status=send_mail(
            "Cockpit Platform Details",
            message,
            None,
            ['{}'.format(user_email)],
            fail_silently=False
            )
        if exit_status == 1:
            print("Mail sent Successfull")
    except Exception as e:
        print("Error sending cockpit mail\n{}".format(e))