# major: happy
# minor: sad
# Am: A minor, sad
# A: A major, happy
# m: minor
# b: flat (back one key)

harmonic_to_note = {"1b": "B", 
                    "1a": "Abm", 
                    "2b": "F#", 
                    "2a": "Ebm", # e flat or what?  
                    "3b": "Db", 
                    "3a": "Bbm", 
                    "4b": "Ab", 
                    "4a": "Fm", 
                    "5b": "Eb", 
                    "5a": "Cm", 
                    "6b": "Bb", 
                    "6a": "Gm",
                    "7a": "Dm",
                    "7b": "F",
                    "8a": "Am",
                    "8b": "C",
                    "9a": "Em",
                    "9b": "G",
                    "10a": "Bm",
                    "10b": "D",
                    "11a": "F#m",
                    "11b": "A",
                    "12a": "Dbm",
                    "12b": "E",
                    "11a": "Gbm",
                    "2b": "Gb"}


harmonic_to_traktor = {"1b": "6d", 
                    "1a": "6m", 
                    "2b": "7d", 
                    "2a": "7m",
                    "3b": "8d", 
                    "3a": "8m", 
                    "4b": "9d", 
                    "4a": "9m", 
                    "5b": "10d", 
                    "5a": "10m", 
                    "6b": "11d", 
                    "6a": "11m",
                    "7a": "12m",
                    "7b": "12d",
                    "8a": "1m",
                    "8b": "1d",
                    "9a": "2m",
                    "9b": "2d",
                    "10a": "3m",
                    "10b": "3d",
                    "11a": "4m",
                    "11b": "4d",
                    "12a": "5m",
                    "12b": "5d"}

sharp_flat_equivalents = {
        "C#": "Db",
        "D#": "Eb",
        "E#": "F",
        "F#": "Gb",
        "G#": "Ab",
        "A#": "Bb",
        "B#": "C"
    }

harmonic_major_order = ["1B", "2B", "3B", "4B", "5B", "6B", "7B", "8B", "9B", "10B", "11B", "12B"]
harmonic_minor_order = ["1A", "2A", "3A", "4A", "5A", "6A", "7A", "8A", "9A", "10A", "11A", "12A"]
notes_and_flats = ['A', 'Ab', 'B', 'Bb', 'C', 'D', 'Db', 'E', 'Eb', 'F', 'F#', 'G', 'Gb'] 
notes_sharps = ['A', 'Ab', 'B', 'Bb', 'C', 'D', 'Db', 'E', 'Eb', 'F', 'F#', 'G', 'Gb'] 
# major: nothing, minor: m

"""
"2a" should map to "Ebm" which is E-flat minor, so that part is correct.
The "a" side typically represents minor keys, while the "b" side represents major keys.
The "1a" key should be "A minor" (Am) instead of "Abm" which would be "G# minor".
The "12a" key should be "C# minor" (C#m) instead of "Dbm", although they are enharmonically equivalent, the Camelot wheel typically uses "C# minor" for the 12a position.
"""


