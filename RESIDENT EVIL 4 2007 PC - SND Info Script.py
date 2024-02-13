import tkinter as tk
from tkinter import filedialog
import struct

def extract_info(file_path):
    try:
        with open(file_path, 'rb') as file:
            header = file.read(32)
            num_groups = 2  # Número fixo de grupos por SND
            group_headers = []
            for _ in range(num_groups):
                group_header = file.read(96)
                group_headers.append(group_header)

            with open(file_path + "_info.txt", 'w') as txt_file:
                txt_file.write("Resident Evil 4 2007 PC - SND Info Tool by RE-Play Games, 02/2024\n\n") # Linha adicionada

                txt_file.write("Header:\n")
                txt_file.write(header.hex() + "\n\n")

                for i, group_header in enumerate(group_headers):
                    group_size = struct.unpack('<I', group_header[4:8])[0]
                    group_start_pointer = struct.unpack('<I', group_header[12:16])[0]
                    group_end_pointer = struct.unpack('<I', group_header[44:48])[0]

                    txt_file.write(f"Group {i+1}:\n")
                    txt_file.write(f"Size: {group_size}\n")
                    txt_file.write(f"Start Pointer: {group_start_pointer}\n")
                    txt_file.write(f"End Pointer: {group_end_pointer}\n\n")

                    # Lê as entradas de configuração de som dentro do grupo
                    file.seek(group_start_pointer)
                    entry_counter = 0
                    while True:
                        sound_config_entry = file.read(28)
                        if len(sound_config_entry) < 28:
                            break
                        
                        audio_id = sound_config_entry[0]
                        prog_id = sound_config_entry[1]
                        unck2 = sound_config_entry[2]
                        id2 = sound_config_entry[3]
                        prio = sound_config_entry[4]
                        pan = sound_config_entry[5]
                        vol = sound_config_entry[6]
                        aux_a = sound_config_entry[7]
                        id1 = sound_config_entry[8]
                        vol_flag = sound_config_entry[9]
                        pitch_l = struct.unpack('<h', sound_config_entry[10:12])[0]
                        pitch_h = struct.unpack('<h', sound_config_entry[12:14])[0]
                        enc_vol = sound_config_entry[14]
                        grob = sound_config_entry[15]
                        srd_type = sound_config_entry[16]
                        span = sound_config_entry[17]
                        svol = sound_config_entry[18]
                        free1 = sound_config_entry[19]
                        free2 = sound_config_entry[20]
                        free3 = sound_config_entry[21]
                        flag = struct.unpack('<I', sound_config_entry[22:26])[0]
                        unck17 = struct.unpack('<H', sound_config_entry[26:28])[0]

                        txt_file.write(f"\nEntrada de configuração de som {entry_counter}:\n")
                        txt_file.write(f"Audio id: {audio_id}\n")
                        txt_file.write(f"Prog# id: {prog_id}\n")
                        txt_file.write(f"Unk2: {unck2}\n")
                        txt_file.write(f"Id2: {id2}\n")
                        txt_file.write(f"Prio: {prio}\n")
                        txt_file.write(f"Pan: {pan}\n")
                        txt_file.write(f"Vol: {vol}\n")
                        txt_file.write(f"Aux_a: {aux_a}\n")
                        txt_file.write(f"Id1: {id1}\n")
                        txt_file.write(f"Vol_flag: {vol_flag}\n")
                        txt_file.write(f"Pitch_l: {pitch_l}\n")
                        txt_file.write(f"Pitch_h: {pitch_h}\n")
                        txt_file.write(f"Enc_vol: {enc_vol}\n")
                        txt_file.write(f"Grob: {grob}\n")
                        txt_file.write(f"Srd_type: {srd_type}\n")
                        txt_file.write(f"Span: {span}\n")
                        txt_file.write(f"Svol: {svol}\n")
                        txt_file.write(f"Free1: {free1}\n")
                        txt_file.write(f"Free2: {free2}\n")
                        txt_file.write(f"Free3: {free3}\n")
                        txt_file.write(f"Flag: {flag}\n")
                        txt_file.write(f"unck17: {unck17}\n")

                        entry_counter += 1

            return "Informações extraídas com sucesso!"
    except Exception as e:
        return f"Erro ao extrair informações: {e}"

def browse_file():
    filename = filedialog.askopenfilename(filetypes=[("SND files", "*.snd")])
    if filename:
        status_label.config(text=extract_info(filename))

# Configuração da interface gráfica
root = tk.Tk()
root.title("RESIDENT EVIL 4 - SND Info Script")
root.geometry("400x200")

browse_button = tk.Button(root, text="Escolher Arquivo", command=browse_file)
browse_button.pack(pady=20)

status_label = tk.Label(root, text="")
status_label.pack()

root.mainloop()
