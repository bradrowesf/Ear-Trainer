"""Guitar Conversion Stuff"""


class GuitarUtil:

    """Covert stuff as relates to the guitar"""

    def __init__(self):

        # Define string names
        self.guitar_strings = ["E", "B", "G", "D", "A", "E"]

        # A list of lists of each full note (INCLUDING OCTAVE) name for each guitar string.
        # Index: 0 - High E; 5 - Low E.
        self.guitar_full_notes = []
        self.guitar_notes = []  # Same as above, but just the names -- NO OCTAVE IDENTIFICATION

        note_names = ["C", "C#", "D", "D#", "E",
                      "F", "F#", "G", "G#", "A", "A#", "B"]

        # The starting octave for each string.
        string_octaves = [4, 3, 3, 3, 2, 2]

        # The starting note for string in the note_names list
        # The index values in note_names list.
        string_note_cycle_start = [4, 11, 7, 2, 9, 4]

        for guitar_string in range(0, 6):

            octave = string_octaves[guitar_string]
            note_name_offset = string_note_cycle_start[guitar_string]

            full_string_notes = []
            string_notes = []

            for fret in range(0, 23):   # 23 so that we define the 22 fret.

                # Get the right index for the string/fret pair
                note_name_index = (fret + note_name_offset) % len(note_names)

                if note_name_index == 0:
                    # We're on C, next octave
                    octave += 1

                full_note_name = note_names[note_name_index] + str(octave)

                full_string_notes.append(full_note_name)
                string_notes.append(note_names[note_name_index])

            self.guitar_full_notes.append(full_string_notes)
            self.guitar_notes.append(string_notes)

    def get_string_from_number(self, number):
        """Get name for string number"""

        # It's a 6 string guitar
        if number < 1 or number > 6:
            raise ValueError

        # Normal string numbering convention (i.e. High E string is 1; Low E is 6)

        return_string = ""
        if number == 1:
            return_string = "High "
        elif number == 6:
            return_string = "Low "

        return_string += self.guitar_strings[number - 1]

        return return_string

    def get_string_from_reverse_number(self, number):
        """Get name from zero based index"""

        # String numbering only a computer would do (i.e. Low E string is 0; High E is 5)

        true_number = 6 - number
        return self.get_string_from_number(true_number)

    def get_full_note_name(self, string, fret):
        """Return the text string name of a note INCLUDING ocatve"""
        # Normal human string and fret numbering convention

        guitar_string = self.guitar_full_notes[string - 1]
        note_name = guitar_string[fret]

        return note_name

    def get_note_name(self, string, fret):
        """Just the note name, SANS octave"""
        # Normal human string and fret numbering convention

        guitar_string = self.guitar_notes[string - 1]
        note_name = guitar_string[fret]

        return note_name

    def get_lowest_full_note_on_string(self, note, string):
        """Basically find octave of the lowest of a particular note on a string"""
        # note is the SANS-octave name.  Return the full note name WITH octave.

        # Find the lowest note
        guitar_string = self.guitar_notes[string - 1]
        fret = guitar_string.index(note)

        # Now look at the full note name list.
        guitar_string = self.guitar_full_notes[string - 1]

        return guitar_string[fret]

    def get_fret_from_full_note_name(self, full_note_name, string):
        """Get the fret/position for the note on string in question"""

        # String should be human numbered so change to zero based index.
        guitar_string = self.guitar_full_notes[string - 1]

        return guitar_string.index(full_note_name)

    def get_fret_string_from_name(self, full_note_name,
                                  low_fret_range=0, high_fret_range=22,
                                  high_string=1, low_string=6):
        """Find all the string/fret pairings from a full note name"""

        # Convert human string numbers to list index values
        high_string_limit = high_string - 1
        low_string_limit = low_string - 1

        # The list we're going to populate [Fret, String]
        fret_string = []

        for idx, guitar_string_notes in enumerate(self.guitar_full_notes):

            # Remember low string has a high index and vice versa
            if high_string_limit <= idx <= low_string_limit:
                try:
                    # Find the note on the string and if it's there add it to the return list
                    fret = guitar_string_notes.index(full_note_name)
                    if low_fret_range <= fret <= high_fret_range:
                        fret_string.append(
                            [fret, self.get_string_from_number(idx+1)])
                except ValueError:
                    pass    # This is fine.

        return fret_string
