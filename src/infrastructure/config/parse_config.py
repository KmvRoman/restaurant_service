import pathlib

from cattrs import structure
from omegaconf import OmegaConf

from src.infrastructure.config.config import Config

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent.parent


def load_config(path: str):
    dictionary_config = OmegaConf.to_container(OmegaConf.merge(
        OmegaConf.load(path),
        OmegaConf.structured(Config)
    ), resolve=True)
    return structure(dictionary_config, Config)
