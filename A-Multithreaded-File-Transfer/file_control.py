import os

# verificando se aquivo existe no diretório
def isExist(file_path):
    return os.path.isfile(file_path)

# pegando o tamanho do arquivo
def getFile_size(file_path):
    return os.path.getsize(file_path)/(1024 * 1024)

# retornando o nome e tamanho dos arquivos
def list_files_dir(dir_files):

    os.environ['HOME']
    files = os.listdir(dir_files)

    # list_path_files_with_size = ''

    for file in files:
        file_path = os.path.join(dir_files, file)
        file_size = os.path.getsize(file_path)

        files[file_path.replace(dir_files, '')] = float(file_size/(1024 * 1024))

    # return list_path_files_with_size
    return files
