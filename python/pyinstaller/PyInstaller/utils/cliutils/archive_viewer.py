U
    ��_�#  �                   @   s�   d Z ddlZddlZddlZddlZddlZddlmZ ddl	m
Z
mZ e�e�Zdd� Zdd� Zg fd	d
�Zdd� Zdd� Zdd� Zdd� Zdd� Zdd� Zdd� Zdd� ZdS )zP
This module is for the miscellaneous routines which do not fit somewhere else.
�    N)�log)�BYTECODE_MAGIC�text_read_modec                 C   s,   g }t �| �D ]\}}}|�t|�� q|S )zLReturns a list *.dll, *.so, *.dylib in given directories and subdirectories.)�os�walk�extend�dlls_in_dir)�	directory�filelist�root�dirs�files� r   �@/storage/emulated/0/python/pyinstaller/PyInstaller/utils/misc.py�dlls_in_subdirs   s    r   c                 C   s   t | dddg�S )z:Returns a list of *.dll, *.so, *.dylib in given directory.z*.soz*.dllz*.dylib)�files_in_dir)r	   r   r   r   r   %   s    r   c              	   C   s,   g }|D ]}|� t�tj�| |��� q|S )zAReturns a list of files which match a pattern in given directory.)r   �globr   �path�join)r	   Zfile_patternsr   Zfile_patternr   r   r   r   *   s    r   c                  C   s>   g } zddl }| �d� W n tk
r8   t�d� Y nX | S )z^
    Try importing codecs and encodings to include unicode support
    in created binary.
    r   N�codecszCannot detect modules 'codecs'.)r   �append�ImportError�logger�error)�modulesr   r   r   r   �get_unicode_modules2   s    r   c                 C   sr   t j�t j�| ��}d}z@td�D ]2}tt �|��}||krJt j�|�}q"|  W S q"W n tk
rl   Y nX dS )a  
    Return the path to top-level directory that contains Python modules.

    It will look in parent directories for __init__.py files. The first parent
    directory without __init__.py is the top-level directory.

    Returned directory might be used to extend the PYTHONPATH.
    z__init__.py�
   N)r   r   �dirname�abspath�range�set�listdir�IOError)�filenameZcurr_dir�pattern�ir   r   r   r   �get_path_to_toplevel_modulesB   s    	r&   c                 C   s$   zt �| �d W S    Y dS X d S )N�   r   )r   �stat)�fnmr   r   r   �mtime^   s    r*   c                 C   s  t j�|d�}g }| D �]�\}}}|dkr<|�|||f� q|dkrFq|�d�r�|}|tjjrbdnd }t j�|�s�|tjjr�dnd }n|}|dd� }t	|�t	|�k}	|	s�t
|d	��}
|
�� dd
� tk}	W 5 Q R X |	�r�zt�||� t�d|� W � n� tk
�r�   t j�|�d }d|k�rL|�d�dd� |�d�d  }}n|�d�d }}t jj|f|�� }t j�|��s�t �|� t j�||| �}t	|�t	|�k}	|	�s�t
|d	��}
|
�� dd
� tk}	W 5 Q R X |	�r�t�||� t�d|� Y nX |�|||f� q|S )a�  
    Given a TOC or equivalent list of tuples, generates all the required
    pyc/pyo files, writing in a local directory if required, and returns the
    list of tuples with the updated pathnames.

    In the old system using ImpTracker, the generated TOC of "pure" modules
    already contains paths to nm.pyc or nm.pyo and it is only necessary
    to check that these files are not older than the source.
    In the new system using ModuleGraph, the path given is to nm.py
    and we do not know if nm.pyc/.pyo exists. The following logic works
    with both (so if at some time modulegraph starts returning filenames
    of .pyc, it will cope).
    Z
localpycos�PYMODULE)�-Nz.py�o�cN������rb�   zcompiled %s�   �__init__�.)r   r   r   r   �endswith�sys�flags�optimize�existsr*   �open�readr   �
py_compile�compiler   �debugr"   �splitext�split�makedirs)Ztoc�workpathZbasepath�new_toc�nmr)   �typZsrc_fnmZobj_fnmZneeds_compile�fh�extZleading�mod_namer   r   r   �compile_py_filesg   sR    
	
$
rI   c              	   C   sL   t j�| �}t j�|�s"t �|� t| ddd��}t�||� W 5 Q R X dS )zo
    Save data into text file as Python data structure.
    :param filename:
    :param data:
    :return:
    �w�utf-8��encodingN)r   r   r   r9   rA   r:   �pprint)r#   �datar   �fr   r   r   �save_py_data_struct�   s
    
rQ   c              
   C   s>   t | tdd��&}ddlm} t|�� �W  5 Q R � S Q R X dS )zc
    Load data saved as python code and interpret that code.
    :param filename:
    :return:
    rK   rL   �   )�BindingRedirectN)r:   r   Zdepend.bindependrS   �evalr;   )r#   rP   rS   r   r   r   �load_py_data_struct�   s    rU   c                 C   s   t j�t j�| ��S )N)r   r   r   �normpath)Zapathr   r   r   �absnormpath�   s    rW   c                 C   sB   d}g }| � d�dd� D ]"}||r,d| n|7 }|�|� q|S )z�
    Return list of parent package names.
        'aaa.bb.c.dddd' ->  ['aaa', 'aaa.bb', 'aaa.bb.c']
    :param full_modname: Full name of a module.
    :return: List of parent module names.
    � r4   r   r/   )r@   r   )Zfull_modname�prefix�parents�pkgr   r   r   �module_parent_packages�   s    r\   )�__doc__r   r   rN   r<   r6   �PyInstallerr   �loggingZPyInstaller.compatr   r   �	getLogger�__name__r   r   r   r   r   r&   r*   rI   rQ   rU   rW   r\   r   r   r   r   �<module>   s&   
	c