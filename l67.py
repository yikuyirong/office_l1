import sqlite3
import os


def main():
    path = r"C:\Users\Public\iVMS-4200 Site"

    def _get_file_stat(file):
        return {"filename": file, "state": os.stat(file)}

    def _get_files_info(path):

        files_info = []

        for file in map(lambda p: os.path.join(path, p), os.listdir(path)):
            # print(file)
            if os.path.isfile(file):
                files_info.append(_get_file_stat(file))
            elif os.path.isdir(file):
                for fileinfo in _get_files_info(file):
                    files_info.append(fileinfo)

        return files_info

    if os.path.isdir(path):

        for info in sorted([(fileinfo["filename"], fileinfo["state"].st_mtime) for fileinfo in _get_files_info(path)],key=lambda x:x[1],reverse=True)[0:20]:
            print(info)


if __name__ == '__main__':
    main()
