"""

    BANDIZIP COMMAND LINE WRAPPERS v1.0
 
for more details, check the following links
https://en.bandisoft.com/bandizip/
https://en.bandisoft.com/bandizip/help/parameter/


"""

import logging
import os
import re
import subprocess

ARCHIVE_FORMAT_7Z_SPLIT = '001'
ARCHIVE_FORMAT_7Z = '7z'
ARCHIVE_FORMAT_ACE = 'ace'
ARCHIVE_FORMAT_AES = 'aes' # encryption algo
ARCHIVE_FORMAT_ALZ = 'alz'
ARCHIVE_FORMAT_ARC = 'arc'
ARCHIVE_FORMAT_ARJ = 'arj'
ARCHIVE_FORMAT_BH = 'bh'
# ARCHIVE_FORMAT_BIN = 'bin'
ARCHIVE_FORMAT_BR = 'br'
ARCHIVE_FORMAT_BZ = 'bz'
ARCHIVE_FORMAT_BZ2 = 'bz2'
ARCHIVE_FORMAT_CAB = 'cab'
# ARCHIVE_FORMAT_Compound_MSI = 'msi' 
ARCHIVE_FORMAT_EGG = 'egg'
ARCHIVE_FORMAT_GZ = 'gz'
# ARCHIVE_FORMAT_IMG = 'img'
# ARCHIVE_FORMAT_ISO = 'iso'
# ARCHIVE_FORMAT_ISZ = 'isz'
ARCHIVE_FORMAT_LHA = 'lha'
ARCHIVE_FORMAT_LZ = 'lz'
ARCHIVE_FORMAT_LZH = 'lzh'
ARCHIVE_FORMAT_LZMA = 'lzma' # compression algo
ARCHIVE_FORMAT_PMA = 'pma'  
ARCHIVE_FORMAT_RAR = 'rar'
# ARCHIVE_FORMAT_RAR5 = 'rar'
# ARCHIVE_FORMAT_SFX_EXE = 'exe' 
ARCHIVE_FORMAT_TAR = 'tar'
ARCHIVE_FORMAT_TBZ = 'tbz'
ARCHIVE_FORMAT_TBZ2 = 'tbz2'
ARCHIVE_FORMAT_TGZ = 'tgz'
ARCHIVE_FORMAT_TLZ = 'tlz'
ARCHIVE_FORMAT_TXZ = 'txz'
# ARCHIVE_FORMAT_UDF = 'udf'
# ARCHIVE_FORMAT_WIM = 'wim'
# ARCHIVE_FORMAT_XPI = 'xpi'
ARCHIVE_FORMAT_XZ = 'xz'
ARCHIVE_FORMAT_Z = 'z'
ARCHIVE_FORMAT_ZIP = 'zip'
ARCHIVE_FORMAT_ZIPX = 'zipx'
ARCHIVE_FORMAT_ZPAQ = 'zpaq'
ARCHIVE_FORMAT_ZSTD = 'zst'
ARCHIVE_FORMAT_NSIS = 'nsi'

SUPPORTED_FORMATS_COMPRESS = [
    ARCHIVE_FORMAT_ZIP,
    ARCHIVE_FORMAT_7Z,
    ARCHIVE_FORMAT_ZIPX,
    # ARCHIVE_FORMAT_SFX_EXE,
    ARCHIVE_FORMAT_TAR,
    ARCHIVE_FORMAT_TGZ,
    ARCHIVE_FORMAT_LZH,
    # ARCHIVE_FORMAT_ISO,
    ARCHIVE_FORMAT_GZ,
    ARCHIVE_FORMAT_XZ
]

SUPPORTED_FORMATS_DECOMPRESS = [
    ARCHIVE_FORMAT_7Z,
    ARCHIVE_FORMAT_ACE,
    ARCHIVE_FORMAT_AES,
    ARCHIVE_FORMAT_ARC,
    ARCHIVE_FORMAT_ALZ,
    ARCHIVE_FORMAT_ARJ,
    ARCHIVE_FORMAT_BH,
    # ARCHIVE_FORMAT_BIN,
    ARCHIVE_FORMAT_BZ,
    ARCHIVE_FORMAT_BZ2,
    ARCHIVE_FORMAT_CAB,
    # ARCHIVE_FORMAT_Compound_MSI,
    ARCHIVE_FORMAT_EGG,
    ARCHIVE_FORMAT_GZ,
    # ARCHIVE_FORMAT_IMG,
    # ARCHIVE_FORMAT_ISO,
    # ARCHIVE_FORMAT_ISZ,
    ARCHIVE_FORMAT_LHA,
    ARCHIVE_FORMAT_LZ,
    ARCHIVE_FORMAT_LZH,
    ARCHIVE_FORMAT_LZMA,
    ARCHIVE_FORMAT_PMA,
    ARCHIVE_FORMAT_RAR,
    # ARCHIVE_FORMAT_RAR5,
    # ARCHIVE_FORMAT_SFX_EXE,
    ARCHIVE_FORMAT_TAR,
    ARCHIVE_FORMAT_TBZ,
    ARCHIVE_FORMAT_TBZ2,
    ARCHIVE_FORMAT_TGZ,
    ARCHIVE_FORMAT_TLZ,
    ARCHIVE_FORMAT_TXZ,
    # ARCHIVE_FORMAT_UDF,
    # ARCHIVE_FORMAT_WIM,
    # ARCHIVE_FORMAT_XPI,
    ARCHIVE_FORMAT_XZ,
    ARCHIVE_FORMAT_Z,
    ARCHIVE_FORMAT_ZIP,
    ARCHIVE_FORMAT_ZIPX,
    ARCHIVE_FORMAT_ZPAQ,
    ARCHIVE_FORMAT_ZSTD,
    ARCHIVE_FORMAT_BR,
    ARCHIVE_FORMAT_NSIS,
]

