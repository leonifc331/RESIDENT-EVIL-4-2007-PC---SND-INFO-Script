import tkinter as tk
from tkinter import filedialog
import struct

class SNDInfoEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("RESIDENT EVIL 4 2007 PC - SND Editor By RE-Play Games")
        self.root.geometry("800x600")

        self.current_file = None
        self.sound_info = None
        self.current_group = 1
        self.current_entry = 0

        self.audio_names = {}
        self.progression_names = {}

        self.create_widgets()

    def create_widgets(self):
        self.browse_button = tk.Button(self.root, text="Select File", command=self.load_file)
        self.browse_button.pack(pady=10)

        self.load_audio_progression_file_button = tk.Button(self.root, text="Load Audio Progression File", command=self.load_audio_progression_file)
        self.load_audio_progression_file_button.pack(pady=10)

        self.group_navigation_frame = tk.Frame(self.root)
        self.group_navigation_frame.pack(pady=10)

        self.prev_group_button = tk.Button(self.group_navigation_frame, text="Previous Group", command=self.prev_group)
        self.prev_group_button.grid(row=0, column=0, padx=5)

        self.next_group_button = tk.Button(self.group_navigation_frame, text="Next Group", command=self.next_group)
        self.next_group_button.grid(row=0, column=1, padx=5)

        self.entry_navigation_frame = tk.Frame(self.root)
        self.entry_navigation_frame.pack(pady=10)

        self.prev_entry_button = tk.Button(self.entry_navigation_frame, text="Previous Sound Entry", command=self.prev_entry)
        self.prev_entry_button.grid(row=0, column=0, padx=5)

        self.next_entry_button = tk.Button(self.entry_navigation_frame, text="Next Sound Entry", command=self.next_entry)
        self.next_entry_button.grid(row=0, column=1, padx=5)

        self.save_button = tk.Button(self.root, text="Save File", command=self.save_file)
        self.save_button.pack(pady=10)

        self.info_frame = tk.Frame(self.root)
        self.info_frame.pack(pady=20)

        self.entry_info_labels = []
        self.entry_info_entries = []

        # Campo para exibir o número da entrada
        self.entry_num_label = tk.Label(self.info_frame, text="Sound Entry Number:")
        self.entry_num_label.grid(row=11, column=0, padx=5, pady=5)
        self.entry_num_var = tk.StringVar()
        self.entry_num_var.set("")
        self.entry_num_display = tk.Label(self.info_frame, textvariable=self.entry_num_var)
        self.entry_num_display.grid(row=11, column=1, padx=5, pady=5)

        # Campo para exibir o nome da progressão da sound entry selecionada
        self.progression_name_label = tk.Label(self.info_frame, text="Progression Name:")
        self.progression_name_label.grid(row=12, column=0, padx=5, pady=5)
        self.progression_name_var = tk.StringVar()
        self.progression_name_var.set("")
        self.progression_name_display = tk.Label(self.info_frame, textvariable=self.progression_name_var)
        self.progression_name_display.grid(row=12, column=1, padx=5, pady=5)

        # Campo para exibir o nome do audio id da sound entry selecionada
        self.audio_name_label = tk.Label(self.info_frame, text="Audio Name:")
        self.audio_name_label.grid(row=13, column=0, padx=5, pady=5)
        self.audio_name_var = tk.StringVar()
        self.audio_name_var.set("")
        self.audio_name_display = tk.Label(self.info_frame, textvariable=self.audio_name_var)
        self.audio_name_display.grid(row=13, column=1, padx=5, pady=5)

    def load_file(self):
        filename = filedialog.askopenfilename(filetypes=[("SND files", "*.snd")])
        if filename:
            self.current_file = filename
            self.sound_info = self.extract_info(self.current_file)
            self.current_group = 1
            self.current_entry = 0
            self.display_info()

    def load_audio_progression_file(self):
        filename = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if filename:
            try:
                with open(filename, 'r') as file:
                    current_progression_id = None
                    for line in file:
                        line = line.strip()
                        if line.startswith("Progressão ID"):
                            current_progression_id = int(line.split(':')[0].split()[-1])
                            progression_name = line.split(':')[-1].strip()
                            self.progression_names[current_progression_id] = progression_name
                        elif line.startswith("SND audio ID"):
                            audio_id, audio_name = line.split(':')
                            audio_id = int(audio_id.split()[-1])
                            audio_name = audio_name.strip()
                            self.audio_names[audio_id] = audio_name
                print("Audio progression file loaded successfully!")
                self.update_progression_names()
            except Exception as e:
                print(f"Error loading audio progression file: {e}")

    def update_progression_names(self):
        if self.sound_info:
            for group_info in self.sound_info.values():
                for entry_info in group_info:
                    prog_id = entry_info.get('PROGRESSION ID:', '')
                    progression_name = self.progression_names.get(prog_id, '')
                    entry_info['Progression Name:'] = progression_name

    def extract_info(self, file_path):
        try:
            sound_info = {}

            with open(file_path, 'rb') as file:
                header = file.read(32)
                num_groups = 2  # Número fixo de grupos por SND
                group_headers = []
                for _ in range(num_groups):
                    group_header = file.read(96)
                    group_headers.append(group_header)

                for i, group_header in enumerate(group_headers):
                    group_size = struct.unpack('<I', group_header[4:8])[0]
                    group_start_pointer = struct.unpack('<I', group_header[12:16])[0]

                    file.seek(group_start_pointer)
                    entry_counter = 0
                    group_info = []

                    while True:
                        sound_config_entry = file.read(28)
                        if len(sound_config_entry) < 28:
                            break
                        
                        audio_id = struct.unpack('<b', sound_config_entry[0:1])[0] 
                        prog_id = struct.unpack('<b', sound_config_entry[1:2])[0]
                        unck2 = struct.unpack('<b', sound_config_entry[2:3])[0]
                        id2 = struct.unpack('<b', sound_config_entry[3:4])[0]
                        prio = struct.unpack('<b', sound_config_entry[4:5])[0]
                        pan = struct.unpack('<b', sound_config_entry[5:6])[0]
                        vol = struct.unpack('<b', sound_config_entry[6:7])[0]
                        aux_a = struct.unpack('<b', sound_config_entry[7:8])[0]
                        id1 = struct.unpack('<b', sound_config_entry[8:9])[0]
                        vol_flag = struct.unpack('<b', sound_config_entry[9:10])[0]
                        pitch_l = struct.unpack('<h', sound_config_entry[10:12])[0]
                        pitch_h = struct.unpack('<h', sound_config_entry[12:14])[0]
                        enc_vol = struct.unpack('<b', sound_config_entry[14:15])[0]
                        grob = struct.unpack('<b', sound_config_entry[15:16])[0]
                        srd_type = struct.unpack('<b', sound_config_entry[16:17])[0]
                        span = struct.unpack('<b', sound_config_entry[17:18])[0]
                        svol = struct.unpack('<b', sound_config_entry[18:19])[0]
                        free1 = struct.unpack('<b', sound_config_entry[19:20])[0]
                        free2 = struct.unpack('<b', sound_config_entry[20:21])[0]
                        free3 = struct.unpack('<b', sound_config_entry[21:22])[0]
                        flag = struct.unpack('<I', sound_config_entry[22:26])[0]
                        unck17 = struct.unpack('<H', sound_config_entry[26:28])[0]

                        entry_info = {
                            'AUDIO ID:': audio_id,
                            'PROGRESSION ID:': prog_id,
                            'UNKNOW2:': unck2,
                            'ID 2:': id2,
                            'PRIORITY:': prio,
                            'PAN:': pan,
                            'VOLUME:': vol,
                            'AUX_A:': aux_a,
                            'ID 1:': id1,
                            'VOLUME_FLAG:': vol_flag,
                            'PITCH LOW:': pitch_l,
                            'PITCH HIGH:': pitch_h,
                            'ENC VOLUME:': enc_vol,
                            'GROB:': grob,
                            'SRD TYPE:': srd_type,
                            'SPAN:': span,
                            'S VOLUME:': svol,
                            'FREE1:': free1,
                            'FREE2:': free2,
                            'FREE3:': free3,
                            'FLAG:': flag,
                            'UNKNOW17:': unck17,
                            'start_pointer': group_start_pointer + entry_counter * 28
                        }

                        group_info.append(entry_info)
                        entry_counter += 1

                    sound_info[f"group_{i+1}"] = group_info

            return sound_info
        except Exception as e:
            print(f"Error extracting information: {e}")
            return None

    def display_info(self):
        if self.sound_info:
            group_info = self.sound_info.get(f"group_{self.current_group}")
            if group_info:
                entry_info = group_info[self.current_entry]

                self.entry_num_var.set(str(self.current_entry))

                for label, entry in zip(self.entry_info_labels, self.entry_info_entries):
                    label.destroy()
                    entry.destroy()
                self.entry_info_labels = []
                self.entry_info_entries = []

                for i, (key, value) in enumerate(entry_info.items()):
                    if key in ['AUDIO ID:', 'PROGRESSION ID:', 'UNKNOW2:', 'ID 2:', 'PRIORITY:', 'PAN:', 'VOLUME:', 'AUX_A:', 'ID 1:', 'VOLUME_FLAG:',
                               'PITCH LOW:', 'PITCH HIGH:', 'ENC VOLUME:', 'GROB:', 'SRD TYPE:', 'SPAN:', 'S VOLUME:', 'FREE1:', 'FREE2:',
                               'FREE3:', 'FLAG:', 'UNKNOW17:', 'AUDIO NAME:']:
                        label = tk.Label(self.info_frame, text=key)
                        label.grid(row=i % 11, column=i // 11 * 2, padx=5, pady=5)
                        entry = tk.Entry(self.info_frame, width=10)
                        entry.insert(0, str(value))
                        entry.grid(row=i % 11, column=i // 11 * 2 + 1, padx=5, pady=5)
                        self.entry_info_labels.append(label)
                        self.entry_info_entries.append(entry)

                audio_id = entry_info.get('AUDIO ID:', '')
                prog_id = entry_info.get('PROGRESSION ID:', '')
                audio_name = self.audio_names.get(audio_id, '')
                progression_name = entry_info.get('Progression Name:', '')

                self.audio_name_var.set(audio_name)
                self.progression_name_var.set(progression_name)

    def prev_group(self):
        if self.current_group > 1:
            self.current_group -= 1
            self.current_entry = 0
            self.display_info()

    def next_group(self):
        if self.current_group < 2:  # Número fixo de grupos por SND
            self.current_group += 1
            self.current_entry = 0
            self.display_info()

    def prev_entry(self):
        if self.current_entry > 0:
            self.current_entry -= 1
            self.display_info()

    def next_entry(self):
        group_info = self.sound_info.get(f"group_{self.current_group}")
        if group_info and self.current_entry < len(group_info) - 1:
            self.current_entry += 1
            self.display_info()

    def save_file(self):
        if self.current_file and self.sound_info:
            try:
                with open(self.current_file, 'r+b') as file:
                    file.write(struct.pack('32s', b'\xCA\xB6\xBE\x20' * 8))
                    group_info = self.sound_info.get(f"group_{self.current_group}")
                    entry_info = group_info[self.current_entry]
                    entry_data = struct.pack(
                        '<bbbbbbbbbbhhbbbbbbbbIH',
                        int(self.entry_info_entries[0].get()),  # audio_id
                        int(self.entry_info_entries[1].get()),  # prog_id
                        int(self.entry_info_entries[2].get()),  # unck2
                        int(self.entry_info_entries[3].get()),  # id2
                        int(self.entry_info_entries[4].get()),  # prio
                        int(self.entry_info_entries[5].get()),  # pan
                        int(self.entry_info_entries[6].get()),  # vol
                        int(self.entry_info_entries[7].get()),  # aux_a
                        int(self.entry_info_entries[8].get()),  # id1
                        int(self.entry_info_entries[9].get()),  # vol_flag
                        int(self.entry_info_entries[10].get()),  # pitch_l
                        int(self.entry_info_entries[11].get()),  # pitch_h
                        int(self.entry_info_entries[12].get()),  # enc_vol
                        int(self.entry_info_entries[13].get()),  # grob
                        int(self.entry_info_entries[14].get()),  # srd_type
                        int(self.entry_info_entries[15].get()),  # span
                        int(self.entry_info_entries[16].get()),  # svol
                        int(self.entry_info_entries[17].get()),  # free1
                        int(self.entry_info_entries[18].get()),  # free2
                        int(self.entry_info_entries[19].get()),  # free3
                        int(self.entry_info_entries[20].get()),  # flag
                        int(self.entry_info_entries[21].get()),  # unck17
                    )
                    file.seek(entry_info['start_pointer'])
                    file.write(entry_data)
                print("File saved successfully!")
            except Exception as e:
                print(f"Error saving file: {e}")
        else:
            print("Please load a sound file first.")

# Inicializar a aplicação
root = tk.Tk()
app = SNDInfoEditor(root)
root.mainloop()
