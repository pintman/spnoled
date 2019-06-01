SCALE = 20


class Bot:
    def __init__(self, bot_json, display):
        ''' Create bot from a json object of the following form
        {'bot_id': 7894182, 'm': 4.994642734527588, 'p': [[...]]}
        '''
        self.id = bot_json['bot_id']
        self.pos = bot_json['p'][0]
        assert len(self.pos) == 2
        self.mass = bot_json['m']
        self.display = display

    def draw(self):
        if self.on_display():
            xdisp, ydisp = self.display_coordinates()
            #print("draw on display", xdisp, ydisp)
            self.display.px(xdisp, ydisp, True)

    def on_display(self):
        xdisp, ydisp = self.display_coordinates()
        return 0 <= xdisp < self.display.width and 0 <= ydisp < self.display.height

    def display_coordinates(self):
        x, y = self.pos
        xoff, yoff = self.display.offset
        xdisp, ydisp = x - xoff, y - yoff

        return int(xdisp / SCALE), int(ydisp / SCALE)

    def __str__(self):
        return f"{self.id}@{self.pos}"

    