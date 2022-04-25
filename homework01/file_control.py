import os

# veriicar se aquivo existe em diretório
def isExist(file_path):
    return os.path.isfile(file_path)

# retorna tamanho do arquivo em MB
def getFile_size(file_path):
    return os.path.getsize(file_path)/(1024 * 1024)

# retorna um dicionário com o nome e tamanho dos arquivos existentes
def list_files_dir(dir_files):
    files = dict()

    os.environ['HOME']
    files = os.listdir(dir_files)

    # list_path_files_with_size = ''

    for file in files:
        file_path = os.path.join(dir_files, file)
        file_size = os.path.getsize(file_path)

        files[file_path.replace(dir_files, '')] = float(file_size/(1024 * 1024))

    # return list_path_files_with_size
    return files
