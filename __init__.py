import os
import glob
import shutil
import sys
import folder_paths

from .NSwapInputNodeS import NSwapInput




NODE_CLASS_MAPPINGS = {
    "N_SwapInput": NSwapInput,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "N_SwapInput": "N Swap Input",
}

WEB_DIRECTORY = "./web"
__all__ = [
    "NODE_CLASS_MAPPINGS",
    "NODE_DISPLAY_NAME_MAPPINGS",
    "WEB_DIRECTORY",
    ]
