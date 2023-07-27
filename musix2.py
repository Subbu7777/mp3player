import os
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QFileDialog, QSlider
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QPixmap
import mutagen

class MusicPlayer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Music Player")
        self.setGeometry(400, 200, 550, 330)

        self.title_label = QLabel(self)
        self.title_label.setGeometry(50, 200, 300, 30)
        self.title_label.setAlignment(Qt.AlignCenter)

        self.album_cover_label = QLabel(self)
        self.album_cover_label.setGeometry(150, 100, 150, 150)

        self.browse_button = QPushButton("Browse", self)
        self.browse_button.setGeometry(50, 30, 50, 30)
        self.browse_button.clicked.connect(self.browse_songs)

        self.play_button = QPushButton("Play", self)  # for play button
        self.play_button.setGeometry(150, 30, 50, 30)  # x,y ,width height
        self.play_button.clicked.connect(self.play_music)  # connection

        self.pause_button = QPushButton("Pause", self)  # for pause button
        self.pause_button.setGeometry(250, 30, 50, 30)
        self.pause_button.clicked.connect(self.pause_music)  # connection

        self.previous_button = QPushButton("Previous", self)  # for previous song
        self.previous_button.setGeometry(50, 70, 80, 30)
        self.previous_button.clicked.connect(self.play_previous)

        self.next_button = QPushButton("Next", self)  # for next song
        self.next_button.setGeometry(350, 70, 50, 30) 
        self.next_button.clicked.connect(self.play_next)

        self.volume_button = QPushButton("Mute", self)
        self.volume_button.setGeometry(350, 30, 50, 30)
        self.volume_button.clicked.connect(self.toggle_mute)

        # for song position moving cursor
        self.position_slider = QSlider(Qt.Horizontal, self)
        self.position_slider.setGeometry(50, 250, 300, 30)
        self.position_slider.sliderMoved.connect(self.set_position)

        self.volume_slider = QSlider(Qt.Vertical, self)  # for moving volume
        self.volume_slider.setGeometry(10, 20, 20, 200)
        # takes the value and passes it to the set_volume function
        self.volume_slider.setMinimum(0)
        self.volume_slider.setMaximum(100)
        self.volume_slider.setValue(30)
        self.volume_slider.valueChanged.connect(self.set_volume)


        # creating the media player for playing the songs
        self.media_player = QMediaPlayer(self)
        self.media_player.positionChanged.connect(self.update_position)  # moves the song forward and backward
        self.media_player.durationChanged.connect(self.update_duration)  # moves the song duration position

        self.status_label = QLabel(self)  # creating the label
        self.status_label.setGeometry(10, 270, 400, 30)# assging the message display
        self.status_label.setAlignment(Qt.AlignCenter)


        self.time_label = QLabel(self)#for duration diapsly
        self.time_label.setGeometry(350, 250, 80, 30)
        self.time_label.setAlignment(Qt.AlignCenter)

    def play_music(self):
        if self.media_player.state() == QMediaPlayer.PausedState:  # mediaplayer on paused so we are playing it
            self.media_player.play()  # playing the song
            # calling self.status_label and assigning the text
            self.status_label.setText("Music Playing")

    def pause_music(self):
        if self.media_player.state() == QMediaPlayer.PlayingState:
            self.media_player.pause()
            self.status_label.setText("Music Paused")

    def stop_music(self):
        if self.media_player.state() == QMediaPlayer.PlayingState or self.media_player.state() == QMediaPlayer.PausedState:  # even playing or pausing
            self.media_player.stop()  # move to the starting position
            self.status_label.setText("Music Stopped")

    def play_next(self):  # increase the song index to +1 and passing song index to the load song
        if self.song_index < len(self.songs) - 1:
            self.song_index += 1
            self.load_song()

    def play_previous(self):
        if self.song_index > 0:
            self.song_index -= 1
            self.load_song()

    def set_position(self, position):  # setting
        self.media_player.setPosition(position)

    def update_position(self, position):  # moves the cursor the song will moves forward
        self.position_slider.setValue(position)
        self.update_time_label(position)

    def set_volume(self, volume):  # here volume is int value
        self.media_player.setVolume(volume)  # volume is required argmnts

    def toggle_mute(self):
        if self.media_player.isMuted():
            self.media_player.setMuted(False)
            self.volume_button.setText("Mute")
        else:
            self.media_player.setMuted(True)
            self.volume_button.setText("Unmute")

        self.song_directory = ""
        self.song_index = -1
        self.songs = []

        self.media_player = QMediaPlayer(self)
        self.media_player.positionChanged.connect(self.update_position)
        self.media_player.durationChanged.connect(self.update_duration)

        # Rest of the initialization...

    def browse_songs(self):
        file_dialog = QFileDialog()
        song_path, _ = file_dialog.getOpenFileName(self)
        if song_path:
            self.song_directory = os.path.dirname(song_path)
            self.load_songs()
            self.song_index = 0
            self.load_song()

    def load_songs(self):
        self.songs = []
        for i in os.listdir(self.song_directory):
            if i.endswith(".mp3") or i.endswith(".wav"):
                self.songs.append(os.path.join(self.song_directory, i))


    def update_duration(self, duration):  # duration updation
        self.position_slider.setMinimum(0)  # starting is zero position
        self.position_slider.setMaximum(duration)  # moves along the song

    
    def update_time_label(self, position): #to display the duration of the song pass from duration song
        duration_ms = self.media_player.duration()
        position_minutes = int(position / 60000)
        position_seconds = int((position % 60000) / 1000)
        duration_minutes = int(duration_ms / 60000)
        duration_seconds = int((duration_ms % 60000) / 1000)
        time_text = f"{position_minutes:02d}:{position_seconds:02d} / {duration_minutes:02d}:{duration_seconds:02d}"
        self.time_label.setText(time_text)

    def closeEvent(self, event):
        self.media_player.stop()

    # Rest of the methods...

    def load_song(self):
            if self.song_index >= 0 and self.song_index < len(self.songs):
                song_path = self.songs[self.song_index]
                audio = mutagen.File(song_path)
                 #print(audio[APIC:kick-mp3-songs-my3songs.jpg])
            try:
                if audio and 'APIC:' in audio.tags:  # Check if the song has album cover
                  # Extract the album cover data from the metadata
                  album_cover_data = audio.tags['APIC:'].data
                  #print(album_cover_data,"...............................................................")
                  pixmap = QPixmap()  # Create a QPixmap object to load the image data
                  pixmap.loadFromData(album_cover_data)  # Load the image data into the QPixmap
                  self.album_cover_label.setPixmap(pixmap.scaled(150, 150, Qt.KeepAspectRatio))  # Set the album cover pixmap
                  # Set the default image pixmap
                else:
                    k=dict(audio)
                    kk=list(k)
                    kkk=kk[10]
                    album_cover_data=audio[kkk].data
                    pixmap=QPixmap()
                    pixmap.loadFromData(album_cover_data)
                    self.album_cover_label.setPixmap(pixmap.scaled(150, 150, Qt.KeepAspectRatio))  # Set the album cover pixmap
            except:
                 #If no album cover is available, set a default image
                   default_image_path = r'C:\Users\stanneeru\Desktop\Screenshot.png'  # Provide the path to your default image
                   pixmap = QPixmap(default_image_path)
                   self.album_cover_label.setPixmap(pixmap.scaled(150, 150, Qt.KeepAspectRatio))

            media_content = QMediaContent(QUrl.fromLocalFile(song_path))
            self.media_player.setMedia(media_content)
            self.media_player.play()
            # msg_box = QMessageBox()
            # title=title[0]
            # msg_box.setText(title)
            # #j=title
            self.status_label.setText("music playing")

    # Rest of the class...

if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = MusicPlayer()
    player.show()
    sys.exit(app.exec_())
