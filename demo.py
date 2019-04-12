from api import Api
from time import sleep
import sys
import os
import shutil
import json
#import wget


def update_dir(directory):
    if os.path.exists(directory):
        shutil.rmtree(directory)
    os.mkdir(directory)


MAX_VIDS_PER_TAG = 500
SECS_TO_SLEEP_BETWEEN_VIDEOS = 2
SECS_TO_SLEEP_BETWEEN_BATCHES = 2
#VIDEOS_DIR = "/Users/icecream/tiktok_download/download/videos"
#INFOS_DIR = "/Users/icecream/tiktok_download/download/infos"
#TAGS_DIR = "/Users/icecream/tiktok_download/download/tags"
TAGS_DIR = "/Users/onaga/Documents/Pasheda_likes_football/download_tiktok/Leshka_best_proger_ever"


htag_list = [
    "streetstyle",
    "streetsnap",
    "sneakerheads",
    "sneakerhead",
    "sashatattooing",
    "hypebeast",
    "fashionupcycling",
    "fashionprediction",
    "fashionismyprofession",
    "fashionismypassion",
    "fashioninyears",
    "cutecouple",
    "badgemestyle",
    "ausaltmachneu",
    "стиль",
    "моднаяобложка2019",
    "лучшеевстиле",
    "лучшеевбьюти",
    "1mlifestyle",
    "1mfashioneu",
    "1mfashion"
]


def dump_json(data, name):
    with open(name, 'w') as f:
        json.dump(data, f)


def login_(login):
    if (login.get('code')):
        from capthca import capthca
        cc = capthca(login.get('code'))
        if (cc.backdata):
            if (len(cc.backdata) > 0):
                login = Api.login(username, password, cc.backdata)
                del cc
                login_(login)
        else:
            print('empty form again')
            login = Api.login(username, password, cc.backdata)
            del cc
            login_(login)

if __name__ == "__main__":
    api = Api()

    api.global_variable['device_id'] = "6648944787888948741"
    api.global_variable['iid'] = "6648944787888948741"
    api.global_variable['openudid'] = "6vchx2vx3ubd051q"

    offset = 0

    for tag in htag_list:
        challenges_json = api.search_hashtag(text=tag)
        dump_json(challenges_json, "challenges_json.json")
        cid = challenges_json["challenge_list"][0]["challenge_info"]["cid"]

        #tagVideosFolder = os.path.join(VIDEOS_DIR, tag)
        #tagInfosFolder = os.path.join(INFOS_DIR, tag)
        tagsFolder = os.path.join(TAGS_DIR, tag)
        #update_dir(tagVideosFolder)
        #update_dir(tagInfosFolder)
        update_dir(tagsFolder)

        counter = 0
        while True:
            print("Take batch for hashtag {} number {}".format(tag, counter))
            tag_videos = api.list_hashtag(cid=cid, count=15, offset=offset)
            dump_json(tag_videos, os.path.join(tagsFolder, str(counter)))
            vids = tag_videos["aweme_list"]

            '''
            for vid in vids:
                video_id = vid["aweme_id"]
                url = vid["video"]["play_addr"]["url_list"][0]
                sleep(SECS_TO_SLEEP_BETWEEN_VIDEOS )
                wget.download(url, out=os.path.join(tagVideosFolder, "{}.mp4".format(video_id)))
                dump_json(vid, os.path.join(tagInfosFolder, video_id))
                print(" -> Downloaded video {} for hashtag {}".format(video_id, tag))
            '''

            sleep(SECS_TO_SLEEP_BETWEEN_BATCHES)

            offset = offset + len(vids) + 1
            counter += 1

            if tag_videos["has_more"] == 0 or offset > MAX_VIDS_PER_TAG:
                break
