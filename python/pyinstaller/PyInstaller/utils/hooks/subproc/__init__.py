U
    ��_�t  �                4   @   sJ  d dl Z d dlZd dlZd dlZddlmZmZmZmZ d dl	m
Z
mZ ddlmZ ddlmZmZmZ ddlmZ e�e�ZG d	d
� d
�Zed�Zed�Zdd� Zdd� Zdd� ZdHdd�Zdddddddddddd d!d"d#d$d%d&d'd(d)d*d+dd,d-d-d.d/d0d1d2ddd3d4d5d6d7d8d9d:dd;dddd<d=d>d?d@�3ZdAdB� Z dCdD� Z!dEdF� Z"dGZ#dS )I�    N�   )�eval_statement�exec_statement�get_homebrew_path�get_module_file_attribute)�
getImports�getfullnameof�   )�log)�is_win�	is_darwin�is_linux)�miscc                   @   s   e Zd Zdd� Zdd� ZdS )�Qt5LibraryInfoc                 C   s*   |dkrt d�|���|| _|dk| _d S )N��PyQt5�PySide2�Invalid namespace: {0}r   )�	Exception�format�	namespace�is_PyQt5)�selfr   � r   �D/storage/emulated/0/python/pyinstaller/PyInstaller/utils/hooks/qt.py�__init__!   s    zQt5LibraryInfo.__init__c              
   C   s�   d| j kr�td| j �}zt�|�}W n8 tk
r^ } zt�dt|�|� d}W 5 d }~X Y nX |sld | _	n|�
� D ]\}}t| ||� qtt| |�S t�d S )N�versiona"  
                import sys

                # exec_statement only captures stdout. If there are
                # errors, capture them to stdout so they can be displayed to the
                # user. Do this early, in case PyQt5 imports produce stderr
                # output.
                sys.stderr = sys.stdout

                import json
                try:
                    from %s.QtCore import QLibraryInfo, QCoreApplication
                except:
                    print('False')
                else:
                    # QLibraryInfo isn't always valid until a QCoreApplication is
                    # instantiated.
                    app = QCoreApplication(sys.argv)
                    paths = [x for x in dir(QLibraryInfo) if x.endswith('Path')]
                    location = {x: QLibraryInfo.location(getattr(QLibraryInfo, x))
                                for x in paths}
                    try:
                        version = QLibraryInfo.version().segments()
                    except AttributeError:
                        version = []
                    print(json.dumps({
                        'isDebugBuild': QLibraryInfo.isDebugBuild(),
                        'version': version,
                        'location': location,
                    }))
            z<Cannot read QLibraryInfo output: raised %s when decoding:
%sF)�__dict__r   r   �json�loadsr   �logger�warning�strr   �items�setattr�getattr�AttributeError)r   �nameZjson_strZqli�e�k�vr   r   r   �__getattr__)   s$    
� �
zQt5LibraryInfo.__getattr__N)�__name__�
__module__�__qualname__r   r+   r   r   r   r   r       s   r   r   r   c                 C   s�   | dkrt d�| ���| dkr,tjd g}n$| dkrBtjd g}ntd�| ��}|sdt d�| ���n,g }|D ]}tj�|�rl|�	t
|�� ql|}|s�t d�| d	�|����|S )
z�
    Return list of paths searched for plugins.

    :param namespace: Import namespace, i.e., PyQt4, PyQt5, PySide, or PySide2

    :return: Plugin directory paths
    ��PyQt4r   �PySider   r   r   ZPluginsPathr   z�
            from {0}.QtCore import QCoreApplication;
            app = QCoreApplication([]);
            print(list(app.libraryPaths()))
            z"Cannot find {0} plugin directorieszd
            Cannot find existing {0} plugin directories
            Paths checked: {1}
            �, )r   r   �pyqt5_library_info�location�pyside2_library_infor   �os�path�isdir�appendr"   �join)r   �pathsZvalid_pathsr7   Zqt_plugin_pathsr   r   r   �qt_plugins_dirc   s,    � �r<   c              	      s�   |dkrt d�|���t|d�}g }|D ]}|�t�tj�|| ��� q(t	rd|dkrddd� |D �}nt	r~|dkr~dd� |D �}t
�d	|| � |dkr�d
}n(|dkr�tj�ddd�}ntj�dd�}tj�|| �� � fdd�|D �}|S )a  
    Return list of dynamic libraries formatted for mod.binaries.

    :param plugin_type: Plugin to look for
    :param namespace: Import namespace, i.e., PyQt4, PyQt5, PySide, or PySide2

    :return: Plugin directory path corresponding to the given plugin_type
    r/   r   �r   )r0   r1   c                 S   s   g | ]}|� d �s|�qS )zd4.dll��endswith��.0�fr   r   r   �
