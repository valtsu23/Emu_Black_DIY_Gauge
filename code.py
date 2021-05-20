import board
import busio
import struct
import time
import displayio
import terminalio
import digitalio
import canio
from adafruit_display_text import label
from adafruit_bitmap_font import bitmap_font
import adafruit_ili9341
import adafruit_stmpe610
import adafruit_ds3231
import adafruit_sdcard
import storage

# RTC communication
myI2C = busio.I2C(board.SCL, board.SDA)
rtc = adafruit_ds3231.DS3231(myI2C)

if False:   # change to True if you want to write the time!
    #                     year, mon, date, hour, min, sec, wday, yday, isdst
    t = time.struct_time((2021,  03,   16,   10,  30,  00,    0,   -1,    -1))
    # you must set year, mon, date, hour, min, sec and weekday
    # yearday is not supported, isdst can be set but we don't do anything with it at this time

    print("Setting time to:", t)     # uncomment for debugging
    rtc.datetime = t
    print()

# SPI communication pins
spi = board.SPI()

# SD card
sd_cs = digitalio.DigitalInOut(board.D5)
sdcard = adafruit_sdcard.SDCard(spi, sd_cs)
vfs = storage.VfsFat(sdcard)
storage.mount(vfs, "/sd")

# Create library object using our Bus SPI port
displayio.release_displays()

# TFT pins
tft_cs = board.D9
tft_dc = board.D10

display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs)
display = adafruit_ili9341.ILI9341(display_bus, width=240, height=320, rotation=90)

# Touch
st_cs_pin = digitalio.DigitalInOut(board.D6)
st = adafruit_stmpe610.Adafruit_STMPE610_SPI(spi, st_cs_pin)

# For registering just one touch
touched = 0

# Groups
tab_number_group = displayio.Group(x=0, y=0)
row1_group = displayio.Group(x=0, y=0)
row2_group = displayio.Group(x=0, y=108)
row3_group = displayio.Group(x=0, y=214)
lines_group = displayio.Group(x=0, y=0)

# Display group
view = displayio.Group(max_size=15)
view.append(tab_number_group)
view.append(row1_group)
view.append(row2_group)
view.append(row3_group)
view.append(lines_group)

# Lines
line_bitmap = displayio.Bitmap(240, 2, 1)
line_palette = displayio.Palette(1)
line_palette[0] = 0xFFFFFF  # Purple
line_1 = displayio.TileGrid(line_bitmap, pixel_shader=line_palette, x=0, y=106)
line_2 = displayio.TileGrid(line_bitmap, pixel_shader=line_palette, x=0, y=212)
# Draw the lines
lines_group.append(line_1)
lines_group.append(line_2)

# Default Label styling:
TABS_X = 0
TABS_Y = 0

# Fonts
fontB = bitmap_font.load_font("/Helvetica-Bold-62.bdf")
fontS = bitmap_font.load_font("/Helvetica-Bold-35.bdf")
fontVS = bitmap_font.load_font("/Helvetica-Bold-21.bdf")

# Tab number
tab_number_label = label.Label(fontVS, text="0", color=0xFFFFFF, max_glyphs=200, scale=1)
tab_number_label.x = TABS_X+5
tab_number_label.y = TABS_Y+15
tab_number_group.append(tab_number_label)

# Data rows
# Item 1
# Clock label objects
clock_label = label.Label(fontB, text="00:00", color=0xFFFFFF, max_glyphs=200, scale=1)
clock_label.x = TABS_X+38
clock_label.y = TABS_Y+50

# Item 2
# Lambda text label objects
lambdat_label = label.Label(fontVS, text="Lambda", color=0xFFFFFF, max_glyphs=200, scale=1)
lambdat_label.x = TABS_X+10
lambdat_label.y = TABS_Y+50

# Lambda label objects
lambda_label = label.Label(fontB, text="NA", color=0xFFFFFF, max_glyphs=200, scale=1)
lambda_label.x = TABS_X+105
lambda_label.y = TABS_Y+50

# Item 3
# Oil p. text label objects
oilpt_label = label.Label(fontS, text="Oil p.", color=0xFFFFFF, max_glyphs=200, scale=1)
oilpt_label.x = TABS_X+10
oilpt_label.y = TABS_Y+50

# Oil pressure label objects
oilp_label = label.Label(fontB, text="NA", color=0xFFFFFF, max_glyphs=200, scale=1)
oilp_label.x = TABS_X+105
oilp_label.y = TABS_Y+50

# Item 4
# Oil temperature text label objects
oiltt_label = label.Label(fontS, text="Oil t.", color=0xFFFFFF, max_glyphs=200, scale=1)
oiltt_label.x = TABS_X+10
oiltt_label.y = TABS_Y+50

# Oil temperature label objects
oilt_label = label.Label(fontB, text="NA", color=0xFFFFFF, max_glyphs=200, scale=1)
oilt_label.x = TABS_X+105
oilt_label.y = TABS_Y+50

