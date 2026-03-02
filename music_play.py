import unittest
from abc import ABC,abstractmethod
from enum import Enum

class MusicPlayer:
    def __init__(self):
        self.__library = []
        self.__playlist = []

    def search(self,name):
        for playlist in self.__playlist:
            for song in playlist.content:
                if song.name == name:
                    return song
                if song.album == name:
                    return song

    def add_to_library(self,library):
        self.__library.append(library)

    def create_playlist(self,name):
        playlist = Playlist(name)
        self.__playlist.append(playlist)

    def add_to_playlist(self,playlist_name,content):
        for playlist in self.__playlist:
            if playlist.name == playlist_name:
                playlist.content.append(content)

    def play_single(self,song):
        print(f"Play {song.name} author is {song.author} from {song.album} file type is {song.file_type}")

    def play_album(self,album):
        print(f"play {album}")

    def play_playlist(self,playlist_name):
        for playlist in self.__playlist:
            if playlist.name == playlist_name:
                for content in playlist.content:
                    self.play_single(content)

class Playlist:
    def __init__(self,name):
        self.__name = name
        self.__content = []

    @property
    def name(self):
        return self.__name
    
    @property
    def content(self):
        return self.__content
    
    @content.setter
    def content(self,content):
        self.__content = content

class Song:
    def __init__(self,name,author,album,file_type):
        self.__name = name
        self.__author = author
        self.__album = album
        self.__file_type = file_type

    @property
    def name(self):
        return self.__name
    
    @property
    def author(self):
        return self.__author
    
    @property
    def album(self):
        return self.__album
    
    @property
    def file_type(self):
        return self.__file_type

class Podcast:
    def __init__(self,album,name,channel,author,file_type):
        self.__album = album
        self.__name = name
        self.__channel = channel
        self.__author = author
        self.__file_type = file_type

    @property
    def name(self):
        return self.__name
    
    @property
    def author(self):
        return self.__author
    
    @property
    def album(self):
        return self.__album
    
    @property
    def file_type(self):
        return self.__file_type


# ---------------------------------------------------------
# Test Script (จำลองการใช้งานตามโจทย์)
# ---------------------------------------------------------
if __name__ == "__main__":
    # 1. สร้างเครื่องเล่น
    player = MusicPlayer()

    # 2. สร้างข้อมูล Mockup (เพลง และ Podcast)
    song1 = Song("Shape of You", "Ed Sheeran", "Divide", ".flac")
    song2 = Song("Perfect", "Ed Sheeran", "Divide", ".mp3")
    song3 = Song("Blinding Lights", "The Weeknd", "After Hours", ".aac")
    
    pod1 = Podcast(15, "The Future of AI", "TechTalk", "John Doe", ".mp3")
    pod2 = Podcast(16, "OOP Explained", "CodeDaily", "Jane Smith", ".aac")

    # นำเข้าคลังเพลง
    for item in [song1, song2, song3, pod1, pod2]:
        player.add_to_library(item)

    # 3. ทดสอบ: สร้าง Playlist และเพิ่มเพลง/podcast ปนกัน (โจทย์ระบุว่ามีได้มากกว่า 1 playlist)
    player.create_playlist("My Favorites")
    player.create_playlist("Workout Mix")

    player.add_to_playlist("My Favorites", song1)
    player.add_to_playlist("My Favorites", pod1) # ใส่ Podcast ปนกับเพลง
    
    player.add_to_playlist("Workout Mix", song3)
    player.add_to_playlist("Workout Mix", pod2)

    # 4. ทดสอบความสามารถต่างๆ ของ Music Player
    
    # - เล่นเพลงใดเพลงหนึ่ง
    player.play_single(song2)

    # - เรียกดู/เล่นเพลงใน Playlist (จะเห็นว่ามันเล่นทั้งเพลงและ Podcast ได้รันติดกัน)
    player.play_playlist("My Favorites")

    # - เรียกดู/เล่นเพลงใน Album
    player.play_album("Divide")

    # - ค้นหา (ค้นจากชื่อเพลง หรือ ชื่ออัลบั้ม)
    player.search("divide")  # หาจากชื่ออัลบั้ม
    player.search("future")  # หาจากชื่อ Podcast
