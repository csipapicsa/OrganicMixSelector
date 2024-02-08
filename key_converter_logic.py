def empty(input):
    return input == ""

def first_is_number(input):
    return input[0].isdigit()

def last_element(input, isit =["d", "m"]):
    return input[-1] in isit

def traktor_key_to_chamelot(input):
    # converter to do
    None

def note_to_chamelot(input):
    # converter to do
    None

def key_converter(song_note):
    if empty(song_note):
        # Do nothing, do not list the song
        return ""
    else:
        if first_is_number(song_note):
            if last_element(song_note):
                # return the chamelot key
                return traktor_key_to_chamelot(song_note)
            else:
                # return the harmonic note
                return song_note
        else:
            # it is a musical note, need to convert to chamelot
            return note_to_chamelot(song_note)