"""Midi Conversion Stuff"""

MAX_MIDI_VALUE = 127


class MidiUtil:

    """Get midi note values"""

    def __init__(self):
        note_names = ["C", "C#", "D", "D#", "E",
                      "F", "F#", "G", "G#", "A", "A#", "B"]
        midi_note = 0
        octave = -1
        # List containing true note names. Index is midi note value for that note.
        self.note_array = []

        self.interval_pattern = {
            "Ionian": [2, 2, 1, 2, 2, 2, 1],
            "Dorian": [2, 1, 2, 2, 2, 1, 2],
            "Mixolydian": [2, 2, 1, 2, 2, 1, 2],
            "Aeolian": [2, 1, 2, 2, 1, 2, 2],
            "Minor Pentatonic": [3, 2, 2, 3, 2],
            "Major Pentatonic": [2, 2, 3, 2, 3],
            "Blues Scale": [3, 2, 1, 1, 3, 2],
            "Major": [4, 3, 5],
            "Minor": [3, 4, 5],
            "Major Seventh": [4, 3, 4, 1],
            "Dominant Seventh": [4, 3, 3, 2],
            "Minor Seventh": [3, 4, 3, 2],
            "I7": [4, 3, 3, 2],
            "IV7": [3, 2, 4, 3]
        }

        self.chord_intervals = {
            "Major": [4, 3, 5],
            "Minor": [3, 4, 5],
            "Major Seventh": [4, 3, 4, 1],
            "Dominant Seventh": [4, 3, 3, 2],
            "Minor Seventh": [3, 4, 3, 2]
        }

        self.mode_root_chord_type = {
            "Ionian": "Major",
            "Dorian": "Minor Seventh",
            "Mixolydian": "Dominant Seventh",
            "Aeolian": "Minor",
            "Minor Pentatonic": "Minor Seventh",
            "Major Pentatonic": "Dominant Seventh",
            "Blues Scale": "Dominant Seventh"
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
        """Return the true note name.  Index to request is the midi note value."""
        return self.note_array[index]

    def get_chord_for_mode(self, mode):
        """Return the correct chord type for mode in question."""
        return self.mode_root_chord_type[mode]

    def build_note_list(self, low_note, high_note, interval, key=None):
        """Build list of midi note values constructed from the defined interval pattern"""

        # Notes are midi values, key is a SANS-octave name string.

        start_note = low_note
        tonic_note = low_note
        return_notes = []
        intervals = self.interval_pattern[interval]
        prepend_intervals = []

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
                    return_notes.append(note)
                    note += step

            for step in intervals:
                if note > high_note:
                    break
                return_notes.append(note)
                note += step

        return return_notes

    def build_from_intervals(self, low_note, interval_type):
        """Build a list of midi note values using intervals, starting at the low midi note value"""

        # Which intervals?
        intervals = self.interval_pattern[interval_type]

        return_notes = []
        note = low_note
        return_notes.append(note)
        for interval in intervals:
            note += interval
            return_notes.append(note)

        return return_notes

    def index(self, note_name):
        """Implement list index function"""

        # Return the midi note value of the full note name.
        return self.note_array.index(note_name)

    def list_of_midi_notes(self, note_name, low_range=-1, high_range=128):
        """Return a list of midi note values for a give note name"""

        note_list = []
        octave = -1
        limit = 9

        if note_name in ["A", "A#", "B"]:
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
        """Some debugging"""
        print(self.note_array[index])

    def print_notes(self):
        """Some debugging"""
        midi_note = 0
        for note_name in self.note_array:
            print("Midi Note: ", midi_note, "Note Name: ", note_name)
            midi_note += 1
