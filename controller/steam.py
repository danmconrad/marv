import evdev
import math

from evdev import ecodes
from evdev.util import categorize, event_factory
from evdev.events import KeyEvent, AbsEvent, SynEvent

EMPTY_STATE = {
  "X": {}
}

class Steam:
  def __init__(self):
    self.state = EMPTY_STATE
    self.controller = self.__get_controller()


  def __get_controller(self):
    devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
    for device in devices:
      if "Valve Software Steam" in device.name:
        return evdev.InputDevice(device.fn)

  # Public

  def is_connected(self):
    if self.controller is None:
      return False
    else:
      return True

  def print_capabilities(self):
    print(self.controller.capabilities(verbose=True))

  def listen(self):
    for event in self.controller.read_loop():
      self.__handle_event(event)

      if type(evdev.util.categorize(event)) is SynEvent:
        yield self.state

  # # Private

  def __handle_event(self, event):
    categorized_event = evdev.util.categorize(event)

    print(categorized_event)

  #   if type(categorized_event) is KeyEvent:
  #     self.__handle_key_event(categorized_event)

  #   if type(categorized_event) is AbsEvent:
  #     self.__handle_abs_event(event)

  # def __handle_key_event(self, event):
  #   pretty_code = self.__get_event_pretty_code(event.keycode)
  #   self.__add_key_state(pretty_code, event.keystate)

  # def __handle_abs_event(self, event):
  #   pretty_code = self.__get_event_pretty_code(ecodes.ABS[event.code])
  #   self.__add_axis_state(pretty_code, event.value)

  # def __get_event_pretty_code(self, code):
  #   if isinstance(code, list):
  #     code = code[0]
  #   return PRETTY_MAP[code]

  # def __add_key_state(self, code, state):
  #   self.state[code]["pressed"] = (state == 1)

  # def __add_axis_state(self, code, value):
  #   if "DPAD" in code:
  #     self.__add_dpad_state(code, value)

  #   elif "ANALOG_HORIZONTAL" in code:
  #     self.__add_analog_horizontal_state(code, value)

  #   elif "ANALOG_VERTICAL" in code:
  #     self.__add_analog_vertical_state(code, value)

  #   elif code in ["L2", "R2"]:
  #     self.__add_trigger_state(code, value)

  # def __add_dpad_state(self, code, value):
  #   if code == "DPAD_VERTICAL":
  #     value *= -1
  #     self.__add_key_state("DPAD_UP", value)
  #     self.__add_key_state("DPAD_DOWN", -value)

  #   elif code == "DPAD_HORIZONTAL":
  #     self.__add_key_state("DPAD_LEFT", -value)
  #     self.__add_key_state("DPAD_RIGHT", value)

  #   self.__add_key_state(code, value)

  #   button = self.state[code]
  #   button["magnitude"] = value
  #   button["pressed"] = value != 0

  #   DPAD = self.state["DPAD"]
  #   DPAD_HORIZONTAL =  self.state["DPAD_HORIZONTAL"]
  #   DPAD_VERTICAL =  self.state["DPAD_VERTICAL"]

  #   DPAD["pressed"] = True in [DPAD_HORIZONTAL["pressed"], DPAD_VERTICAL["pressed"]]
  #   DPAD["angle"] = DPAD_ANGLES[DPAD_HORIZONTAL["magnitude"]][DPAD_VERTICAL["magnitude"]]
  #   DPAD["magnitude"] = 1 if DPAD["pressed"] == True else 0

  # def __add_analog_horizontal_state(self, code, value):
  #   magnitude = (value - 127.5) / 127.5
  #   button = self.state[code]
  #   button["pressed"] = magnitude != 0
  #   button["magnitude"] = magnitude

  #   side = "LEFT" if "LEFT" in code else "RIGHT"

  #   aggegate_button = self.state[side+"_ANALOG"]
  #   HORIZONTAL =  self.state[side+"_ANALOG_HORIZONTAL"]
  #   VERTICAL =  self.state[side+"_ANALOG_VERTICAL"]

  #   aggegate_button["pressed"] = True in [HORIZONTAL["pressed"], VERTICAL["pressed"]]

  #   horizontal_magnitude = HORIZONTAL["magnitude"]
  #   vertical_magnitude = VERTICAL["magnitude"]

  #   aggregate_magnitude = min(1, math.hypot(horizontal_magnitude, vertical_magnitude))
  #   aggegate_button["magnitude"] = aggregate_magnitude

  #   if aggregate_magnitude == 0:
  #     angle = 0

  #   else:
  #     angle = math.degrees(math.asin(vertical_magnitude/aggregate_magnitude))

  #     if horizontal_magnitude < 0:
  #       angle = 180 - angle

  #   if angle < 0:
  #     angle += 360

  #   aggegate_button["angle"] = angle

  # def __add_analog_vertical_state(self, code, value):
  #   magnitude = round((128 - value) / 128, 2)
  #   button = self.state[code]
  #   button["pressed"] = magnitude != 0
  #   button["magnitude"] = magnitude

  # def __add_trigger_state(self, code, value):
  #   button = self.state[code]
  #   button["pressed"] = value != 0
  #   button["magnitude"] = value / 255
