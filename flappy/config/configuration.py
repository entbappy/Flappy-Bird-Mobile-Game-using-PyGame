import os
import sys
from flappy.logger.log import logging
from flappy.utils.util import read_yaml_file
from flappy.exception.exception_handler import AppException
from flappy.entity.config_entity import TemplatesConfig, RootGameConfig

ROOT_DIR = os.getcwd()
# Main config file path
CONFIG_FOLDER_NAME = "config"
CONFIG_FILE_NAME = "config.yaml"
CONFIG_FILE_PATH = os.path.join(ROOT_DIR,CONFIG_FOLDER_NAME,CONFIG_FILE_NAME)


class AppConfiguration:
    def __init__(self, config_file_path: str = CONFIG_FILE_PATH):
        try:
            self.configs_info = read_yaml_file(file_path=config_file_path)
        except Exception as e:
            raise AppException(e, sys) from e

    
    def get_templates_config(self) -> TemplatesConfig:
        try:
            templates_config = self.configs_info['templates_config']
            templates_dir = templates_config['templates_dir']

            audios_dir = os.path.join(templates_dir, templates_config['audios_dir'])
            sprites_dir = os.path.join(templates_dir, templates_config['sprites_dir'])

            response = TemplatesConfig(
                audios_dir = audios_dir,
                sprites_dir = sprites_dir
            )

            logging.info(f"Flappy templates config: {response}")
            return response

        except Exception as e:
            raise AppException(e, sys) from e

    
    def get_root_game_config(self) -> RootGameConfig:
        try:
            root_game_config = self.configs_info['root_game_config']

            fps = root_game_config['fps']
            screen_width = root_game_config['screen_width']
            screen_height = root_game_config['screen_height']
            player_name = root_game_config['player_name']
            background_name = root_game_config['background_name']
            pipe_name = root_game_config['pipe_name']

            response = RootGameConfig(
                fps = fps,
                screen_width = screen_width,
                screen_height = screen_height,
                player_name = player_name,
                background_name = background_name,
                pipe_name = pipe_name
            )

            logging.info(f"Flappy root config: {response}")
            return response

        except Exception as e:
            raise AppException(e, sys) from e
