from api.models.track import Track


class TrackRepository:

    @staticmethod
    def add_track(track):
        return track.save()

    @staticmethod
    def get_track_by_name(value):
        track = Track.objects(name=value)
        return track

    @staticmethod
    def delete_all_track():
        Track.objects().delete()

    @staticmethod
    def get_all_tracks():
        return Track.objects()

    @staticmethod
    def get_statistics(group={}, match={}):
        pipeline = []

        if len(match) > 0:
            pipeline.append({"$match": match})

        if len(group) > 0:
            pipeline.append({"$group": group})

        return Track.objects().aggregate(pipeline)