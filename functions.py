from dictionaries import harmonic_to_traktor, harmonic_major_order, harmonic_minor_order
import pandas as pd
import xml.etree.ElementTree as ET

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
    if note[1] == "b":
        prev_key_index = (harmonic_major_order.index(note) - 1) % len(harmonic_major_order)
        next_key_index = (harmonic_major_order.index(note) + 1) % len(harmonic_major_order)
        index = harmonic_major_order.index(note)
        return harmonic_major_order[prev_key_index], harmonic_major_order[next_key_index], harmonic_minor_order[index]
    elif note[1] == "a":
        prev_key_index = (harmonic_minor_order.index(note) - 1) % len(harmonic_minor_order)
        next_key_index = (harmonic_minor_order.index(note) + 1) % len(harmonic_minor_order)
        index = harmonic_minor_order.index(note)
        return harmonic_minor_order[prev_key_index], harmonic_minor_order[next_key_index], harmonic_major_order[index]
    else:
        return None, None
    
print(get_classic_neighbours("6a"))

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

  # Extract key name and determine if minor
  base_key = key_names[nml_key % 12]
  is_minor = nml_key // 12 > 0

  # Return key name with optional "m" for minor
  return base_key + ("m" if is_minor else "")

def load_songs_from_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    # List to hold all song entries
    songs_list = []
    
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
        
        bpm = temp.get('BPM') if temp is not None else None
        
        musical_key_int = musical_key.get('VALUE') if musical_key is not None else ""
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
            'Artist': artist,
            'Title': title,
            'File_Path': full_path,
            'Play_Count': play_count,
            'Comment': comment,
            'BPM': bpm,
            'Musical_Key_Int': musical_key_int,
            'Color': color,
            'Musical_Key': nml_key_int_to_name(int(musical_key_int)) if musical_key_int else ""
        }
        songs_list.append(song_dict)
    
    # Convert the list of dictionaries to a DataFrame
    df_songs = pd.DataFrame(songs_list)

    # TODO doesnt take to much time, so just keep it for now
    df_songs.dropna(subset=['Artist', 'Title'], how='all', inplace=True)  # Drop rows where both Artist and Title are missing
    
    return df_songs

def random_sample_df(df, n_samples, random_state=None):
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

t = reverse_dictionary(harmonic_to_traktor)
print(t)
print(t["6d"])

