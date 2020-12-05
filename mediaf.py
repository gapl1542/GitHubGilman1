from mediafire import MediaFireApi

def media():
    api = MediaFireApi()
    session = api.user_get_session_token(
        email='tesisujappdf@gmail.com',
        password='pdfs2020',
        app_id='42511')

# API client does not know about the token
# until explicitly told about it:
    api.session = session

    response = api.user_get_info()
    print(response['user_info']['display_name'])
    return (response)

    # Or directly for methods that are not yet wrapped
    response = api.request("upload/add_web_upload", {
        "url": "http://forum.mediafiredev.com/images/mfforumlogo.png",
        "filename": "mfforumlogo.png"})

    response = api.request("upload/get_web_uploads",
                    {"key": response['upload_key']})
