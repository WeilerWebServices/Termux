U
    ��_�&  �                   @   s  d Z ddlZddlZddlZddlZddl	Z
ddlZejejB ejB ejB ejB ejB ZejejB ejB Ze
jd dkr�ddlmZ ddlmZ G dd� de�ZG dd� de�ZnddlmZ dd	lmZ d
d� ZeZddd�Zdd� Z dd� Z!dd� Z"dd� Z#dd� Z$dd� Z%dd� Z&dS )z�
A helper module that can work with paths
that can refer to data inside a zipfile

XXX: Need to determine if isdir("zipfile.zip")
should return True or False. Currently returns
True, but that might do the wrong thing with
data-files that are zipfiles.
�    N�   )�StringIOc                   @   s   e Zd Zdd� Zdd� ZdS )�	_StringIOc                 C   s   | S �N� ��selfr   r   �K/storage/emulated/0/python/pyinstaller/PyInstaller/lib/modulegraph/zipio.py�	__enter__$   s    z_StringIO.__enter__c                 C   s   | � �  dS �NF��close�r   �exc_type�	exc_value�	tracebackr   r   r	   �__exit__'   s    z_StringIO.__exit__N��__name__�
__module__�__qualname__r
   r   r   r   r   r	   r   #   s   r   c                   @   s   e Zd Zdd� Zdd� ZdS )�_BytesIOc                 C   s   | S r   r   r   r   r   r	   r
   ,   s    z_BytesIO.__enter__c                 C   s   | � �  dS r   r   r   r   r   r	   r   /   s    z_BytesIO.__exit__Nr   r   r   r   r	   r   +   s   r   )�BytesIOc                 C   s�   | }t j�| �r| d fS g }t j�| �}| r^| |kr^t j�| �\} }|�|� t j�| �r(q^q(| |krtttj|d��t j�	| �s�ttj|d��|�
�  | d�|��d�fS d S )N�No such file or directory�/)�_os�path�exists�
splitdrive�split�append�IOError�_errno�ENOENT�isfile�reverse�join�strip)r   �	full_path�rest�rootZbnr   r   r	   �_locate8   s0    
 � �r+   �rc              	   C   s  d|ksd|kr t tj| d��nd|kr6t tj| d��| }t| �\} }|sTt| |�S zt�| d�}W n$ tjk
r�   t tj|d��Y nX z|�	|�}W n0 tjt
fk
r�   |��  t tj|d��Y nX |��  |dkr�t|�S tjd d	kr�|�d
�}t|�S d S )N�w�azWrite access not supportedzr+r,   r   �rbr   �   �ascii)r!   r"   �EINVALr+   �_open�_zipfile�ZipFile�errorr#   �read�KeyErrorr   r   �_sys�version_info�decoder   )r   �moder(   r)   �zf�datar   r   r	   �openW   sN      �  �
 �
 �

r?   c                 C   s`  | }t | �\} }|s*tj�| �s*t�| �S zt�| d�}W n$ tjk
r^   tt	j
|d��Y nX t� }d}z�|�� D ]�}|d kr�d}|�d�d }|r�|�|� qt|�|�rt||kr�d}d}n8|t|� dkr�d}|t|�d d � �d�d }nd }|rt|�|� qtW n. tjk
�r6   |��  tt	j
|d��Y nX |��  |�sTtt	j
|d��t|�S d S )	Nr,   r   FTr   r   � �   )r+   r   r   r$   �listdirr4   r5   r6   r!   r"   r#   �set�namelistr   �add�
startswith�lenr   �list)r   r(   r)   r=   �result�seen�nm�valuer   r   r	   rB   �   s^    
 �

  �
 �rB   c                 C   s  | }t | �\} }|sXtj�| �}|rTzt�| d�}W dS  tjtfk
rR   Y dS X dS d }z$t�| d�}|�|� |�	�  W dS  t
tjfk
�r   |d k	r�|�	�  z|�|d � W n t
k
r�   Y nX Y dS |d }|�� D ]}|�|�r� Y dS q�ttj|d��Y nX d S )Nr,   FTr   r   )r+   r   r   r$   r4   r5   r6   r!   �getinfor   r8   rD   rF   r"   r#   �r   r(   r)   �okr=   rK   r   r   r	   r$   �   sD    


 �r$   c              	   C   sD  | }t | �\} }|sZtj�| �}|sVzt�| d�}W n tjtfk
rP   Y dS X dS dS d }z�zt�| �}W n$ tjk
r�   tt	j
|d��Y nX z|�|� W n tk
r�   Y n
X W �pdS |d }z|�|� W n tk
r�   Y n
X W �<dS |�� D ]}|�|�� r� W �dS � q�tt	j
|d��W 5 |d k	�r>|��  X d S )Nr,   FTr   r   )r+   r   r   �isdirr4   r5   r6   r!   r   r"   r#   rM   r8   rD   rF   rN   r   r   r	   rP   �   sT     �
 �
rP   c                 C   s�   | }t | �\} }|s tj�| �S zt�| �}W n$ tjk
rR   ttj	|d��Y nX z�z|�|� W n tk
rx   Y n
X W �ldS |d7 }z|�|� W n tk
r�   Y n
X W �8dS |�� D ]}|�|�r� W �dS q�ttj	|d��W 5 |�
�  X d S )Nr   Fr   )r+   r   r   �islinkr4   r5   r6   r!   r"   r#   r   rM   r8   rD   rF   )r   r(   r)   r=   rK   r   r   r	   rQ     sB     �

 �rQ   c                 C   s,   | }t | �\} }|r"ttj|d��t�| �S )Nr   )r+   �OSErrorr"   r#   r   �readlink)r   r(   r)   r   r   r	   rS   ?  s     �rS   c                 C   s  | }t | �\} }|s&t�t�| �j�S d }z�t�| �}d }z|�	|�}W n t
k
r\   Y nX |d kr�z|�	|d �}W n t
k
r�   Y nX |d kr�|d }|�� D ]}|�|�r� q�q�ttj|d��tW �0S |jd? dkr�t�|jd? �W �S tW �S W 5 |d k	�r|��  X d S )Nr   r   �   r   )r+   �_stat�S_IMODEr   �stat�st_moder   r4   r5   rM   r8   rD   rF   r!   r"   r#   �_DFLT_DIR_MODE�external_attr�_DFLT_FILE_MODE�r   r(   r)   r=   �inforK   r   r   r	   �getmodeK  sB    

 �
r^   c                 C   s�   | }t | �\} }|s tj�| �S d }z�t�| �}d }z|�|�}W n tk
rV   Y nX |d kr�z|�|d �}W n tk
r�   Y nX |d kr�|d }|�	� D ]}|�
|�r� q�q�ttj|d��tj�| �W �S t�|jd �W �S |d k	r�|��  X d S )Nr   r   )r   r   �����)r+   r   r   �getmtimer   r4   r5   rM   r8   rD   rF   r!   r"   r#   �_time�mktime�	date_timer\   r   r   r	   r`   y  s>    

 �r`   )r,   )'�__doc__�osr   �zipfiler4   �errnor"   �timera   �sysr9   rW   rU   �S_IXOTH�S_IXGRP�S_IXUSR�S_IROTH�S_IRGRP�S_IRUSRrY   r[   r:   r   Z_BaseStringIOZ_BaseBytesIOr   r   �ior   r+   r?   r3   rB   r$   rP   rQ   rS   r^   r`   r   r   r   r	   �<module>   sR   	������	���	
)6+3+.