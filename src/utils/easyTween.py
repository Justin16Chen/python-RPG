import math
from enum import Enum

from src.utils.mathUtils import lerp


class TaskType(Enum):
    SET = 1
    CALL = 2
    SET_AND_CALL = 3

class Tween:
    ### STATIC PROPERTIES AND METHODS
    tween_list = []

    # update all tweens in Tween.tweenList
    @staticmethod
    def update_tweens(dt):
        # update all tweens
        for i in range(len(Tween.tween_list) - 1, -1, -1):
            tween = Tween.tween_list[i]

            # update tween
            tween.step(dt)

            # set parent's attributes to tween value
            if (
                tween.delay_timer is None
                and not tween.paused
                and isinstance(tween.attribute, str)
            ):
                setattr(tween.parent, tween.attribute, tween.value)

            # delete finished tweens and update loop index to not skip any tweens
            if tween.done:
                if tween.should_call:
                    if tween.call_function_args is None:
                        getattr(tween.parent, tween.call_function_name)()
                    else:
                        getattr(tween.parent, tween.call_function_name)(*tween.call_function_args)

                Tween.tween_list.pop(i)

    ###TWEEN MODIFIER FUNCTIONS
    @staticmethod
    def clear_tweens(parent):
        for i in range(len(Tween.tween_list) - 1, -1, -1):
            if Tween.tween_list[i].parent == parent:
                Tween.tween_list.pop(i)

    @staticmethod
    def clear_all():
        Tween.tween_list = []

    @staticmethod
    def delete_tween(parent, tween_name):
        idx = Tween.get_tween_index(parent, tween_name)
        if idx is not None:
            Tween.tween_list.pop(idx)

    @staticmethod
    def pause_tween(parent, tween_name):
        tween = Tween.get_tween(parent, tween_name)
        if tween is not None:
            tween.pause()

    @staticmethod
    def unpause_tween(parent, tween_name):
        tween = Tween.get_tween(parent, tween_name)
        if tween is not None:
            tween.unpause()

    ###TWEEN RETRIEVAL FUNCTIONS
    @staticmethod
    def get_tween_index(parent, tween_name):
        for i, tween in enumerate(Tween.tween_list):
            if parent == tween.parent:
                if tween_name is None or tween.name == tween_name:
                    return i
        return None

    @staticmethod
    def get_tween(parent, tween_name):
        idx = Tween.get_tween_index(parent, tween_name)
        return None if idx is None else Tween.tween_list[idx]

    @staticmethod
    def has_tween(parent, tween_name=None):
        return not Tween.get_tween_index(parent, tween_name) is None

    ###EASING FUNCTIONS
    # x = num between 0 and 1
    @staticmethod
    def ease_linear(x):
        return x

    @staticmethod
    def ease_in_sine(x):
        return 1 - math.cos(x * math.pi * 0.5)

    @staticmethod
    def ease_out_sine(x):
        return math.sin((x * math.pi) * 0.5)

    @staticmethod
    def ease_in_out_sine(x):
        return -(math.cos(math.pi * x) - 1) / 2

    @staticmethod
    def ease_in_cubic(x):
        return x**3

    @staticmethod
    def ease_out_cubic(x):
        return 1 - ((1 - x) ** 3)

    @staticmethod
    def ease_in_out_cubic(x):
        return 4 * x**3 if x < 0.5 else 1 - ((-2 * x + 2) ** 3) / 2

    @staticmethod
    def ease_in_back(x):
        c1 = 1.70158
        c3 = c1 + 1
        return c3 * x * x * x - c1 * x * x

    @staticmethod
    def ease_out_back(x):
        c1 = 1.70158
        c3 = c1 + 1
        return 1 + c3 * ((x - 1) ** 3) + c1 * ((x - 1) ** 2)

    @staticmethod
    def ease_in_out_back(x):
        c1 = 1.70158
        c2 = c1 * 1.525
        return (
            (((2 * x) ** 2) * ((c2 + 1) * (x * 2 - 2) + c2)) / 2
            if x < 0.5
            else (((2 * x) ** 2) * ((c2 + 1) * (x * 2 - 2) + c2) + 2) / 2
        )

    # returns y value given a function type and the x value
    @staticmethod
    def get_y_val(tween_type, x):
        if tween_type == "inSine":
            return Tween.ease_in_sine(x)
        if tween_type == "outSine":
            return Tween.ease_out_sine(x)
        if tween_type == "inOutSine":
            return Tween.ease_in_out_sine(x)
        if tween_type == "inCubic":
            return Tween.ease_in_cubic(x)
        if tween_type == "outCubic":
            return Tween.ease_out_cubic(x)
        if tween_type == "inOutCubic":
            return Tween.ease_in_out_cubic(x)
        if tween_type == "inBack":
            return Tween.ease_in_back(x)
        if tween_type == "outBack":
            return Tween.ease_out_back(x)
        if tween_type == "inOutBack":
            return Tween.ease_in_out_back(x)
        return Tween.ease_linear(x)

    # returns if a tween is done or not
    @staticmethod
    def tween_done(tween):
        if tween.loop:
            return False
        if tween.ping_pong:
            return tween.stage == "back" and tween.percent <= 0
        return tween.percent >= 1

    ### INDIVIDUAL PROPERTIES AND METHODS
    # tween_properties = {start: num, end: num, time: num, type: string, delay: optional num, finish_func: optional dict}
    # type = linear, lerp
    # finish_func = {name: string, args: any value}
    def __init__(
        self,
        parent, attr, start_value, end_value, time,
        call_function_name=None,
        call_function_args = None,
        tween_type="linear",
        delay=0,
        loop=False, ping_pong=False,
        name="tween"
    ):
        if time <= 0:
            raise ValueError(f"time of {time} must be positive for {name} Tween")

        Tween.tween_list.append(self)

        self.parent = parent
        self.start_value = start_value
        self.end_value = end_value
        self.time = time
        self.attribute = attr
        self.call_function_name = call_function_name
        self.call_function_args = call_function_args
        self.tween_type = tween_type
        self.loop = loop
        self.ping_pong = ping_pong
        self.name = name

        self.done = False
        self.stage = "there"
        self.paused = False
        self.progress = 0

        self.delay_timer = None
        if delay != 0:
            self.delay_timer = Timer(
                self,
                self.name + " delay timer",
                time=delay,
                set_attr_name="delay_timer",
                set_attr_to=None,
            )

        self.type = TaskType.SET if call_function_name is None else TaskType.SET_AND_CALL

        setattr(parent, self.attribute, self.start_value)

    @property
    def should_call(self):
        return self.type == TaskType.CALL or self.type == TaskType.SET_AND_CALL

    @property
    def percent(self):
        return max(0, min(1, self.progress / self.time))

    def __str__(self):
        return f"percent: {self.percent}, value: {self.value}"

    def step(self, dt):
        # do nothing when paused
        if self.paused:
            return

        # update main tween stage
        if self.delay_timer is None:

            # update percent counter
            if not self.ping_pong:
                self.progress += dt
                self.progress = max(0.0, min(self.time, self.progress))

            # update ping ponging
            if self.ping_pong:
                # find direction to step percent variable
                progress_dir = 1 if self.stage == "there" else -1
                self.progress += progress_dir * dt
                self.progress = max(0.0, min(self.time, self.progress))

                # turn the other way
                if self.percent == 1:
                    self.stage = "back"
                elif self.percent == 0 and self.loop:
                    self.stage = "there"

            # update looping
            if self.loop:
                if not self.ping_pong and self.percent == 1:
                    self.progress = 0

            # check if tween is done
            self.done = Tween.tween_done(self)

    # pausing functions
    def pause(self):
        self.paused = True

    def unpause(self):
        self.paused = False

    # get value of tween
    @property
    def value(self):
        return lerp(
            self.start_value, self.end_value, Tween.get_y_val(self.tween_type, self.percent)
        )

    @value.setter
    def value(self, value):
        raise Exception("cannot set value of a tween")


