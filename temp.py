from dictionaries import harmonic_to_note
from TEMP_CONFIG import song_tempo, master_tempo, song_note

import math

def semitones_difference(song_tempo, master_tempo):
    return 12 * math.log2(master_tempo / song_tempo)

def split_semitones_difference(song_tempo, master_tempo):
    difference = semitones_difference(song_tempo, master_tempo)
    integer_part = int(difference)
    decimal_part = difference - integer_part
    return [integer_part, decimal_part]

def calculate_tempo_for_semitones(master_tempo, semitone_difference):
    # Reverse the semitone difference formula to find the song tempo
    return master_tempo / (2 ** (semitone_difference / 12))

def nearest_integer(float_number):
    return round(float_number)


semitone_difference_int, semitone_difference_decimal = split_semitones_difference(song_tempo, master_tempo)
print(semitone_difference_int, semitone_difference_decimal)
base_case_semitone = nearest_integer(semitone_difference_decimal)
print(f"base case for search: {base_case_semitone}")

song_tempo_2 = calculate_tempo_for_semitones(master_tempo, semitone_difference_decimal)
print(song_tempo_2)