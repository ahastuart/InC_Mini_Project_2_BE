from flask import Blueprint, jsonify, request
from music.spotify import getPlaylist as getTracks
from music.spotify import search as getPlaylist
from music.youtube import search as getYoutubeId
from music.musicdb import *

# music_bp = Blueprint('music', __name__, url_prefix='/api/music')

# @music_bp.route('/', methods=['GET'])
def get_playlist(dream_id, analysis_result):
    try:
        # dream_id = request.args.get('dream_id')
        # emotion = request.args.get('emotion')
        # keyword = request.args.get('keyword') 
        playlist_id = getPlaylist.main(emotion=analysis_result['sentiment'], keyword=analysis_result['keyword'])
        track_list = getTracks.main(playlist_id)
        
        video_info_list = []

        for track in track_list:
            video_info = getYoutubeId.main(track)
            video_info_list.append({
                'track': track,
                'video_id': video_info[0]['videoId']
            })
            music = MusicDAO.new_music_recommendation(dream_id, track, video_info[0]['videoId'])

        for video in video_info_list:
            print(video)
            
        return video_info_list
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500