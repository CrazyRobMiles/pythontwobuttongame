## Two Button Game
## Rob Miles
## Version 1.0

import time
import random

# Uncomment the version that you want to run.
version="RPI"
#version="ESP32"
#version="PICO"
#version="PICO-RGB"
#version="CLB"

if version=="CLB":
    import paho.mqtt.client as mqtt
    import json

    # For the CLB version the colours are given by characters
    
    red='R';green='G';blue='B'
    cyan='C';magenta='M';yellow='Y'
    white='W';black='K'
    
    class CLB(object):
        
        def connected(self,client,userdata,flags,rc):
            print("Connected")
            command = '{"process":"pixels","command":"pattern","steps":5,"pattern":"mask","colourmask":"K"}'
            self.client.publish(self.mqtt_prefix + self.blue_button,command)
            self.client.publish(self.mqtt_prefix + self.red_button,command)
            self.client.subscribe("lb/command/clb-host")
            
        def on_message(self, client, userdata, message):
            message_text = str(message.payload.decode("utf-8"))
            message_obj = json.loads(message_text)
            if message_obj["from"]==self.blue_button:
                if message_obj["text"]=="down":
                   self.blue_down_flag=True
                else:
                   self.blue_down_flag=False
            if message_obj["from"]==self.red_button:
                if message_obj["text"]=="down":
                   self.red_down_flag=True
                else:
                   self.red_down_flag=False
            
        def __init__(self):
            mqtthost="put MQTT host here"
            mqttuser="put MQTT username here"
            mqttpwd="put MQTT password here"
            # name for this device
            mqttdevice="clb-host"
            self.client = mqtt.Client(mqttdevice)
            self.client.username_pw_set(mqttuser, mqttpwd)
            self.client.on_connect = self.connected
            self.client.on_message=self.on_message
            self.client.connect(mqtthost, port=1883)
            self.client.loop_start()
            self.red_button = "red"
            self.blue_button = "blue"
            self.mqtt_prefix = "lb/command/"
            self.red_down_flag=False
            self.blue_down_flag=False
            self.no_of_leds=12
            self.leds = [black] * self.no_of_leds
            
        def pixels_show(self):
            colour_string = ""
            for col in self.leds:
                colour_string = colour_string + str(col)
            command = '{"process":"pixels","command":"pattern","pattern":"mask","steps":5,"colourmask":"' + colour_string + '" }'
            self.client.publish(self.mqtt_prefix + self.blue_button,command)
            self.client.publish(self.mqtt_prefix + self.red_button,command)
            pass

        def pixel_set(self,i, col):
            self.leds[i]=col
            pass
            
        def red_down(self):
            return self.red_down_flag
            
        def blue_down(self): 
            return self.blue_down_flag
    
    hardware=CLB

if version=="RPI":
    
    red=(255,0,0);green=(0,255,0);blue=(0,0,255)
    cyan=(0,255,255);magenta=(255,0,255);yellow=(255,255,0)
    white=(255,255,255);black=(0,0,0)

    class RPi(object):
        
        def __init__(self):
            import digitalio
            import board
            import neopixel
            no_of_leds=6
            neo_gpio=board.D18
            red_gpio=board.D22
            blue_gpio=board.D27
            self.no_of_leds = no_of_leds
            self.neo_gpio=neo_gpio
            self.red_gpio=red_gpio
            self.blue_gpio=blue_gpio

            self.pixels = neopixel.NeoPixel(self.neo_gpio, no_of_leds)

            self.red_button = digitalio.DigitalInOut(red_gpio)
            self.red_button.direction = digitalio.Direction.INPUT
            self.red_button.pull = digitalio.Pull.UP

            self.blue_button = digitalio.DigitalInOut(blue_gpio)
            self.blue_button.direction = digitalio.Direction.INPUT
            self.blue_button.pull = digitalio.Pull.UP

        def pixels_show(self):
            pass

        def pixel_set(self,i, col):
            self.pixels[i]=col
            
        def red_down(self):
            return not self.red_button.value
            
        def blue_down(self): 
            return not self.blue_button.value
        
    hardware = RPi

