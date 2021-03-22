from email.mime.image import MIMEImage


def email_embed_image(email, img_content_id, img_data):
    """
    Attach Image to email message.
    """
    img = MIMEImage(img_data)
    img.add_header('Content-ID', '<%s>' % img_content_id)
    img.add_header('Content-Disposition', 'inline')
    email.attach(img)
    return email


