from random import randrange

def get_audio_file():
    intervals =[
        {"interval": MAJOR_SECOND, "audio_files": ["Major_2-A-B+.mp3", "Major_2-D-E+.mp3", "Major_2-G%23-A%23.mp3"]},
        {"interval": MINOR_SECOND, "audio_files": ["Minor_2-A-B-flat+.mp3", "Minor_2-C-C%23+.mp3", "Minor_2-F-F%23+.mp3"]},
        {"interval": MAJOR_THIRD, "audio_files": ["Major_3-D-F%23+.mp3", "Major_3-F%23-A%23.mp3", "Major_3-G-B+.mp3"]}, 
        {"interval": MINOR_THIRD, "audio_files": ["Minor_3-C%23-E.mp3", "Minor_3-F%23-A.mp3", "Minor_3-G%23-B+.mp3"]},
        {"interval": PERFECT_FOURTH, "audio_files": ["Perfect_4-A-D.mp3", "Perfect_4-D-G.mp3", "Perfect_4-F-B-flat.mp3", "Perfect_4-G%23-C%23.mp3"]}, 
        {"interval": PERFECT_FIFTH, "audio_files": ["Perfect_5-D-A.mp3", "Perfect_5-E-B.mp3", "Perfect_5-F%23-C%23.mp3"]}, 
        {"interval": TRITONE, "audio_files": ["Tritone_D-G%23.mp3", "Tritone_E-A%23.mp3", "Tritone_F-B.mp3"]}, 
        {"interval": MAJOR_SIXTH, "audio_files": ["Major_6-C%23-A%23.mp3", "Major_6-D-B.mp3", "Major_6-D-B.mp3"]}, 
        {"interval": MINOR_SIXTH, "audio_files": ["Minor_6-C-A-flat.mp3", "Minor_6-D-flat-A.mp3", "Minor_6-E-C.mp3", "Minor_6-F-D-flat.mp3"]}, 
        {"interval": MINOR_SEVENTH, "audio_files": ["Minor_7-E-D.mp3", "Minor_7-E-flat-D-flat.mp3", "Minor_7-F-E-flat.mp3"]}, 
        {"interval": MAJOR_SEVENTH, "audio_files": ["Major_7-C-B.mp3", "Major_7-E-flat-D.mp3", "Major_7-F-E.mp3"]}, 
        {"interval": OCTAVE, "audio_files": ["Octave_C-C.mp3", "Octave_D-D.mp3", "Octave_E-E.mp3"]}, 

    ]

    idx = randrange(0, len(intervals))
    interval = intervals[idx]
    audio_idx = randrange(0, len(interval['audio_files']))
    audio = interval['audio_files']
    random_file = audio[audio_idx]
    url = f"https://cohort-6-intervals.s3.amazonaws.com/{random_file}" 
    return url

