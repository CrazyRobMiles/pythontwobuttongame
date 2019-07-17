from machine import Pin
from neopixel import NeoPixel
import time
import random

neo_gpio=13
no_of_leds = 6

red_gpio=12
blue_gpio=14

red_button=Pin(red_gpio,Pin.IN, Pin.PULL_UP)
blue_button=Pin(blue_gpio,Pin.IN, Pin.PULL_UP)

pixel_pin = Pin(neo_gpio,Pin.OUT)
pixels = NeoPixel(pixel_pin, no_of_leds)

red_col=(255,0,0)
green_col=(0,255,0)
blue_col=(0,0,255)
cyan_col=(0,255,255)
magenta_col=(255,0,255)
yellow_col=(255,255,0)
white_col=(255,255,255)
black_col=(0,0,0)

def button_test():
    obr=red_button.value()
    obb=blue_button.value()
    while True:
        nbr=red_button.value()
        nbb=blue_button.value()
        if nbr!=obr: print("red changed")
        if nbb!=obb: print("blue changed")
        obr=nbr
        obb=nbb
        time.sleep(0.01)

red=0
green=1
blue=2
cyan=3
magenta=4
yellow=5
white=6
black=7

spectrum_colours=(red_col,green_col,blue_col,cyan_col,magenta_col,yellow_col, white_col, black_col)

easy_puzzles = [[black,black,black,red,blue,blue],
           [black,black,black,blue,red,red],
           [black,blue,blue,blue,red,red],
           [black,blue,blue,red,red,red],
           [black,blue,blue,blue,blue,blue],
           [white,white,white,red,blue,blue],
           [white,white,white,blue,red,red],
           [white,blue,blue,blue,red,red],
           [white,blue,blue,red,red,red],
           [white,blue,blue,blue,blue,blue],
           [white,red,blue,red,red,red],
           [white,red,blue,red,red,red] ]

hard_puzzles = [[green,yellow,cyan,red,blue,blue],
           [magenta,yellow,green,blue,red,red],
           [cyan,cyan,cyan,blue,red,red],
           [yellow,blue,blue,red,red,red],
           [green,blue,blue,blue,blue,blue],
           [yellow,blue,yellow,yellow,yellow,yellow],
           [yellow,red,yellow,yellow,yellow,yellow],
           [yellow,red,yellow,yellow,cyan,yellow],
           [yellow,blue,yellow,red,blue,magenta],
           [magenta,red,cyan,cyan,cyan,magenta],
           [green,green,blue,red,red,green],
           [red,red,red,blue,blue,red],
           [red,red,blue,blue,blue,blue],
           [white,white,white,white,white,red],
           [white,white,white,white,white,blue],
           [green,blue,blue,blue,blue,blue],
           [black,red,blue,red,red,red]]

def render_lamps(source):
    count=0
    for colour in source:
        pixels[count]=spectrum_colours[colour]
        count = count + 1
    pixels.write()
    
def fill_lamps(col):
    pixels.fill(col)
    pixels.write()
    
def fixed_spectrum():
    render_lamps(spectrum_colours)

def random_spectrum():
    random.shuffle(random_spectrum_colours)
    render_lamps(random_spectrum_colours)

def get_buttons():
    global red_button_down, blue_button_down
    red_button_down = not red_button.value()
    blue_button_down = not blue_button.value()
    
def wait_for_buttons_released():
    while True:
        get_buttons()
        if red_button_down or blue_button_down:
            continue
        break

def wait_for_a_player():
    # waits for player - flash the lights
    # to remind people the device is still powered
    sleep_count=0
    sleep_limit=100
    while True:
        get_buttons()
        if red_button_down or blue_button_down:
            break
        time.sleep(0.1)
        sleep_count+=1
        if sleep_count == sleep_limit:
            sleep_count=0
            fill_lamps(cyan_col)
            time.sleep(0.5)
            fill_lamps(black_col)
            

def more_reds(puzzle):
    red_count=0
    blue_count=0
    for item in puzzle:
        if item==red:
            red_count=red_count+1
        if item==blue:
            blue_count=blue_count+1
    if red_count==blue_count:
        raise Exception("Invalid puzzle",puzzle)
    return red_count>blue_count

def get_puzzle(level):
    if level < 10:
        return random.choice(easy_puzzles)
    return random.choice(hard_puzzles)

def shuffle_puzzle(puzzle):
    shuffle_length = len(puzzle)-1
    for count in range(0,shuffle_length):
        i = random.randint(0,shuffle_length)
        j = random.randint(0,shuffle_length)
        puzzle[i], puzzle[j] = puzzle[j], puzzle[i]
        
def rotate_puzzle_left(puzzle):
    bottom = puzzle[0]
    for pos in range(0,len(puzzle)-1):
        puzzle[pos]=puzzle[pos+1]
    puzzle[len(puzzle)-1]=bottom

def display_score(score):
    tens = int(score/10)
    units = score-10*tens
    for i in range(0,tens):
        fill_lamps(yellow_col)
        time.sleep(0.3)
        fill_lamps(black_col)
        time.sleep(0.3)
    time.sleep(0.6)
    for i in range(0,units):
        fill_lamps(magenta_col)
        time.sleep(0.3)
        fill_lamps(black_col)
        time.sleep(0.3)
    time.sleep(0.6)

while True:

    wait_for_buttons_released()
    
    for count in range(0,3):
        fill_lamps(white_col)
        time.sleep(0.3)
        fill_lamps(black_col)
        time.sleep(0.3)

    count=0
    alive=True
    response_time = 4.0
    move_time = 0.33
        
    while alive:
        puzzle=get_puzzle(count)
        shuffle_puzzle(puzzle)
        render_lamps(puzzle)
        start_time=time.time()
        start_move=time.time()
        while True:
            get_buttons()
            if red_button_down and blue_button_down:
                alive=False
                break
            if red_button_down:
                if more_reds(puzzle):
                    count=count+1
                else:
                    alive=False
                break
            if blue_button_down:
                if not more_reds(puzzle):
                    count=count+1
                else:
                    alive=False
                break
            
            if time.time() - start_move > move_time:
                start_move=time.time()
                if count>20:
                    if count>30:
                        if count > 40:
                            fill_lamps(black_col)
                        else:        
                            shuffle_puzzle(puzzle)
                            render_lamps(puzzle)
                    else:
                        rotate_puzzle_left(puzzle)
                        render_lamps(puzzle)
                    
            if time.time() - start_time > response_time:
                alive=False
                break
        if alive:      
            fill_lamps(green_col)
            time.sleep(0.5)
            fill_lamps(black_col)
            time.sleep(0.5)
            wait_for_buttons_released()
    
    if count==0:
        fill_lamps(black_col)
        wait_for_a_player()
    else:    
        fill_lamps(red_col)
        time.sleep(0.5)
        fill_lamps(black_col)
        time.sleep(0.5)
        display_score(count)

    
    

  