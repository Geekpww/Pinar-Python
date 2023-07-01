"""
define save functionalities
"""

__all__ = ['save',
           'load']

from pathlib import Path
import pickle
import logging

from pinar.util.config import CONFIG

LOGGER = logging.getLogger(__name__)


def save(out_file_name, var):
    """Save variable with provided file name. Uses configuration save_dir folder
    if no absolute path provided.

    Parameters
    ----------
    out_file_name : str
        file name (absolute path or relative to configured save_dir)
    var : object
        variable to save in pickle format
    """
    out_file = Path(out_file_name) if Path(out_file_name).is_absolute() \
        else CONFIG.local_data.save_dir.dir().joinpath(out_file_name)
    target_dir = out_file.parent
    try:
        # Generate folder if it doesn't exists
        if not target_dir.is_dir():
            target_dir.mkdir()
            LOGGER.info('Created folder %s.', target_dir)
        with out_file.open('wb') as flh:
            pickle.dump(var, flh, pickle.HIGHEST_PROTOCOL)
            LOGGER.info('Written file %s', out_file)
    except FileNotFoundError as err:
        raise FileNotFoundError(f'Folder {target_dir} not found: ' + str(err)) from err
    except OSError as ose:
        raise ValueError('Data is probably too big. Try splitting it: ' + str(ose)) from ose


def load(in_file_name):
    """Load variable contained in file. Uses configuration save_dir folder
    if no absolute path provided.

    Parameters
    ----------
    in_file_name : str
        file name

    Returns
    -------
    object
    """
    in_file = Path(in_file_name) if Path(in_file_name).is_absolute() \
        else CONFIG.local_data.save_dir.dir().joinpath(in_file_name)
    with in_file.open('rb') as flh:
        data = pickle.load(flh)
    return data
