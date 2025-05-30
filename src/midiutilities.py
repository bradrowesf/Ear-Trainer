'''Midi Conversion Stuff'''

MAX_MIDI_VALUE = 127


class MidiUtil:

    '''Get midi note values'''

    def __init__(self):
        note_names = ['C', 'C#', 'D', 'D#', 'E',
                      'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        midi_note = 0
        octave = -1
        # List containing true note names. Index is midi note value for that note.
        self.note_array = []

        self.interval_pattern = {
            'Chromatic': [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            'Ionian': [0, 2, 2, 1, 2, 2, 2, 1],
            'Dorian': [0, 2, 1, 2, 2, 2, 1, 2],
            'Phrygian': [0, 1, 2, 2, 2, 1, 2, 2],
            'Lydian': [0, 2, 2, 2, 1, 2, 2, 1],
            'Mixolydian': [0, 2, 2, 1, 2, 2, 1, 2],
            'Aeolian': [0, 2, 1, 2, 2, 1, 2, 2],
            'Locrian': [0, 1, 2, 2, 1, 2, 2, 2],
            'Minor Pentatonic': [0, 3, 2, 2, 3, 2],
            'Major Pentatonic': [0, 2, 2, 3, 2, 3],
            'Blues Scale': [0, 3, 2, 1, 1, 3, 2],
            'Melodic Minor': [0, 2, 1, 2, 2, 2, 2, 1],
            'Harmonic Minor': [0, 2, 1, 2, 2, 1, 3, 1],
            'Super Locrian': [0, 1, 2, 1, 2, 2, 2, 2],
            'Lydian Dominant': [0, 2, 2, 2, 1, 2, 1, 2],
            'Half-Whole Diminished': [0, 1, 2, 1, 2, 1, 2, 1, 2],
            'Major': [0, 4, 3, 5],
            'Minor': [0, 3, 4, 5],
            'Major Seventh': [0, 4, 3, 4, 1],
            'Dominant Seventh': [0, 4, 3, 3, 2],
            'Minor Seventh': [0, 3, 4, 3, 2],
            'Half Diminished': [0, 3, 3, 4, 2],
            'Fully Diminished': [0, 3, 3, 3, 3],
            'I7': [0, 4, 3, 3, 2],
            'IMaj7': [0, 4, 3, 4, 1],
            'ii7': [0, 2, 3, 4, 3],
            'IV7': [0, 3, 2, 4, 3],
            'V7': [2, 3, 2, 4, 1],
            'biii°7': [0, 3, 3, 3, 3],
            'V°7': [1, 3, 3, 3, 2],
            'vii°7': [2, 3, 3, 3, 1]
        }

        self.intervals = {
            'm2': 1,
            '-m2': -1,
            'M2': 2,
            '-M2': -2,
            'm3': 3,
            '-m3': -3,
            'M3': 4,
            '-M3': -4,
            'P4': 5,
            '-P4': -5,
            'Aug4': 6,
            '-Aug4': -6,
            'P5': 7,
            '-P5': -7,
            'm6': 8,
            '-m6': -8,
            'M6': 9,
            '-M6': -9,
            'm7': 10,
            '-m7': -10,
            'M7': 11,
            '-M7': -11
        }

        self.chord_intervals = {
            'Major': [4, 3, 5],
            'Minor': [3, 4, 5],
            'Major Seventh': [4, 3, 4, 1],
            'Dominant Seventh': [4, 3, 3, 2],
            'Minor Seventh': [3, 4, 3, 2]
        }

        self.mode_root_chord_type = {
            'Ionian': 'Major',
            'Dorian': 'Minor Seventh',
            'Mixolydian': 'Dominant Seventh',
            'Aeolian': 'Minor',
            'Minor Pentatonic': 'Minor Seventh',
            'Major Pentatonic': 'Dominant Seventh',
            'Blues Scale': 'Dominant Seventh'
        }

        # Build the midi note_array
        while midi_note <= MAX_MIDI_VALUE:
            for note_name in note_names:
                if midi_note <= MAX_MIDI_VALUE:
                    true_note_name = note_name + str(octave)
                    self.note_array.append(true_note_name)
                    midi_note += 1

            octave += 1

    def __getitem__(self, index):
        '''Return the true note name.  Index to request is the midi note value.'''
        return self.note_array[index]

    def get_chord_for_mode(self, mode):
        '''Return the correct chord type for mode in question.'''
        return self.mode_root_chord_type[mode]

    def get_semitone_count_for_interval(self, interval):
        '''Return the # of semitones from the interval name'''
        return self.intervals[interval]

    def is_tonic(self, tonic: int, test_note: int) -> bool:
        '''A somewhat common test of whether a particular note is a tonic note.'''

        if ((test_note - tonic) % 12) == 0:
            return True
        return False

    def build_note_list(self, low_note, high_note, intervals_list, key=None):
        '''Build list of midi note values constructed from the defined interval pattern'''

        # Notes are midi values, key is a SANS-octave name string.

        # The list of interval lists that we'll return.
        return_notes_list = []

        # Iterate over each interval list
        for interval_list in intervals_list:
            start_note = low_note
            tonic_note = low_note
            return_notes = []
            prepend_intervals = []
            intervals = self.interval_pattern[interval_list]

            # Determine if the first interval is 0, meaning that the pattern includes the tonic note
            exclude_tonic = intervals[0] != 0

            # Check if we past a key center AND that the key center exists in range.
            if key is not None:
                key_center_notes = self.list_of_midi_notes(key)
                for note in key_center_notes:
                    if low_note <= note <= high_note:
                        # tonic_note now equals lowest tonic note in the range.
                        tonic_note = note
                        break

            # If low_note isn't start_note, that means we're not in the key center of low_note
            if tonic_note != low_note:
                # We need to walk down from this tonic note, to the lowest note in the key in range
                note = tonic_note
                reversed_intervals = list(reversed(intervals))
                while note >= low_note:
                    for step in reversed_intervals:
                        if note >= low_note:
                            start_note = note           # New starting note
                            note -= step
                            if note >= low_note:
                                # Add an interval
                                prepend_intervals.insert(0, step)
                        else:
                            break

            note = start_note

            first_time = True
            while note <= high_note:
                # Do notes below tonic first (but only first time).
                if first_time:
                    first_time = False
                    for step in prepend_intervals:
                        if note > high_note:
                            break

                        # If the pattern doesn't include tonics and this is tonic, don't add it.
                        if not (exclude_tonic and self.is_tonic(tonic_note, note)):
                            return_notes.append(note)
                        note += step

                for step in intervals:

                    # If step is zero, skip it.
                    if step == 0:
                        continue

                    if note > high_note:
                        break

                    # If the pattern doesn't include tonics and this is tonic, don't add it.
                    if not (exclude_tonic and self.is_tonic(tonic_note, note)):
                        return_notes.append(note)
                    note += step

            # List complete, let's append it to the return list
            return_notes_list.append(return_notes)

        return return_notes_list

    def build_from_intervals(self, low_note, interval_type):
        '''Build a list of midi note values using intervals, starting at the low midi note value'''

        # Which intervals?
        intervals = self.interval_pattern[interval_type]

        # Determine if the first interval is 0, meaning that the pattern includes the tonic note
        exclude_tonic = intervals[0] != 0

        return_notes = []
        note = low_note
        # return_notes.append(note)
        for interval in intervals:
            note += interval
            if not (exclude_tonic and self.is_tonic(low_note, note)):
                return_notes.append(note)

        return return_notes

    def index(self, note_name):
        '''Implement list index function'''

        # Return the midi note value of the full note name.
        return self.note_array.index(note_name)

    def list_of_midi_notes(self, note_name, low_range=-1, high_range=128):
        '''Return a list of midi note values for a give note name'''

        note_list = []
        octave = -1
        limit = 9

        if note_name in ['G#', 'A', 'A#', 'B']:
            limit = 8

        while octave <= limit:
            note_to_find = note_name + str(octave)
            note_to_add = self.index(note_to_find)

            # Only capture it if it's in our range
            if low_range < note_to_add < high_range:
                note_list.append(self.index(note_to_find))

            octave += 1

        return note_list

    def midi_to_note(self, index):
        '''Some debugging'''
        print(self.note_array[index])

    def print_notes(self):
        '''Some debugging'''
        midi_note = 0
        for note_name in self.note_array:
            print('Midi Note: ', midi_note, 'Note Name: ', note_name)
            midi_note += 1