CMD_ADD_FILES = 'a'                     # Add files to archive
CMD_EXTRACT_WITH_FULL_PATH =  'x'       # eXtract files with full pathname
CMD_TEST_INTEGRITY = 't'                # Test integrity of archive
CMD_DELETE_FILES = 'd'                  # Delete files from archive
CMD_CREATE_ARCHIEVE = 'c'               # Create new archive(or overwrite exist file)
CMD_CREATE_ARCHIEVE_WITH_DIALOG = 'cd'  # Display “New Archive” dialog box
CMD_EXTRACT_WITHOUT_FULL_PATH = 'e'     # Extract files without directory names
CMD_LIST_CONTENTS = 'l'                 # List contents of archive
CMD_LIST_CONTENTS_VERBOSELY = 'v'       # Verbosely list contents of archive(ZIP format only)
CMD_RENAME_FILES = 'rn'                 # Rename files in archive

CMDS_LIST = [
    CMD_ADD_FILES,
    CMD_EXTRACT_WITH_FULL_PATH,
    CMD_TEST_INTEGRITY,
    CMD_DELETE_FILES,
    CMD_CREATE_ARCHIEVE,
    CMD_CREATE_ARCHIEVE_WITH_DIALOG,
    CMD_EXTRACT_WITHOUT_FULL_PATH,
    CMD_LIST_CONTENTS,
    CMD_LIST_CONTENTS_VERBOSELY,
    CMD_RENAME_FILES,
]

is_bcommand = lambda cmd: cmd.startswith('b')

OVERWRITE_OPTION_OVERWRITE_ALL = '-aoa'
OVERWRITE_OPTION_SKIP = '-aos'
OVERWRITE_OPTION_AUTORENAME = '-aou'

OVERWRITE_OPTIONS_LIST = [
    OVERWRITE_OPTION_OVERWRITE_ALL,
    OVERWRITE_OPTION_SKIP,
    OVERWRITE_OPTION_AUTORENAME
]

TARGET_OPTION_DLG="-target:dlg"
TARGET_OPTION_AUTO="-target:auto"
TARGET_OPTION_NAME="-target:name"

TARGET_OPTIONS_LIST = [
    TARGET_OPTION_DLG,
    TARGET_OPTION_AUTO,
    TARGET_OPTION_NAME,
]

def is_supported_for_compress(file_path):
    formats = '(('+')|('.join(SUPPORTED_FORMATS_COMPRESS)+'))' 
    file_regex = f'.*\.{formats}(\.[0-9]+)?'
    return re.fullmatch(file_regex, file_path.lower()) is not None

def is_supported_for_decompress(file_path):
    formats = '(('+')|('.join(SUPPORTED_FORMATS_DECOMPRESS)+'))' 
    file_regex = f'.*\.{formats}(\.[0-9]+)?'
    return re.fullmatch(file_regex, file_path.lower()) is not None

def _execute_cmd(bandizip_exe, command_or_bcommand, archive=None, switches_list=None, files_list=None, path_to_extract=None, logger=logging):
    
    assert command_or_bcommand in CMDS_LIST, 'Unknown command!'
    assert not is_bcommand(command_or_bcommand) or archive, f'archive argument is invalid: {archive}'

    full_command_parts = []
    full_command_parts.append(f'"{os.path.abspath(bandizip_exe)}"' if os.path.isfile(bandizip_exe) else bandizip_exe)
    full_command_parts.append(command_or_bcommand)
    full_command_parts.append(' '.join(switches_list)) if switches_list else None
    full_command_parts.append(f'"{os.path.abspath(archive)}"') if not is_bcommand(command_or_bcommand) else None
    full_command_parts.append(' '.join(files_list)) if files_list else None
    full_command_parts.append(path_to_extract) if not is_bcommand(command_or_bcommand) and path_to_extract else None
    full_command = ' '.join(full_command_parts)
    logger.debug(f'command : {full_command}')

    return_val = {}
    try:
        return_val['cmd'] = full_command
        return_val['output'] = subprocess.check_output(full_command, stdin=subprocess.DEVNULL, stderr=subprocess.STDOUT).decode()
        return_val['returncode'] = 0
    except subprocess.CalledProcessError as reason:
        return_val['cmd'] = reason.cmd
        return_val['returncode'] = reason.returncode
        return_val['output'] = reason.output.decode()
        logger.debug(f'stdout:{reason.stdout}')
        logger.debug(f'stderr:{reason.stderr}')
    finally:
        logger.debug(f'return_val: {return_val}')

    return return_val

