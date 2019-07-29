# micropython-oled-progressbars
This is a collection of display elements for showing progress on ssd1306 OLED screen using micropython.

The elements are built to reduce draw calls to the frame buffer (improving performance).
If your application requires redraws every update (if, for instance, you have a loading bar which animates across the screen while updating) you can call the "BarBase" class instead which will repaint the entire element on updates.

# Usage

## Basic infinite progress bar
![Basic Infinite Bar](/images/basic.jpg)
```python
import ssd1306
import progress_bar

i2c = I2C(-1, scl=Pin(5), sda=Pin(4))

oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

# create a new progress bar
infinte_bar = progress_bar.ProgressBar(10, 40, oled.width - 20, 15, oled)

oled.text('connecting to', 0, 10)
oled.text('network...', 0, 20)

# animate the progress bar
while True:
  infinte_bar.update()
  oled.show()
```

## Infinite progress bar with text
![Infinite Bar With Text](/images/text.jpg)
```python

# create a new progress bar
infinte_bar = progress_bar.ProgressBar(10, 40, oled.width - 20, 15, oled)
index = 0
# animate the progress bar
while True:
  # set dynamic text on top of bar
  infinte_bar.set_text('SLEEPING %s' % index, 0)
  infinte_bar.update()
  oled.show()
  
  if index >= 99:
    index = 0
  else:
    index += 1
```

## Progress progress bar
```python

# create a new progress bar
my_bar = progress_bar.ProgressBar(10, 40, oled.width - 20, 15, oled)
index = 0
# animate the progress bar
while True:
  # set amount of bar to fill
  my_bar.set_percent(index)
  my_bar.update()
  oled.show()
  
  if index >= 99:
    index = 0
  else:
    index += 1
```
