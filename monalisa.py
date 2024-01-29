from midiutil import MIDIFile

# Create a MIDI file
midi_file = MIDIFile(1)  # 1 track

# Add notes to the track
track = 0
channel = 0
time = 0  # In beats
duration = 1  # In beats
volume = 100  # 0-127
pitch = [60, 62, 64, 65, 67, 69, 71, 72]  # MIDI note numbers (C4 to C5)

for note in pitch:
    midi_file.addNote(track, channel, note, time, duration, volume)
    time += 1  # Move to the next beat

# Save the MIDI file
with open("simple_music.mid", "wb") as midi_file_out:
    midi_file.writeFile(midi_file_out)
