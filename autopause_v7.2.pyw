import asyncio
import time

from tkinter import *
from pystray import MenuItem as item
import pystray
from PIL import Image, ImageTk

from threading import Thread

from winrt.windows.media.control import (
    GlobalSystemMediaTransportControlsSessionManager as MediaManager ,
    GlobalSystemMediaTransportControlsSessionPlaybackStatus as PlaybackStatus
)


ICON_PATH = 'spotify_pause.ico'


current_state=0
old_state=0

is_spotify_playing = 0
is_media_playing = 0

is_spotify_paused = 0



# Define a function for quit the window
def quit_window(icon, item):
   icon.stop()
#    win.destroy()


# Define a function to show the window again
def show_window(icon, item):
#    icon.stop()
#    win.after(0,win.deiconify())
    ...

# Hide the window and show on the system taskbar
def hide_window():
#    win.withdraw()
   image=Image.open(ICON_PATH)
   menu=(item('Quit', quit_window), item('Show', show_window))
   icon=pystray.Icon("name", image, "Auto Pause", menu)
   icon.run()


async def get_media_info():

    global is_spotify_paused
    global is_media_playing

    sessions = await MediaManager.request_async()

    # current_session = sessions.get_current_session()
    run_both = None
    
    while True:
        current_sessions= sessions.get_sessions()

        # print(current_sessions)

        # is_media_playing = 0

        chrome_info = None
        spotify_info = None


        for session in current_sessions:

            # if "chrome" in session.source_app_user_model_id.lower():
            #     chrome_info = session.get_playback_info()
            if "spotify" in session.source_app_user_model_id.lower():

                if is_media_playing:
                    run_both = 1
                else: 
                    run_both = 0
                spotify_manager = session 
                spotify_info = session.get_playback_info()
            else:
                
                chrome_info = session.get_playback_info()
                
                # print(chrome_info)

        if (not chrome_info) or chrome_info.playback_status == PlaybackStatus.PAUSED:
            run_both=0
            is_media_playing = 0


        elif chrome_info.playback_status == PlaybackStatus.PLAYING:
            # run_both=0
            is_media_playing=1
        
        if run_both:
                time.sleep(0.32)
                # print("run both")
                continue
        
        if spotify_info:
            
            if chrome_info and chrome_info.playback_status == PlaybackStatus.PLAYING and spotify_info.playback_status == PlaybackStatus.PLAYING: #status of 4 is playing, 5 is paused
                await spotify_manager.try_pause_async()

                print("spotify paused")
                is_spotify_paused = 1
            elif (not chrome_info or chrome_info.playback_status == PlaybackStatus.PAUSED) and spotify_info.playback_status == PlaybackStatus.PAUSED  and is_spotify_paused == 1:
                print("spotify resumed")
                is_spotify_paused = 0
                
                await spotify_manager.try_play_async()
            time.sleep(0.3)
        else: 
            time.sleep(2)

            
        
                
 
   
def tkinter():
    win=Tk()

    win.title("Auto Pause")
    # Set the size of the window
    # win.geometry("700x350")

    win.protocol('WM_DELETE_WINDOW', hide_window)
    current_media_info = asyncio.run(get_media_info())
    win.mainloop()

def app():
    asyncio.run(get_media_info())

if __name__ == '__main__':

    thread2 = Thread(target = app, args = ())
    # thread = Thread(target = tkinter, args = ())
    thread2.daemon = True
    thread2.start()
    

    # thread.start()

    # win=Tk()

    # win.title("Auto Pause")
    # # Set the size of the window
    # win.geometry("0x0")
    hide_window()

    # win.protocol('WM_DELETE_WINDOW', hide_window)
    # current_media_info = asyncio.run(get_media_info())

    # win.mainloop()

    

    # root.mainloop()

    # while True:


        # current_media_info = asyncio.run(get_media_info())
        # # print(current_media_info)
        # if(current_media_info==5):
        #     print("paused")
        # elif(current_media_info==4): 
        #     print("playing")
        # elif(current_media_info==2): 
        #     print("changing")
        # time.sleep(0.3)