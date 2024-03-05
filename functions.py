from dictionaries import harmonic_to_traktor, harmonic_major_order, harmonic_minor_order
import pandas as pd
import xml.etree.ElementTree as ET

from dictionaries import harmonic_to_note

def reverse_dictionary(dictionary):
    """
    Reverse a dictionary, swapping keys and values.
    """
    return {v: k for k, v in dictionary.items()}

def position_of_an_element(note, harmonic_list_1=harmonic_major_order, harmonic_list_2=harmonic_minor_order):
    """
    Given a note, return its position in the harmonic scale.
    """
    if note in harmonic_list_1:
        return harmonic_list_1.index(note)
    elif note in harmonic_list_2:
        return harmonic_list_2.index(note)
    else:
        return None

def get_classic_neighbours(note):
    """
    Given a note, return its classic neighbours.
    """
    if note[-1] == "b":
        prev_key_index = (harmonic_major_order.index(note) - 1) % len(harmonic_major_order)
        next_key_index = (harmonic_major_order.index(note) + 1) % len(harmonic_major_order)
        index = harmonic_major_order.index(note)
        return harmonic_major_order[prev_key_index], harmonic_major_order[next_key_index], harmonic_minor_order[index]
    elif note[-1] == "a":
        prev_key_index = (harmonic_minor_order.index(note) - 1) % len(harmonic_minor_order)
        next_key_index = (harmonic_minor_order.index(note) + 1) % len(harmonic_minor_order)
        index = harmonic_minor_order.index(note)
        return harmonic_minor_order[prev_key_index], harmonic_minor_order[next_key_index], harmonic_major_order[index]
    else:
        return None, None
    
# print(get_classic_neighbours("6a"))

# It will came from the config 
temp_list_of_neighbours = ["+1", "+2", "T0", "T+1"]
temp_distance_in_sound = ["+1", "+2"] # These values will be added to the base case, which could be anything, like 0.4, and so on

def nml_key_int_to_name(nml_key):
  """
  Converts a Traktor NML musical key integer value to a key name,
  including minor keys and handling values up to 12.

  Args:
    nml_key: The Traktor NML musical key integer value (0-12).

  Returns:
    A string containing the key name (e.g., "C", "Cm", "C#m", etc.).
  """

  # Define the key names
  key_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
  key_names = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]

  # Extract key name and determine if minor
  base_key = key_names[nml_key % 12]
  is_minor = nml_key // 12 > 0

  # Return key name with optional "m" for minor
  return base_key + ("m" if is_minor else "")

def load_songs_from_xml(file_path, 
                        note_to_harmonic=reverse_dictionary(harmonic_to_note),
                        bpm_semitone_threshold=0.4):
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    # List to hold all song entries
    songs_list = []
    id = 1
    
    # Iterate over each ENTRY element in the XML tree
    for entry in root.findall(".//ENTRY"):
        # Get the artist and title
        artist = entry.get('ARTIST')
        title = entry.get('TITLE')
        
        # Find the INFO sub-element and extract play count and comment
        info = entry.find('.//INFO')
        temp = entry.find('.//TEMPO')
        musical_key = entry.find('.//MUSICAL_KEY')
        
        play_count = int(info.get('PLAYCOUNT')) if info is not None and info.get('PLAYCOUNT') is not None else ""
        comment = info.get('COMMENT') if info is not None else None
        color = int(info.get('COLOR')) if info is not None and info.get('COLOR') is not None else ""
        
        bpm = float(temp.get('BPM')) if temp is not None else 0
        
        musical_key_int = musical_key.get('VALUE') if musical_key is not None else 0
        musical_key = nml_key_int_to_name(int(musical_key_int)) if musical_key_int else ""
        harmonic_key = note_to_harmonic[musical_key] if musical_key else ""
        bpm_max = calculate_new_tempo(bpm, bpm_semitone_threshold)
        bpm_min = calculate_new_tempo(bpm, -bpm_semitone_threshold)
        # I have no idea why it is not working 
        #musical_key = int(musical_key.get('VALUE')) if musical_key is not None and musical_key.get('VALUE') is not None else 0
        
        # Attempt to get the file path
        try:
            location = entry.find('.//LOCATION')
            file_path = location.get('FILE') if location is not None else None
            dir_path = location.get('DIR').replace(':/','').replace(':','/') if location is not None else None
            full_path = dir_path + file_path if file_path and dir_path else None  # Construct the full file path
        except Exception as e:
            full_path = None
            print("No file path found for", artist, title)
        
        # Create a dictionary for the row entry
        song_dict = {
            'ID': id,
            'Artist': artist,
            'Title': title,
            'File_Path': full_path,
            'Play_Count': play_count,
            'Comment': comment,
            'BPM': int(bpm), # it is really a temporary, since I wanna filter it 
            'BPM_max': bpm_max,
            'BPM_min': bpm_min,
            'Musical_Key_Int': int(musical_key_int),
            'Color': color,
            'Musical_Key': musical_key,
            'Harmonic_Key': harmonic_key,
            'Kind': "Base"
        }
        songs_list.append(song_dict)
        id += 1
    
    # Convert the list of dictionaries to a DataFrame
    df_songs = pd.DataFrame(songs_list)

    # TODO doesnt take to much time, so just keep it for now
    df_songs.dropna(subset=['Artist', 'Title'], how='all', inplace=True)  # Drop rows where both Artist and Title are missing
    # drop files where musical_key_int is 0
    df_songs = df_songs[df_songs['Musical_Key_Int']!= 0]
    return df_songs