class Timer:
    timer_list = []

    @staticmethod
    def update_timers(dt):
        for i in range(len(Timer.timer_list) - 1, -1, -1):
            timer = Timer.timer_list[i]

            timer.step(dt)

            if timer.destroy:
                Timer.timer_list.pop(i)

    @staticmethod
    def clear_all():
        Timer.timer_list = []


    @staticmethod
    def clear_timers(parent):
        for i in range(len(Timer.timer_list) - 1, -1, -1):
            if Timer.timer_list[i].parent == parent:
                Timer.timer_list.pop(i)

    def __init__(
        self,
        parent,
        name,
        time,
        set_attr_name=None,
        set_attr_to=None,
        call_function_name=None,
        args=None,
    ):
        Timer.timer_list.append(self)
        self.parent = parent
        self.name = name
        self.cur_time = 0
        if time <= 0:
            raise ValueError(f"time of {time} must be positive for {name} Timer")
        self.time = time
        self.destroy = False

        # find type of timer - set, call, set_and_call
        self.type = None
        if set_attr_name is not None:
            if call_function_name is not None:
                self.type = TaskType.SET_AND_CALL
            else:
                self.type = TaskType.SET
        elif call_function_name is not None:
            self.type = TaskType.CALL

        # set a variable
        if self.should_set:
            self.attribute = set_attr_name
            self.setTo = set_attr_to

        # call a function
        if self.should_call:
            self.funcName = call_function_name
            self.args = args

    @property
    def should_set(self):
        return self.type == TaskType.SET or self.type == TaskType.SET_AND_CALL

    @property
    def should_call(self):
        return self.type == TaskType.CALL or self.type == TaskType.SET_AND_CALL

    def step(self, dt):
        self.cur_time += dt
        if self.cur_time >= self.time:
            # set a variable
            if self.should_set:
                setattr(self.parent, self.attribute, self.setTo)
            # call a function
            if self.should_call:
                if self.args is None:
                    getattr(self.parent, self.funcName)()
                else:
                    getattr(self.parent, self.funcName)(*self.args)

            self.destroy = True