if version=="PICO-RGB":
    
    import picokeypad as keypad

    red=(255,0,0);green=(0,255,0);blue=(0,0,255)
    cyan=(0,255,255);magenta=(255,0,255);yellow=(255,255,0)
    white=(255,255,255);black=(0,0,0)
    
    class PICO_RGB(object):
        def __init__(self):
            
            keypad.init()
            keypad.set_brightness(1)
            self.no_of_leds=12
            self.red_bit = 0b1000000000000000
            self.blue_bit =  0b0001000000000000
            self.pixel_set(12,blue)
            self.pixel_set(15,red)
            self.pixels_show()

        def pixels_show(self):
            keypad.update()

        def pixel_set(self,i, col):
            keypad.illuminate(i, col[0], col[1], col[2])
            
        def red_down(self):
            return (keypad.get_button_states() & self.red_bit) > 0
            
        def blue_down(self):
            return (keypad.get_button_states() & self.blue_bit) > 0
        
    hardware=PICO_RGB

if version=="ESP32":
    
    red=(255,0,0);green=(0,255,0);blue=(0,0,255)
    cyan=(0,255,255);magenta=(255,0,255);yellow=(255,255,0)
    white=(255,255,255);black=(0,0,0)

    class ESP32(object):
        def __init__(self):
            from machine import Pin
            from neopixel import NeoPixel
            
            self.no_of_leds = 6
            self.neo_gpio=13
            self.red_gpio=12
            self.blue_gpio=14

            self.red_button=Pin(self.red_gpio,Pin.IN, Pin.PULL_UP)
            self.blue_button=Pin(self.blue_gpio,Pin.IN, Pin.PULL_UP)

            pixel_pin = Pin(self.neo_gpio,Pin.OUT)
            self.pixels = NeoPixel(pixel_pin, self.no_of_leds)

        def pixels_show(self):
            self.pixels.write()

        def pixel_set(self,i, col):
            self.pixels[i]=col
            
        def red_down(self):
            return not self.red_button.value()
            
        def blue_down(self): 
            return not self.blue_button.value()
        
    hardware=ESP32

if version=="PICO":
    
    import array, time, random
    from machine import Pin
    import rp2

    red=(255,0,0);green=(0,255,0);blue=(0,0,255)
    cyan=(0,255,255);magenta=(255,0,255);yellow=(255,255,0)
    white=(255,255,255);black=(0,0,0)

    NUM_LEDS=6

    @rp2.asm_pio(sideset_init=rp2.PIO.OUT_LOW, out_shiftdir=rp2.PIO.SHIFT_LEFT, autopull=True, pull_thresh=24)
    def ws2812():
        T1 = 2
        T2 = 5
        T3 = 3
        wrap_target()
        label("bitloop")
        out(x, 1)               .side(0)    [T3 - 1]
        jmp(not_x, "do_zero")   .side(1)    [T1 - 1]
        jmp("bitloop")          .side(1)    [T2 - 1]
        label("do_zero")
        nop()                   .side(0)    [T2 - 1]
        wrap()

    # Create the StateMachine with the ws2812 program, outputting on pin
    sm = rp2.StateMachine(0, ws2812, freq=8_000_000, sideset_base=Pin(6))

    # Start the StateMachine, it will wait for data on its FIFO.
    sm.active(1)

    # Display a pattern on the LEDs via an array of LED RGB values.
    ar = array.array("I", [0 for _ in range(NUM_LEDS)])

    class PICO(object):
            
        def __init__(self):
            
            self.no_of_leds = 6
            self.neo_gpio=6
            self.red_gpio=8
            self.blue_gpio=7
            
            self.red_button=Pin(self.red_gpio,Pin.IN, Pin.PULL_UP)
            self.blue_button=Pin(self.blue_gpio,Pin.IN, Pin.PULL_UP)
            
        def pixels_show(self):
            dimmer_ar = array.array("I", [0 for _ in range(self.no_of_leds)])
            for i,c in enumerate(ar):
                r = int(((c >> 8) & 0xFF))
                g = int(((c >> 16) & 0xFF))
                b = int((c & 0xFF))
                dimmer_ar[i] = (g<<16) + (r<<8) + b
            sm.put(dimmer_ar, 8)
            time.sleep_ms(10)

        def pixel_set(self,i, color):
            ar[i] = (color[1]<<16) + (color[0]<<8) + color[2]
            
        def red_down(self):
            return not self.red_button.value()
            
        def blue_down(self): 
            return not self.blue_button.value()
        
    hardware = PICO

fillers=(green,cyan,magenta,yellow,white,black)

