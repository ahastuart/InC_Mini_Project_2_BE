import pymysql
from dbconn.DBconn import *

class MusicDAO:
    
    @staticmethod
    def new_music_recommendation(dream_id, song_name, spotify_url):
        cursor = dbconn.get_db().cursor()
    
        try:
            sql = '''
                INSERT INTO music_recommendations
                (dream_id, song_name, spotify_url)
                VALUES (%s, %s, %s);
            '''
            cursor.execute(sql, (dream_id, song_name, spotify_url))
            dbconn.get_db().commit()
            return True
            
        except Exception as e:
            print(f"Error adding music recommendation: {str(e)}")
            dbconn.get_db().rollback()
            return False
            
        finally:
            dbconn.get_db().close()
    