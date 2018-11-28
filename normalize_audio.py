# -*- coding: utf-8 -*-

import os, time
from subprocess import check_output

folder_mp4 = "/home/user1/smb/Intenso/Eigene_Videos_klein"
folder_backup = "/home/user1/backup_audio"
num_files = sum([len(files) for r, d, files in os.walk(folder_mp4)])/4
counter_ = 0
for root, dirs, files in os.walk(folder_mp4):
    for file in files:
        if file.endswith(".mp4"):
            counter_ += 1
            file_path = os.path.join(root, file)
            backup_path = os.path.join(folder_backup, file)
            print("Created: %s" % time.ctime(os.path.getctime(file_path)))
            stat = os.stat(file_path)
            print("\nBearbeite Datei: " + file_path + " (" + str(counter_) + " von " + str(num_files) + ")")
            # backup the original audio stream
            print("Backup der originalen Audio Streams")
            out = check_output(['ffmpeg', '-i', file_path, '-vn', '-acodec', 'copy', backup_path])
            print(out)
            os.utime(backup_path, (stat.st_atime,stat.st_mtime))
            # normalize the audio
            print("\nNormalizing Audio (" + str(counter_) + " von " + str(num_files) + ")")
            out = check_output(['ffmpeg-normalize', '-v', file_path, '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-o', file_path, '-f'])
            print(out)
            os.utime(file_path, (stat.st_atime,stat.st_mtime))
print("Fertig")
