import math

class BarStyle():
  DIAGONAL_FORWARD  = 0
  DIAGONAL_BACKWARD = 1
  ARROW_FORWARD     = 2
  ARROW_BACKWARD    = 3

class infinite_bar_base():
  
  def __init__(self, x, y, width, height, oled, band_style=0, band_width=20):
    self.inited = False
    
    self.x = x
    self.y = y
    self.height = height
    self.width = width
    self.oled = oled
    self.phase = 0
    self.band_width = band_width
    self.band_style = band_style
    
    self.text = None
    self.text_color = 1
    
    self.update()
    self.inited = True
  
  def update(self):
    if not self.inited:
      x_range = range(0, self.width + 1)
      y_range = range(0, self.height + 1)
    else:
      x_range = range(1, self.width)
      y_range = range(1, self.height)
    
    for i in x_range:
      for j in y_range:
        if i == 0 or j == 0 or i == self.width or j == self.height:
          if not self.inited:
            # draw outline
            self.oled.pixel(self.x + i, self.y + j, 1)
        else:
          # draw barbershop poll
          self.oled.pixel(
            self.x + i, 
            self.y + j,
            self._get_pixel_color(i, j, self.phase)
          )
    
    # print the text out
    self.draw_text()
    
    # increase phase
    self.phase = (self.phase + 1) % (self.band_width - 1)
  
  def _get_pixel_color(self, x, y, phase):
    return ((phase + x + y) % self.band_width * 2) < self.band_width
  
  def set_text(self, text, color=1):
    self.text = text
    self.text_color = color
  
  def draw_text(self):
    if self.text == None:
      return
    
    # All characters have dimensions of 8x8 pixels and there is currently no way to change the font.
    text_width = len(self.text) * 8
    block_padding = 1 # 1 pixel padding around text mask
    text_x = math.floor(self.x + (self.width - text_width) / 2)
    text_y = math.floor(self.y + (self.height - 6) / 2)
    
    self.oled.framebuf.fill_rect(
      text_x - block_padding,
      text_y - block_padding,
      text_width + block_padding * 2,
      8 + block_padding * 2,
      not self.text_color
    )
    self.oled.text(self.text, text_x, text_y, self.text_color)
  
class infinite_bar(infinite_bar_base):
  def __init__(self, x, y, width, height, oled):
    super().__init__(x, y, width, height, oled)
    self.inited = True
  
  def redraw(self):
    self.inited = False
    super().update()
    self.inited = True
  
  def update(self):
    if not self.inited:
      # update unoptimized the first time (paint all pixels)
      return super().update()
    
    bar_count = math.ceil(self.width / self.band_width * 2)
    for i in range(bar_count):
      for j in range(0, self.height - 1):
        x = i * self.band_width - j - self.phase
        if 0 < x < self.width:
          # draw left side
          self.oled.pixel(
            self.x + x, 
            self.y + j + 1,
            1
          )
        x = x + math.floor(self.band_width / 2)
        if 0 < x < self.width:
          # draw right side
          self.oled.pixel(
            self.x + x, 
            self.y + j + 1,
            0
          )
    
    # print the text out
    self.draw_text()
    
    # increase phase
    self.phase = (self.phase + 1) % (self.band_width)

