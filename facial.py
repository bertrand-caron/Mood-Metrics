from requests import post, get
from json import loads
from pprint import pprint

APP_ID, APP_KEY = '<your_kairos_app_id>', '<your_kairos_app_key>'

HEADERS = {'app_id': APP_ID, 'app_key': APP_KEY}

IMAGE_SOURCE = 'http://scmb-atb.biosci.uq.edu.au/dihedral_data/project_13/{0}.jpg'

if False:
    get_detect = get(
        'https://api.kairos.com/detect',
        headers=HEADERS,
        params=dict(source=IMAGE_SOURCE),
    )

    print(get_detect.text)
    print(get_detect.url)

def satisfaction_for(img_url: str) -> int:
    media_id_request = post(
        'https://api.kairos.com/v2/media',
        headers=HEADERS,
        params=dict(source=image_url)
    )

    media_id = loads(media_id_request.text)['id']

    emotion_request = get(
        'https://api.kairos.com/v2/analytics/{id}'.format(id=media_id),
        headers=HEADERS,
    )

    try:
        emotion_score = loads(emotion_request.text)['impressions'][0]['emotion_score']
        positive, negative = map(lambda key: emotion_score[key], ['positive', 'negative'])
        score = max(0, min(100, 50 + positive - negative))
        assert 0 <= score <= 100, score
        return score
    except:
        return None

IMAGES = ['chris_happy', 'chris_sad', 'krishore_happy', 'krishore_neutral', 'krishore_sad', 'bertrand_happy', 'bertrand_neutral', 'bertrand_sad']

for image_url in map(lambda i: IMAGE_SOURCE.format(i), IMAGES):
    print(satisfaction_for(image_url))

