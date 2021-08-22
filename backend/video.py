from datetime import datetime
from flask import make_response, abort
from models import Video, VideoSchema
from config import db
from sqlalchemy import exc


def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))


# Create a handler for our read (GET) people
def read_all():
    """
    This function responds to a request for /api/all_videos
    with the complete lists of videos

    :return:        list of videos
    """
    videos = Video.query.all()

    video_schema = VideoSchema(many=True)
    return video_schema.dump(videos)


def read_one(videoname):
    """
    This function responds to a request for /api/videos/{videoname}
    with one matching video from videos
    :param videoname:   videoname of video to find
    :return:        video matching videoname
    """
    video = Video.query.filter_by(videoname=videoname).first()
    video_schema = VideoSchema(many=False)
    if video:
        return video_schema.dump(video)
    else:
        # otherwise, nope, not found
        abort(
                404, f"Video with videoname {videoname} not found"
            )     

    
def create(video):
    """
    This function creates a new video in the video structure
    based on the passed in video data
    :param video:  video to create in video structure
    :return:        201 on success, 406 on video exists
    """
    date = video.get("date", None)
    thumbnail_photo = video.get("thumbnail_photo", None)
    time = video.get("time", None)
    videoname = video.get("videoname", None)

    try:
        video = Video(date=date, thumbnail_photo=thumbnail_photo, time=time, videoname=videoname)
        db.session.add(video)
        db.session.commit()
    except exc.IntegrityError:
        abort(
                400, f"Video with videoname {videoname} or with the thumbnail_photo {thumbnail_photo} already exsists"
            ) 

    return make_response(f"{videoname} successfully created", 201)

    
def update(videoname, video):
    """
    This function updates an existing video in the video structure
    :param videoname:   videoname of video to update in the video structure
    :param video:  video to update
    :return:        updated video structure
    """
    video_to_change = Video.query.filter_by(videoname=videoname).first()

    # Does the video exist in videos?
    if video:
        video_to_change.date = video.get("date", None)
        video_to_change.thumbnail_photo = video.get("thumbnail_photo", None)
        video_to_change.time = video.get("time", None)
        video_to_change.videoname = video.get("videoname", None)

        db.session.commit()

        return video
    else:
        # otherwise, nope, not found
        abort(
            404, f"Video with videoname {videoname} not found"
        ) 

    
def delete(videoname):
    """
    This function deletes a video from the video structure
    :param videoname:   videoname of video to delete
    :return:        200 on successful delete, 404 if not found
    """
    video = Video.query.filter_by(videoname=videoname).first()

    if video:
        db.session.delete(video)
        db.session.commit()
        return make_response(f"{videoname} successfully deleted")  
    else:
        # Otherwise, nope, video to delete not found
        abort(
            404, f"Video with videoname {videoname} not found"
        )