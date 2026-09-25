def recommend_method(media_type):

    if media_type == "HDD":
        return "Overwrite-Based Sanitization"

    elif media_type == "SSD/NVMe":
        return "SSD-Appropriate Sanitization"

    elif media_type == "USB/Flash":
        return "Flash-Media Sanitization"

    elif media_type == "Memory Card":
        return "Flash-Media Sanitization"

    elif media_type == "Disk Image":
        return "Controlled Sanitization"

    elif media_type == "ISO Image":
        return "Controlled Sanitization"

    else:
        return "Do Not Sanitize"