<listcomp>�   s     
 z'qt_plugins_binaries.<locals>.<listcomp>r   c                 S   s   g | ]}|� d �s|�qS )zd.dllr>   r@   r   r   r   rC   �   s     
 z#Found plugin files %s for plugin %sZqt4_pluginsr   �Qt�pluginsr   c                    s   g | ]}|� f�qS r   r   r@   ��dest_dirr   r   rC   �   s     )r   r   r<   �extendr   �dlls_in_dirr6   r7   r:   r   r    �debug)Zplugin_typer   Zpdir�filesr7   Z
plugin_dir�binariesr   rF   r   �qt_plugins_binaries�   s&    	
rM   c                 C   s�   | dkrt d�| ���d}td�| ��}tj�tjddd�}tj�|d�tj�|dd�|g}|D ]4}tj�|d	�}tj�|�r`|}t	�
d
| |�  q�q`|s�t d�| d�|����|S )z�
    Return path to Qt resource dir qt_menu.nib on OSX only.

    :param namespace: Import namespace, i.e., PyQt4, PyQt5,  PySide, or PySide2

    :return: Directory containing qt_menu.nib for specified namespace
    r/   r   Nzz
    from {0}.QtCore import QLibraryInfo
    path = QLibraryInfo.location(QLibraryInfo.LibrariesPath)
    print(path)
    z
python.appZContentsZ	ResourceszQtGui.frameworkzqt_menu.nibzFound qt_menu.nib for %s at %szW
            Cannot find qt_menu.nib for {0}
            Path checked: {1}
            r2   )r   r   r   r6   r7   r:   �sys�exec_prefix�existsr    rJ   )r   Zmenu_dirr7   Zanaconda_pathr;   r4   r   r   r   �qt_menu_nib_dir�   s2    �� � �rQ   � c              
   C   s*  ddl }dtjkr>| d dkr>t�d� tj�tjd dd�S dtjkrt| d d	krtt�d
� tj�tjd dd�S dg}dD ]}t|�}|r~|�|� q~|D ]z}zXtj�|dd�}|�	|ddg��
� }|�d�}|�| �dkr�t�d||� |W   S W q� t|jfk
�r   Y q�X q�t�d| � dS )z~
    Try to find the path to qmake with version given by the argument as a
    string.

    :param version: qmake version
    r   NZQT5DIR�5zUsing $QT5DIR/bin as qmake path�bin�qmakeZQT4DIR�4zUsing $QT4DIR/bin as qmake pathrR   )�qt�qt5z-queryZ
QT_VERSION�utf8z!Found qmake version "%s" at "%s".z+Could not find qmake matching version "%s".)�
subprocessr6   �environr    rJ   r7   r:   r   r9   �check_output�strip�decode�find�OSError�CalledProcessError)r   rZ   �dirs�formulaZhomebrewqtpath�	directoryrU   Zversionstringr   r   r   �get_qmake_path�   s:    

�

 �re   )z.QtBluetoothN)N�qtbase)z.QtCorerf   )z.QtDBusN)NZqtquick1Zqml1tooling)z.QtDesignerN)NN)NNZgamepads)	z.QtGuirf   Z