class two_button_game(object):
    
    def __init__(self, platform):
        self.platform = platform
        self.puzzle = [black] * self.platform.no_of_leds
        self.response_time = 4.0
        self.move_time = 0.33
        self.score=0

    def show_puzzle(self):
        pos=0
        for col in self.puzzle:
            self.platform.pixel_set(pos, col)
            pos = pos + 1
        self.platform.pixels_show()
        
    def fill_lamps(self,col):
        for i in range(self.platform.no_of_leds):
            self.platform.pixel_set(i, col)
        self.platform.pixels_show()

    def flash(self,col,gap):
        self.fill_lamps(col)
        time.sleep(gap)
        self.fill_lamps(black)
        time.sleep(gap)

    def wait_for_buttons_released(self):
        while True:
            if self.platform.blue_down():
                continue
            if self.platform.red_down():
                continue
            return

    def wait_for_a_player(self):
        # waits for player - flash the lights
        # to remind people the device is still powered
        sleep_count=0
        sleep_limit=100
        while True:
            if self.platform.red_down() or self.platform.blue_down():
                break
            time.sleep(0.1)
            sleep_count+=1
            if sleep_count == sleep_limit:
                sleep_count=0
                self.fill_lamps(cyan)
                time.sleep(0.5)
                self.fill_lamps(black)

    def get_puzzle(self):
       
        for i in range(self.platform.no_of_leds):
            self.puzzle[i]=black
            
        while True:
            self.red_count=random.randrange(1,self.platform.no_of_leds-1)
            self.blue_count=random.randrange(1,self.platform.no_of_leds-1)
            if (self.blue_count+self.red_count) > self.platform.no_of_leds:
                continue
            if self.blue_count==self.red_count:
                continue
            break
        
        pos=0
        
        for i in range(self.red_count):
            self.puzzle[pos]=red
            pos += 1
        for i in range(self.blue_count):
            self.puzzle[pos]=blue
            pos += 1
            
        extra_count = pos + self.score

        if extra_count>self.platform.no_of_leds:
            extra_count = self.platform.no_of_leds
            
        for i in range(pos,extra_count):
            self.puzzle[i]= random.choice(fillers)

    def shuffle_puzzle(self):
        for shuffle in range(0,self.platform.no_of_leds):
            i = random.randrange(0,self.platform.no_of_leds)
            j = random.randrange(0,self.platform.no_of_leds)
            self.puzzle[i], self.puzzle[j] = self.puzzle[j], self.puzzle[i]
            
    def rotate_puzzle_left(self):
        bottom = self.puzzle[0]
        for pos in range(0,self.platform.no_of_leds-1):
            self.puzzle[pos]=self.puzzle[pos+1]
        self.puzzle[self.platform.no_of_leds-1]=bottom

    def display_score(self):
        tens = int(self.score/10)
        units = self.score-10*tens
        for i in range(0,tens):
            self.flash(yellow,0.3)
        time.sleep(0.6)
        for i in range(0,units):
            self.flash(magenta,0.3)
        time.sleep(0.6)
        
    def play(self):

        while True:
           
            self.wait_for_buttons_released()
            
            for count in range(0,3):
                self.flash(white, 0.3)

            self.score=0
            self.alive=True
                
            while self.alive:
                self.get_puzzle()
                self.shuffle_puzzle()
                self.show_puzzle()
                start_time=time.time()
                start_move=time.time()
                while True:
                    red_button_down = self.platform.red_down()
                    blue_button_down = self.platform.blue_down()
                    
                    if red_button_down and blue_button_down:
                        self.alive=False
                        break
                    
                    if red_button_down:
                        if self.red_count > self.blue_count:
                            self.score=self.score+1
                        else:
                            self.alive=False
                        break
                    
                    if blue_button_down:
                        if self.blue_count > self.red_count:
                            self.score=self.score+1
                        else:
                            self.alive=False
                        break
                    
                    if (time.time() - start_move) > self.move_time:
                        start_move=time.time()
                        if self.score>40:
                            self.fill_lamps(black)
                        elif self.score>30:
                            self.shuffle_puzzle()
                            self.show_puzzle()
                        elif self.score>20:
                            self.rotate_puzzle_left()
                            self.show_puzzle()
                    if (time.time() - start_time) > self.response_time:
                        self.alive=False
                        break
                if self.alive:      
                    self.flash(green,0.5)
                    self.wait_for_buttons_released()
            
            if self.score==0:
                self.fill_lamps(black)
                self.wait_for_a_player()
            else:    
                self.flash(red,0.5)
                self.display_score()

platform = hardware()
game = two_button_game(platform)
game.play()