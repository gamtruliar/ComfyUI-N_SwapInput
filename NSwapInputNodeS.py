import logging
import folder_paths
import shutil
import os
from typing import Tuple, List, Dict, Optional
from server import PromptServer
from aiohttp import web
import re

logger = logging.getLogger(__name__)

THUMBNAIL_PREFIX="thb_"


class NSwapInput:


    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):

        return {
            "required": {
                "backup_suffix": ("STRING", {"default": ""}),

            }
        }

    RETURN_TYPES = ()
    RETURN_NAMES = ()
    OUTPUT_IS_LIST = ()
    FUNCTION = "swap input folder"
    CATEGORY = "NUtility"

@PromptServer.instance.routes.post("/N_swapinput/backup_input")
async def backup_input_folder(request):
    try:
        data = await request.json()
        if not data.get("backup_suffix"):
            raise ValueError("No backup suffix provided")
        backup_suffix = data.get("backup_suffix")
        # Validate backup_suffix to allow Chinese and other Unicode characters
        if not backup_suffix or not re.match(r"^[\w\u4e00-\u9fff._-]+$", backup_suffix):
            raise ValueError("Invalid backup suffix provided. Only alphanumeric, Chinese characters, dashes, underscores, and periods are allowed.")

        success, message = backup_input_folder(backup_suffix)
        return web.json_response({
            "success": success,
            "message": message
        })
    except Exception as e:
        logger.error(f"Error in backup_input_folder route: {str(e)}")
        return web.json_response({
            "success": False,
            "error": str(e)
        }, status=500)

@PromptServer.instance.routes.post("/N_swapinput/restore_input")
async def restore_input_folder(request):
    try:
        data = await request.json()
        if not data.get("backup_suffix"):
            raise ValueError("No backup suffix provided")
        backup_suffix = data.get("backup_suffix")
        # Validate backup_suffix to allow Chinese and other Unicode characters
        if not backup_suffix or not re.match(r"^[\w\u4e00-\u9fff._-]+$", backup_suffix):
            raise ValueError("Invalid backup suffix provided. Only alphanumeric, Chinese characters, dashes, underscores, and periods are allowed.")

        success, message = restore_input_folder(backup_suffix)
        return web.json_response({
            "success": success,
            "message": message
        })
    except Exception as e:
        logger.error(f"Error in restore_input_folder route: {str(e)}")
        return web.json_response({
            "success": False,
            "error": str(e)
        }, status=500)

def backup_input_folder(backup_suffix) -> Tuple[bool, str]:
    try:
        input_dir = folder_paths.get_input_directory()
        backup_dir = os.path.join(os.path.dirname(input_dir), "input_"+backup_suffix)

        # Create backup directory if it doesn't exist
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)

        # First, remove all thumbnail files
        for file in os.listdir(input_dir):
            if file.startswith(THUMBNAIL_PREFIX):
                os.remove(os.path.join(input_dir, file))

        # Copy remaining files from input to backup
        for file in os.listdir(input_dir):
            file_path = os.path.join(input_dir, file)
            if os.path.isfile(file_path):
                shutil.copy2(file_path, backup_dir)

        # Clear input directory
        for file in os.listdir(input_dir):
            file_path = os.path.join(input_dir, file)
            if os.path.isfile(file_path):
                os.remove(file_path)

        return True, "Input folder backed up successfully"
    except Exception as e:
        logger.error(f"Backup failed: {str(e)}")
        return False, f"Backup failed: {str(e)}"


def restore_input_folder(backup_suffix) -> Tuple[bool, str]:
    try:
        input_dir = folder_paths.get_input_directory()
        backup_dir = os.path.join(os.path.dirname(input_dir), "input_"+backup_suffix)

        if not os.path.exists(backup_dir):
            return False, "Backup directory not found"

        # Clear thumbnails first
        for file in os.listdir(input_dir):
            if file.startswith(THUMBNAIL_PREFIX):
                os.remove(os.path.join(input_dir, file))

        # Restore original files
        for file in os.listdir(backup_dir):
            shutil.copy2(os.path.join(backup_dir, file), input_dir)

        return True, "Input folder restored successfully"
    except Exception as e:
        logger.error(f"Restore failed: {str(e)}")
        return False, f"Restore failed: {str(e)}"

# Register node class
NODE_CLASS_MAPPINGS = {
    "N_SwapInput": NSwapInput
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "N_SwapInput": "N Swap Input"
}
