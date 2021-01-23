import logging


def get_photo_info_from_text(text):
    if len(text.split()) == 3:
        dx, username, link = text.split()
        try:
            photo_id = link.split('/p/')[1].split('/')[0]
            return True, username, photo_id
        except Exception as err:
            logging.exception(err)
            return False, None, None
    else:
        return False, None, None


def get_list_of_photos_from_matrix(matrix_of_photos):
    photos = []
    for list_of_photos in matrix_of_photos:
        for photo in list_of_photos:
            photos.append(photo)

    return photos
