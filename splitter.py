import os
import ffmpeg
import time
import threading
from colorama import init, Fore, Style

init()

loader_running = True
def retro_loader():
    while loader_running:
        for frame in ['/', '-', '\\', '|']:
            print(Fore.YELLOW + f"\rProcessing videos.. {frame}", end='', flush=True)
            time.sleep(0.1)

print(Fore.GREEN + Style.BRIGHT + "\n╔══════════════════════════════════════════╗")
print("║                                          ║")
print("║           ffmpeg script v.1              ║")
print("║                                          ║")
print("║                     developer: Nicolas   ║")
print("║                                          ║")
print("╚══════════════════════════════════════════╝" + Style.RESET_ALL)

print(Fore.GREEN + Style.BRIGHT + "\nSet input path:")
input_folder = input(Fore.GREEN + Style.BRIGHT + "> " + Style.RESET_ALL).strip()

print(Fore.GREEN + Style.BRIGHT + "\nSet output path:")
output_folder = input(Fore.GREEN + Style.BRIGHT + "> " + Style.RESET_ALL).strip()
os.makedirs(output_folder, exist_ok=True)

while True:
    print(Fore.GREEN + Style.BRIGHT + "\nSet cutting duration (in seconds):")
    tempo = input(Fore.GREEN + Style.BRIGHT + "> " + Style.RESET_ALL).strip()
    if tempo.isdigit() and int(tempo) > 0:
        clip_duration = int(tempo)
        break
    else:
        print(Fore.RED + "An error has occurred." + Style.RESET_ALL)

while True:
    print(Fore.GREEN + Style.BRIGHT + "\nDo you want to save in subfolders per video? (y/n):")
    usar_subpastas = input(Fore.GREEN + Style.BRIGHT + "> " + Style.RESET_ALL).strip().lower()
    if usar_subpastas in ('y', 'n'):
        break
    else:
        print(Fore.RED + "Please type only 'y' or 'n'." + Style.RESET_ALL)

print(Fore.GREEN + Style.BRIGHT + f"\nStarting cuts of {clip_duration} seconds.." + Style.RESET_ALL)

arquivos = [f for f in os.listdir(input_folder) if f.lower().endswith(('.mp4', '.mov', '.avi', '.mkv'))]
videos_processados = 0
videos_pulados = 0

loader_thread = threading.Thread(target=retro_loader)
loader_thread.start()

for filename in arquivos:
    input_path = os.path.join(input_folder, filename)

    try:
        probe = ffmpeg.probe(input_path)
        duration = float(probe['format']['duration'])
    except Exception as e:
        print(Fore.RED + f"\nError when parsing {filename}: {e}" + Style.RESET_ALL)
        videos_pulados += 1
        continue

    base_name = os.path.splitext(filename)[0]

    if usar_subpastas == 'y':
        output_subfolder = os.path.join(output_folder, base_name)
        os.makedirs(output_subfolder, exist_ok=True)
    else:
        output_subfolder = output_folder

    for i, start in enumerate(range(0, int(duration), clip_duration)):
        end_time = min(clip_duration, duration - start)
        if end_time < 1:
            continue

        output_name = f"{base_name}_part{i+1:03d}.mp4"
        output_path = os.path.join(output_subfolder, output_name)

        try:
            (
                ffmpeg
                .input(input_path, ss=start, t=end_time)
                .output(output_path)
                .run(quiet=True)
            )
        except Exception as e:
            print(Fore.YELLOW + f"\nError when cutting {filename} excerpt {i+1}: {e}" + Style.RESET_ALL)
            continue

    videos_processados += 1

loader_running = False
loader_thread.join()
print("\r" + " " * 40 + "\r", end="")

print(Fore.GREEN + Style.BRIGHT + f"\nCompleted successfully!\n")
print(Fore.GREEN + "Processed:" + Style.RESET_ALL + f" {videos_processados}")
print(Fore.GREEN + "Skipped:" + Style.RESET_ALL + f" {videos_pulados}\n")
