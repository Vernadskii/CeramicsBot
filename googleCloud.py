from gphotospy.album import *
from gphotospy.media import *
def listOfLinks(str):
    from gphotospy import authorize
    CLIENT_SECRET_FILE = "googleKey.json"
    service = authorize.init(CLIENT_SECRET_FILE)
    album_manager = Album(service)
    album_iterator = album_manager.list()
    first_album = next(album_iterator)
    try:
        while first_album.get("title") != str:
            first_album = next(album_iterator)
    except:
        print('Error, check name of folders in cloud!')
    media_manager = Media(service)
    album_media_list = list(media_manager.search_album(first_album.get('id'))) #get a list of all media present in the album
    result = []
    for media in album_media_list:
        result.append([media.get("baseUrl"), media.get("description")])
    return result

print(listOfLinks("Vases"))