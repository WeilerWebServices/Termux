U
    ��_:*  �                   @   s�   d dl Z d dlZd dlZd dlZd dlZdZd ZdZdZ	G dd� de
�ZG dd� de
�ZG d	d
� d
e�ZG dd� de
�ZG dd� de
�ZG dd� de�ZdS )�    N�   �   �   c                   @   s   e Zd ZdZdd� ZdS )�FilePoszd
    This class keeps track of the file object representing and current position
    in a file.
    c                 C   s   d | _ d| _d S )Nr   )�file�pos��self� r
   �M/storage/emulated/0/python/pyinstaller/PyInstaller/loader/pyimod02_archive.py�__init__2   s    zFilePos.__init__N)�__name__�
__module__�__qualname__�__doc__r   r
   r
   r
   r   r   -   s   r   c                   @   s8   e Zd ZdZdd� Zdd� Zdd� Zdd	� Zd
d� ZdS )�ArchiveFilez�
    File class support auto open when access member from file object
    This class is use to avoid file locking on windows
    c                 O   s   || _ || _i | _d S �N)�args�kwargs�_filePos)r	   r   r   r
   r
   r   r   ?   s    zArchiveFile.__init__c                 C   s(   t �� }|| jkrt� | j|< | j| S )z�
        Return an instance of FilePos for the current thread. This is a crude
        # re-implementation of threading.local, which isn't a built-in module
        # and therefore isn't available.
        )�thread�	get_identr   r   )r	   Ztir
   r
   r   �localD   s    
zArchiveFile.localc                 C   s   | � � j}|st�t||�S )zr
        Make this class act like a file, by invoking most methods on its
        underlying file object.
        )r   r   �AssertionError�getattr)r	   �namer   r
   r
   r   �__getattr__O   s    
zArchiveFile.__getattr__c                 C   s4   | � � }|jrt�t| j| j�|_|j�|j� dS )zC
        Open file and seek to pos record from last close.
        N)r   r   r   �openr   r   �seekr   )r	   �fpr
   r
   r   �	__enter__X   s    
zArchiveFile.__enter__c                 C   s2   | � � }|jst�|j�� |_|j��  d|_dS )z,
        Close file and record pos.
        N)r   r   r   �tellr   �close)r	   �type�value�	tracebackr   r
   r
   r   �__exit__c   s
    

zArchiveFile.__exit__N)	r   r   r   r   r   r   r   r    r&   r
   r
   r
   r   r   9   s   	r   c                   @   s   e Zd ZdS )�ArchiveReadErrorN)r   r   r   r
   r
   r
   r   r'   q   s   r'   c                   @   sV   e Zd ZdZdZdZdZdZdZddd�Z	d	d