# Rows
row1 = row1_group
row2 = row2_group
row3 = row3_group

def clear_row(row):
    try:
        row.pop()
        row.pop()
    except IndexError:
        pass

def tab1():
    clear_row(row1)
    clear_row(row2)
    clear_row(row3)
    row1_group.append(clock_label)
    row2_group.append(lambdat_label)
    row2_group.append(lambda_label)
    row3_group.append(oiltt_label)
    row3_group.append(oilt_label)

def tab2():
    clear_row(row1)
    clear_row(row2)
    clear_row(row3)
    row1_group.append(clock_label)
    row2_group.append(oilpt_label)
    row2_group.append(oilp_label)
    row3_group.append(lambdat_label)
    row3_group.append(lambda_label)

def tab3():
    clear_row(row1)
    clear_row(row2)
    clear_row(row3)
    row1_group.append(oiltt_label)
    row1_group.append(oilt_label)
    row2_group.append(oilpt_label)
    row2_group.append(oilp_label)
    row3_group.append(lambdat_label)
    row3_group.append(lambda_label)

# Read last tab drom sd card in startup
tabfile = open("/sd/tab_memory.txt", "r")
tab_now = int(tabfile.readline())
tabfile.close()

# Save tab to sd card
def save_tab():
    tabfile = open("/sd/tab_memory.txt", "w")
    tabfile.write("%0.f\n" % tab_now)
    tabfile.close()

#tab_now = 1 (Use this if you disable the sd card function)
# Tab control
def change_tab():
    tab_number_group.pop()
    tab_number_label.text = tab_now
    tab_number_group.append(tab_number_label)
    if tab_now == 1:
        tab1()
    if tab_now == 2:
        tab2()
    if tab_now == 3:
        tab3()
    save_tab()

# Run at startup
change_tab()

#CAN BUS
# The CAN transceiver has a standby pin, bring it out of standby mode
if hasattr(board, 'CAN_STANDBY'):
    standby = digitalio.DigitalInOut(board.CAN_STANDBY)
    standby.switch_to_output(False)

# The CAN transceiver is powered by a boost converter, turn on its supply
if hasattr(board, 'BOOST_ENABLE'):
    boost_enable = digitalio.DigitalInOut(board.BOOST_ENABLE)
    boost_enable.switch_to_output(True)

# Use this line if your board has dedicated CAN pins. (Feather M4 CAN and Feather STM32F405)
can = canio.CAN(rx=board.CAN_RX, tx=board.CAN_TX, baudrate=500_000, auto_restart=True)

# CAN listener 0x602 and 0x603
listener = can.listen(matches=[canio.Match(0x602, mask=0x604)], timeout=.1)

# Needed for CAN BUS
old_bus_state = None
last_message_id = 0

# Main loop
while True:
    # Touch control
    while st.touched:
        while not st.buffer_empty:
            ts = st.touches
            for point in ts:
                # Perform transformation to get into
                # display coordinate system! (Not in use)
                # y = point["y"]
                # x = 4096 - point["x"]
                # x = 2 * x // 30 - 18
                # y = 8 * y // 90 - 18
                # To register just one touch
                touched = 1
    if touched == 1:
        tab_now = tab_now + 1
        if tab_now == 4:
            tab_now = 1
        touched = 0
        change_tab()

    # Clock update
    t = rtc.datetime
    clock_label.text = "%02d:%02d" % (t.tm_hour, t.tm_min)

    # Update display
    display.show(view)

    # CAN BUS
    # Bus state information
    bus_state = can.state
    if bus_state != old_bus_state:
        print(f"Bus state changed to {bus_state}")
        old_bus_state = bus_state
    message = listener.receive()

    # Message handling
    if message is None:
        print("No message received within timeout")
        #time.sleep(1)
        continue

    data = message.data
    if len(data) != 8:
        print(f"Unusual message length {len(data)}")
        #time.sleep(1)
        continue

    id = message.id
    if id == 0x602:
        # To make sure that after 0x603 message the 0x602 comes next. 
        if last_message_id != 602: 
            # Unpack message
            message = struct.unpack("<HBBBBh", data)
            # Just for debugging
            # print(f"0x602: {message}")
            # Update oil pressure and oil temperature
            oilt_label.text = message[2]
            oil_p = message[3]*0.0625
            oilp_label.text = round(oil_p, 1)
            # For message read order
            last_message_id = 602

    if id == 0x603:
        # To make sure that after 0x602 message the 0x603 comes next. 
        if last_message_id != 603: 
            # Unpack message
            message = struct.unpack("<bBBBHH", data)
            # Just for debugging
            # print(f"0x603: {message}")
            # Update lambda value
            lambda_value = message[2]*0.0078125
            lambda_label.text = round(lambda_value, 2)
            # For message read order
            last_message_id = 603