def calculate_new_tempo(song_tempo, semitone_change):
    """
    Calculate the new tempo based on the desired semitone change
    """
    new_tempo = song_tempo * (2 ** (semitone_change / 12))
    return float(new_tempo)

def random_sample_df(df, n_samples=0, random_state=None):
  """
  Randomly samples a specified number of rows from a pandas DataFrame.

  Args:
    df: The pandas DataFrame to sample from.
    n_samples: The number of samples to draw.
    random_state: An optional seed for the random number generator.

  Returns:
    A new pandas DataFrame containing the random sample.

  Raises:
    ValueError: If the requested number of samples is greater than the
                number of rows in the DataFrame.
  """

  # Check if the requested number of samples is valid
  if n_samples > len(df):
    raise ValueError("Number of samples cannot be greater than the number of rows in the dataframe.")

  # Sample the dataframe using random sampling
  if n_samples == 0:
    return df
  else:
    return df.sample(n=n_samples, random_state=random_state)

"""

def empty_key(key):
    
    #Given a key, return the empty key.
    
    if key[1] == "b":
        return key.replace("b", "#")
    elif key[1] == "#":
        return key.replace("#", "b")
    else:
        return None

"""
import matplotlib.pyplot as plt
import networkx as nx

def plot_a_graph(G):
    # Draw the graph
    plt.figure(figsize=(15, 15))  # Optional: Sets the size of the figure

    # Use a layout that spreads nodes further apart, like the shell layout
    pos = nx.spring_layout(G)  # Positions nodes using the spring layout algorithm for better visualization
   # Draw nodes with a smaller size and labels with a smaller font size
    nx.draw_networkx_nodes(G, pos, node_size=50, node_color='skyblue', alpha=0.9)
    nx.draw_networkx_labels(G, pos, font_size=8)

    # Draw edges with increased transparency and a thin line
    nx.draw_networkx_edges(G, pos, alpha=0.3, arrows=True, arrowsize=10, edge_color='black', style='dashed')
    plt.title("Directed Graph")
    plt.show()

#t = reverse_dictionary(harmonic_to_traktor)
#print(t)
#print(t["6d"])

def plot_a_graph_2(G):
    # Assuming G is your graph

    # Choose a layout
    pos = nx.spring_layout(G)

    # Draw the graph
    plt.figure(figsize=(15, 15))
    nx.draw_networkx_nodes(G, pos, node_color='skyblue')
    nx.draw_networkx_edges(G, pos, edge_color='black', arrows=True)

    # Draw labels offset from the nodes
    for node, (x, y) in pos.items():
        plt.text(x, y, s=node, horizontalalignment='left', verticalalignment='bottom', fontsize=8)

    plt.title("Directed Graph")
    plt.axis('off')  # Turn off the axis
    plt.show()


def keep_largest_cluster(G):
    # Find the largest connected component
    largest_cc = max(nx.weakly_connected_components(G), key=len)

    # Create a subgraph containing only the largest connected component
    G_largest = G.subgraph(largest_cc).copy()

    return G_largest