import spotipy
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv


load_dotenv()

client_id = os.environ.get('CLIENT_ID')
client_secret = os.environ.get('CLIENT_SECRET')


auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(auth_manager=auth_manager)


artist_id = "00FQb4jTyendYWaN8pK0wa"
response = sp.artist_top_tracks(artist_id)

filtered_tracks = []


if response and "tracks" in response:
    tracks = response["tracks"]

    
    filtered_tracks = []

    
    for track in tracks:
        
        track_info = {}

        
        for k, v in track.items():
            # Verifica si la clave es una de las que nos interesa
            if k in ["name", "popularity", "duration_ms"]:
                
                if k == "duration_ms":
                    track_info[k] = (v / (1000 * 60)) % 60
                else:
                    track_info[k] = v
        
        filtered_tracks.append(track_info)

    
    tracks = filtered_tracks

   
    print(tracks)

else:
    print("Error: No se pudo obtener las canciones principales del artista o la respuesta no contiene 'tracks'.")




tracks_df = pd.DataFrame.from_records(tracks)
tracks_df.sort_values(["popularity"], inplace = True)

print(tracks_df.head(3))



scatter_plot = sns.scatterplot(data = tracks_df, x = "popularity", y = "duration_ms")
fig = scatter_plot.get_figure()
fig.savefig("scatter_plot.png")