� Z
dd� Zdd� Zdd� Zdd� ZdS )�ArchiveReadera  
    A base class for a repository of python code objects.
    The extract method is used by imputil.ArchiveImporter
    to get code objects by name (fully qualified name), so
    an enduser "import a.b" would become
      extract('a.__init__')
      extract('a.b')
    s   PYL �   �   Nr   c              	   C   s`   d| _ || _|| _ddl}|jj| _|dk	r\t| jd�| _| j� | �	�  | �
�  W 5 Q R X dS )zY
        Initialize an Archive. If path is omitted, it will be an empty Archive.
        Nr   �rb)�toc�path�start�_frozen_importlib�_bootstrap_external�MAGIC_NUMBER�pymagicr   �lib�
checkmagic�loadtoc)r	   r-   r.   r/   r
   r
   r   r   �   s    
zArchiveReader.__init__c                 C   sV   | j �| j| j � t�d| j �d��\}| j �| j| � tt�	| j �� ��| _
dS )z�
        Overridable.
        Default: After magic comes an int (4 byte native) giving the
        position of the TOC within self.lib.
        Default: The TOC is a marshal-able string.
        z!i�   N)r3   r   r.   �TOCPOS�struct�unpack�read�dict�marshal�loadsr,   )r	   �offsetr
   r
   r   r5   �   s    zArchiveReader.loadtocc                 C   s&   | j �|d�\}}|d krd S t|�S )N�r   N)r,   �get�bool)r	   r   �ispkgr   r
   r
   r   �
is_package�   s    zArchiveReader.is_packagec              	   C   sZ   | j �|d�\}}|dkrdS | j�( | j�| j| � t�| j�� �}W 5 Q R X ||fS )a*  
        Get the object corresponding to name, or None.
        For use with imputil ArchiveImporter, object is a python code object.
        'name' is the name as specified in an 'import name'.
        'import a.b' will become:
        extract('a') (return None because 'a' is not a code object)
        extract('a.__init__') (return a code object)
        extract('a.b') (return a code object)
        Default implementation:
          self.toc is a dict
          self.toc[name] is pos
          self.lib has the code object marshal-ed at pos
        r?   N)r,   r@   r3   r   r.   r<   r=   r:   )r	   r   rB   r   �objr
   r
   r   �extract�   s    zArchiveReader.extractc                 C   s   t | j�� �S )z�
        Return a list of the contents
        Default implementation assumes self.toc is a dict like object.
        Not required by ArchiveImporter.
        )�listr,   �keysr   r
   r
   r   �contents�   s    zArchiveReader.contentsc                 C   sr   | j �| j� | j �t| j��| jkr<td| j| jj	f ��| j �t| j
��| j
krbtd| j ��| j �d� dS )zz
        Overridable.
        Check to see if the file object self.lib actually has a file
        we understand.
        z!%s is not a valid %s archive filez%s has version mismatch to dllr6   N)r3   r   r.   r:   �len�MAGICr'   r-   �	__class__r   r2   r   r
   r
   r   r4   �   s    ��zArchiveReader.checkmagic)Nr   )r   r   r   r   rJ   �HDRLENr7   �osZ	_bincacher   r5   rC   rE   rH   r4   r
   r
   r
   r   r(   u   s   
r(   c                   @   s(   e Zd ZdZdd� Zdd� Zdd� ZdS )	�Cipherz<
    This class is used only to decrypt Python modules.
    c                 C   sr   dd l }|j}t|�tkst�t|�tkr:|dt� | _n|�t�| _t| j�tksXt�dd l}|| _	t
jd= d S )Nr   �tinyaes)�pyimod00_crypto_key�keyr#   �strr   rI   �CRYPT_BLOCK_SIZE�zfillrO   �_aesmod�sys�modules)r	   rP   rQ   rO   r
   r
   r   r   �   s    zCipher.__init__c                 C   s   | j �| j�� |�S r   )rU   ZAESrQ   �encode)r	   Zivr
   r
   r   Z__create_cipher  s    zCipher.__create_cipherc                 C   s$   | � |d t� �}|�|td � �S r   )�_Cipher__create_cipherrS   ZCTR_xcrypt_buffer)r	   �data�cipherr
   r
   r   �decrypt  s    zCipher.decryptN)r   r   r   r   r   rY   r\   r
   r
   r
   r   rN   �   s   rN   c                       sD   e Zd ZdZdZdZejd Zd� fdd�	Zdd	� Z	d
d� Z
�  ZS )�ZlibArchiveReaderaD  
    ZlibArchive - an archive with compressed entries. Archive is read
    from the executable created by PyInstaller.

    This archive is used for bundling python modules inside the executable.

    NOTE: The whole ZlibArchive (PYZ) is compressed so it is not necessary
          to compress single modules with zlib.
    s   PYZ r*   �   Nc              	      s�   |d krd}nt|d kr�t t|�d dd�D ]R}|| dkr*zt||d d � �}W n tk
rj   Y q*Y nX |d |� } q�q*d}tt| ��||� zdd l}t� | _	W n t
k
r�   d | _	Y nX d S )Nr   r   ������?)�rangerI   �int�
ValueError�superr]   r   rP   rN   r[   �ImportError)r	   r-   r>   �irP   �rK   r
   r   r     s$    
zZlibArchiveReader.__init__c                 C   s(   | j �|d�\}}}|d kr d S |tkS )N�r   Nr   )r,   r@   �PYZ_TYPE_PKG)r	   r   �typr   �lengthr
   r
   r   rC   5  s    zZlibArchiveReader.is_packagec              
   C   s�   | j �|d�\}}}|d kr d S | j�$ | j�| j| � | j�|�}W 5 Q R X z6| jrd| j�|�}t�	|�}|t
tfkr�t�|�}W n0 tk
r� } ztd| �|�W 5 d }~X Y nX ||fS )Nrh   z"PYZ entry '%s' failed to unmarshal)r,   r@   r3   r   r.   r:   r[   r\   �zlib�
decompress�PYZ_TYPE_MODULEri   r<   r=   �EOFErrorre   )r	   r   rj   r   rk   rD   �er
   r
   r   rE   ;  s&    
��zZlibArchiveReader.extract)NN)r   r   r   r   rJ   r7   r(   rL   r   rC   rE   �__classcell__r
   r
   rg   r   r]     s   	
r]   )r<   r8   rV   rl   �_threadr   rS   rn   ri   �PYZ_TYPE_DATA�objectr   r   �RuntimeErrorr'   r(   rN   r]   r
   r
   r
   r   �<module>   s   8u"