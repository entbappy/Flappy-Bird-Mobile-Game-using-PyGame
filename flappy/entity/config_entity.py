from collections import namedtuple

TemplatesConfig = namedtuple("TemplatesConfig", ["audios_dir",
                                                "sprites_dir"])

RootGameConfig = namedtuple("RootGameConfig", ["fps",
                                                "screen_width",
                                                "screen_height",
                                                "player_name",
                                                "background_name",
                                                "pipe_name"])                                                