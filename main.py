'''
Project: miniPomodoro
By: ushellnullpath
Description:
A lightweight pomodoro timer that can be set to the option of 30min or 60min sessions. 
Each session has 3x pomodoros, 2x five and 1x fifteen-minute breaks in between.
Different libraries that have been used are time, pygame, tkniter and pillow.
Last updated on (D/M/Y): 12/8/2022

'''

import time
from pygame import mixer
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk

#to show different app frames
def show_window(window):
    window.tkraise()

#to drag window anywhere on screen
def win_move(event):
    x, y = root.winfo_pointerxy()
    root.geometry(f"+{x}+{y}")

#---------------------------------------------------------------------------------------------------------------------------------------------------------------
#main
#---------------------------------------------------------------------------------------------------------------------------------------------------------------
root = Tk()
root.title('miniPomodoro by ushellnullpath')
root.geometry('280x190')
root.overrideredirect(True)
root.attributes('-topmost', True)
root.bind('<B1-Motion>', win_move)
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------
#app
#---------------------------------------------------------------------------------------------------------------------------------------------------------------
class App():
    def __init__(self):
        self.start_win = Frame(root)
        self.pomodoro_win = Frame(root)

        for window in (self.start_win, self.pomodoro_win):
            window.grid(row=0 , column=0, sticky='nsew')

        #variables
        self.user_choice = IntVar()
        self.pomodoro_time = ((30 * 60), (60 * 60))
        self.break_time = ((5 * 60), (15 * 60))
        self.sessions = 0
        self.running = False


#---------------------------------------------------------------------------------------------------------------------------------------------------------------
        #start window
#---------------------------------------------------------------------------------------------------------------------------------------------------------------
        self.start_win.configure(background='#d30000')
        #launching the timers
        
        def start_timer():
            choice = self.user_choice.get()
            if choice == 1:
                self.running = True
                session_logic(timer=self.pomodoro_time[0])
                show_window(self.pomodoro_win)
            elif choice == 2:
                self.running = True
                session_logic(timer=self.pomodoro_time[1])
                show_window(self.pomodoro_win)
            else:
                messagebox.showerror("miniPomodoro", "ERROR: Please set your timer.")

        #logo, close, user-choices, start
        logo_symbol = ImageTk.PhotoImage(file="images/logo1.png")
        self.logo_screen = Label(self.start_win, image=logo_symbol, background='#d30000').place(x=17, y=45)

        self.close_window = Button(self.start_win, text='❌', font=('System', 11), width=3, foreground='#ffffff', background='#5c9f00', command=root.quit
        ).place(x=242, y=5)

        self.set_label = Label(self.start_win, text='SET TIMER:', font=('System', 11), foreground='#ffffff', background='#d30000').place(x=20, y=86)

        self.user_choice1 = Radiobutton(self.start_win, variable=self.user_choice, value=1, text='30min', font=('System', 11), 
        background='#d30000', foreground='#ffffff', activebackground='#d30000', activeforeground='#d30000', selectcolor='#d30000').place(x=110, y=84)

        self.user_choice2 = Radiobutton(self.start_win, variable=self.user_choice, value=2, text='60min', font=('System', 11), 
        background='#d30000', foreground='#ffffff', activebackground='#d30000', activeforeground='#d30000', selectcolor='#d30000').place(x=185, y=84)

        self.start_button = Button(self.start_win, text='START', font=('System', 11), width=8, foreground='#ffffff', background='#5c9f00', command=start_timer
        ).place(x=24, y=120)


#---------------------------------------------------------------------------------------------------------------------------------------------------------------
        #pomodoro window
#---------------------------------------------------------------------------------------------------------------------------------------------------------------
        self.pomodoro_win.configure(background='#d30000')
        #timer calc and func(s)
        #countdown logic
        def timer_logic(count):
            if self.running == True:
                minutes = count // 60
                seconds = count % 60
                self.timer_label.config(text=f"{minutes:02d}:{seconds:02d}")
            else: return 

            if count == 0:
                    mixer.init()
                    mixer.music.load("sounds/beep-beep-6151.mp3")
                    mixer.music.play(loops=2)
                    time.sleep(1)
                    mixer.music.stop()
            if count > 0:
                    self.countdown = self.pomodoro_win.after(1000, timer_logic, count-1)
            else: start_timer()

        def session_logic(timer):
            if self.running == True:
                self.sessions += 1
                if self.sessions % 6 == 0:
                    timer_logic(self.break_time[1])
                    self.track_label.config(text="-- on 15min break --")
                elif self.sessions % 2 == 0:
                    timer_logic(self.break_time[0])
                    self.track_label.config(text="-- on 5min break --")
                else:
                    timer_logic(timer)
                    self.track_label.config(text="-- on pomodoro session --")
            else: return

        def reset():
                self.pomodoro_win.after_cancel(self.countdown)
                self.sessions = 0
                self.running = False
                self.user_choice.set(0)
                self.track_label.config(text='')
                self.timer_label.config(text='')
                show_window(self.start_win)

        def exit_pressed():
                root.quit()

        #pomodoro-timer labels and buttons
        self.track_label = Label(self.pomodoro_win, text='', font=('System', 17), foreground='#ffffff', background='#d30000')
        self.track_label.pack(ipady=90)

        self.timer_label = Label(self.pomodoro_win, text='', font=('System', 40), foreground='#ffffff', background='#d30000')
        self.timer_label.place(x=64, y=17)

        self.reset_button = Button(self.pomodoro_win, text='🔄', width=10, font=('System', 18), 
        foreground='#ffffff', background='#5c9f00', command=reset).place(x=-20, y=135)

        self.exit_button = Button(self.pomodoro_win, text='❌', width=8, font=('System', 18), 
        foreground='#ffffff', background='#5c9f00', command=exit_pressed).place(x=137, y=135)

        #run window
        show_window(self.start_win)
        root.mainloop()


App()