def extract_files(bandizip_exe, archive_path, output_dir=None, with_full_paths=True, files_list_regex=None, overwrite_option=OVERWRITE_OPTION_OVERWRITE_ALL, enable_recursive_subdir=True, store_root=None, assume_yes_for_all=True, target_option=None, path_to_extract=None, logger=logging):

    assert os.path.isfile(archive_path), f'file does not exist: {archive_path}'
    assert overwrite_option in OVERWRITE_OPTIONS_LIST, f'invalid overwrite_option argument: {overwrite_option}'
    assert target_option is None or target_option in TARGET_OPTIONS_LIST, 'Invalid target_option'

    command = CMD_EXTRACT_WITH_FULL_PATH if with_full_paths else CMD_EXTRACT_WITHOUT_FULL_PATH
    logger.debug(f'command: {command}')

    switches = []
    switches.append(f'-o:"{output_dir}"') if output_dir else None
    switches.append('-y') if assume_yes_for_all else None
    switches.append(overwrite_option)
    switches.append('-r') if enable_recursive_subdir else switches.append('-r-') if enable_recursive_subdir == False else None
    switches.append('-storeroot:yes') if store_root else None
    switches.append(target_option) if target_option else None
    logger.debug(f'switches: {switches}')

    return _execute_cmd(bandizip_exe, command, archive=archive_path, switches_list=switches, files_list=files_list_regex, path_to_extract=path_to_extract, logger=logger)

def add_files_to_archive(bandizip_exe, files_list_regex, archive_path, archive_format=None, compress_level = None, exclude_files_list_regex=None, root_dir=None, overwrite_archive=False, with_dialog=False, sfx_path=None, use_zopfli=None, enable_recursive_subdir=True, store_root=None, volume_sizes_list=None, no_of_CPU_threads=None, zip_file_comment=None, zip_file_comment_path_txt=None, assume_yes_for_all=True, email=None, path_to_extract=None, logger=logging):

    assert no_of_CPU_threads is None or (no_of_CPU_threads < 100 and no_of_CPU_threads > 0) , f'invalid no_of_CPU_threads arg, supposed to be between 0 and 100 :{no_of_CPU_threads}'
    assert compress_level is None or (compress_level>=0 and compress_level<10), f'invalid compress_level argument: {compress_level}'
    assert sfx_path is None or os.path.isfile(sfx_path), f'invalid sfx_path argument: {sfx_path}'
    assert zip_file_comment_path_txt is None or os.path.isfile(zip_file_comment_path_txt), f'invalid zip_file_comment_path_txt argument: {zip_file_comment_path_txt}'

    if overwrite_archive and with_dialog:
        command = CMD_CREATE_ARCHIEVE_WITH_DIALOG
    elif overwrite_archive and not with_dialog:
        command = CMD_CREATE_ARCHIEVE
    elif not overwrite_archive:
        command = CMD_ADD_FILES
        
    switches = []
    switches.append('-y') if assume_yes_for_all else None
    switches.append('-r') if enable_recursive_subdir else switches.append('-r-') if enable_recursive_subdir == False else None
    switches.append(f'-fmt:{archive_format}') if archive_format else None
    switches.append(f'-t:{no_of_CPU_threads}') if no_of_CPU_threads else None
    switches.append(f'-l:{compress_level}') if compress_level else None
    switches.append(f'-sfx:"{os.path.abspath(sfx_path)}"') if sfx_path else None
    switches.append(f'-zopfli') if use_zopfli else None
    switches.append(f'-storeroot:yes') if store_root else None
    switches.append('ex:"{}"'.format(';'.join(exclude_files_list_regex))) if exclude_files_list_regex else None
    switches.append(f'-root:{root_dir}') if root_dir else None
    switches.append(f'-cmt:{zip_file_comment}') if zip_file_comment else None
    switches.append(f'-cmtfile:{os.path.abspath(zip_file_comment_path_txt)}') if zip_file_comment_path_txt else None
    switches.append(f'-email') if email else None
    switches+= [f'-v:{x}' for x in volume_sizes_list] if volume_sizes_list else []

    return _execute_cmd(bandizip_exe, command, archive=archive_path, switches_list=switches, files_list=files_list_regex, path_to_extract=path_to_extract, logger=logger)
