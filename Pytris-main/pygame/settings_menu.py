import pygame as pg
from settings import KEY_BINDINGS, FONT_PATH  # Ensure you import necessary constants

class SettingsMenu:
    def __init__(self, main):
        self.main = main
        self.font = pg.freetype.Font(FONT_PATH)  # Use the font defined in your settings
        self.remap_mode = False  # Flag to track if in remap mode
        self.selected_key_action = None  # Action currently being remapped

    def draw_remap_gui(self):
        y_offset = 50
        for action, key in KEY_BINDINGS.items():
            key_name = pg.key.name(key)
            text = f"{action.capitalize()}: {key_name}"
            self.font.render_to(self.main.screen, (50, y_offset), text, fgcolor=(255, 255, 255))
            y_offset += 50
        
        if self.selected_key_action:
            instruction_text = f"Press a new key for {self.selected_key_action.capitalize()}"
            self.font.render_to(self.main.screen, (50, y_offset), instruction_text, fgcolor=(255, 255, 0))

    def update(self, event):
        if self.remap_mode:
            if event.type == pg.KEYDOWN:
                if self.selected_key_action:
                    # Remap the selected key
                    KEY_BINDINGS[self.selected_key_action] = event.key
                    self.selected_key_action = None  # Reset after remapping
                else:
                    # Choose an action to remap (this example cycles through the actions)
                    if self.selected_key_action is None:
                        self.selected_key_action = 'left'  # Change this to cycle through keys as needed
        else:
            # Additional update logic can be added here if needed
            pass

    def toggle_remap_mode(self):
        self.remap_mode = not self.remap_mode
        if not self.remap_mode:
            self.selected_key_action = None  # Reset when exiting remap mode