accessibleZiconenginesZimageformatsZ	platformsZplatforminputcontextsZplatformthemesZstyles)z.QtHelpZqt_help)z.QtMacExtrasN)z.QtMultimedia�qtmultimediaZaudioZmediaserviceZplaylistformats)z.QtMultimediaWidgetsrg   )Nrg   )z
.QtNetworkrf   Zbearer)z.QtNfcN)z	.QtOpenGLN�xcbglintegrations�egldeviceintegrations)z.QtPositioningN�position)z.QtPrintSupportNZprintsupport)z.QtQml�qtdeclarative)NN�
qmltooling)z.QtQuickrk   Z
scenegraphrl   rh   ri   )z.QtQuickWidgetsN)NZqtscript)z
.QtSensorsNZsensorsZsensorgestures)z.QtSerialPortZqtserialport)z.QtSqlrf   Z
sqldrivers)z.QtSvgN)z.QtTestrf   )z.QtWebSocketsN)z
.QtWidgetsrf   )z.QtWinExtrasN)z.QtXmlrf   )z.QXmlPatternsZqtxmlpatterns)z.QtWebEngineCoreN�qtwebenginerh   ri   )z.QtWebEnginerm   rm   )z.QtWebEngineWidgetsNrm   )NNZsceneparsersZrenderpluginsZgeometryloaders)z.QtLocationNZgeoservices)z.QtWebChannelN)NNZtexttospeech)NNZcanbus)3Zqt5bluetoothZqt5concurrentZqt5coreZqtdbusZqt5declarativeZqt5designerZqt5designercomponentsZenginioZ
qt5gamepadZqt5guiZqt5helpZqt5macextrasZqt5multimediaZqt5multimediawidgetsZqt5multimediaquick_pZ
qt5networkZqt5nfcZ	qt5openglZqt5positioningZqt5printsupportZqt5qmlrl   Zqt5quickZqt5quickparticlesZqt5quickwidgetsZ	qt5scriptZqt5scripttoolsZ
qt5sensorsZqt5serialportZqt5sqlZqt5svgZqt5testZ	qt5webkitZqt5webkitwidgetsZqt5websocketsZ
qt5widgetsZqt5winextrasZqt5xmlZqt5xmlpatternsZqt5webenginecoreZqt5webengineZqt5webenginewidgetsZ	qt53dcoreZqt53drenderZ
qt53dquickZqt53dquickRenderZ
qt53dinputZqt5locationZqt5webchannelZqt5texttospeechZqt5serialbusc              	   C   s�  t � }t � }t � }tj�tj�| ��\}}|�d�s8t�|�d�sFt�|dd � }|�d�d }|dkrvtd�	|���|dk}|r�t
jr�|s�tjs�g g g fS t|�}	t�d	|	| � t t|	��}
|
�r|
�� }tr�t||r�t
jd
 ntjd
 �}tj�tj�|��d �� }t�r6tj�|�d dk�r6tj�|�d }|�d��rN|dd � }t�rp|�d��rpd|dd �  }|�d��r�|d d� }t�d||� |tkr�t�d|� |
�t|�� t| }|d d� \}}|dd � }|�r�|�|| g� |�|� |r�|�|g� q�g }|D ]}t||d�}|�|� �q|�rDt
jd ntjd }g }|D ]\}tj�||d �}t�|��r�|�|tj�||�s�t�r�dndd�f� nt� d|� �qVt!|�}t�d||||� |||fS )Nz.pyzhook-�   �.r   r   r   r   z8add_qt5_dependencies: Examining %s, based on hook of %s.�BinariesPath�   z.so�libr	   rW   rX   r   Z_condai����z1add_qt5_dependencies: raw lib %s -> parsed lib %sz#add_qt5_dependencies: Import of %s.r=   ZTranslationsPathz_*.qmrR   rD   ZtranslationszIUnable to find Qt5 translations %s. These translations were not packaged.zXadd_qt5_dependencies: imports from %s:
  hiddenimports = %s
  binaries = %s
  datas = %s)"�setr6   r7   �splitext�basename�
startswith�AssertionError�splitr   r   r3   r   r5   r   r    rJ   r   �popr   r   r4   �lowerr   r   r?   �_qt_dynamic_dependencies_dict�updaterM   rH   r:   �globr9   r!   �list)�	hook_file�hiddenimportsZtranslations_baserE   Z	hook_nameZhook_ext�module_namer   r   �module�imports�impZlib_name�ddZlib_name_hiddenimportsZlib_name_translations_baseZlib_name_pluginsrL   ZpluginZmore_binaries�tp�datas�tb�srcr   r   r   �add_qt5_dependencies�  s�    
��
 �� �
�  ��	�   �r�   c           	      C   sf   g }d}| D ]D}t j�|j|jr$dnd |�}t�|�}|D ]}|�||f� q<qt|�|krb|S g S )z�
    globs_to_include is a list of file name globs
    If the number of found files does not match num_files
    then no files will be included.
    ro   rp   Z
PrefixPath)r6   r7   r:   r4   r   r}   r9   �len)	Zglobs_to_includeZ	num_files�qt_library_infoZ
to_includeZdst_dll_path�dllZdll_pathZdll_file_pathsZdll_file_pathr   r   r   �find_all_or_none?  s    
��
r�   c                 C   sR   g }dddg}|t |d| �7 }dg}|t |d| �7 }ddd	g}|t |d| �7 }|S )
Nz
libEGL.dllzlibGLESv2.dllzd3dcompiler_??.dllr	   zopengl32sw.dllrq   zicudt??.dllzicuin??.dllzicuuc??.dll)r�   )r�   rL   Zangle_filesZopengl_software_rendererZ	icu_filesr   r   r   �get_qt_binaries]  s    

r�   )r<   rM   rQ   re   )rR   )$r6   rN   r   r}   �hooksr   r   r   r   ZPyInstaller.depend.bindependr   r   rR   r
   �logging�compatr   r   r   �utilsr   �	getLoggerr,   r    r   r3   r5   r<   rM   rQ   re   r{   r�   r�   r�   �__all__r   r   r   r   �<module>   s�   
	?$*%
 2�Cw