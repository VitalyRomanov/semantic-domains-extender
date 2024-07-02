import argparse
from multiprocessing import Pool
from pathlib import Path
import sqlite3
from typing import Generator
import zipfile
from io import BytesIO

import chardet
from tqdm import tqdm


def stream_subtitle_data_from_database(database_path, data_column_name="content", table_name="zipfiles") -> Generator[str, None, None]:
    con = sqlite3.connect(database_path)
    cur = con.cursor()
    cur.execute(f"SELECT {data_column_name} FROM {table_name}")
    
    while True:
        response = cur.fetchone()
        if response is None:
            break
        
        yield response[0]


def decompress_subtitle_zip(bytes):
    with zipfile.ZipFile(BytesIO(bytes), 'r') as zip_file:
        file_list = zip_file.namelist()
        srt_files = list(filter(
            lambda file_name: (
                file_name.endswith(".srt") or 
                file_name.endswith(".ass")
            ), 
            file_list
        ))
        # assert len(srt_files) == 1, f"Could not find SRT or ASS file in the archive: {file_list}"
        if len(srt_files) > 1:
            print(f"Found multiple SRT or ASS files in the archive: {file_list}. Taking the first one: {srt_files[0]}")
        if len(srt_files) == 0:
            print(f"Could not find SRT or ASS file in the archive: {file_list}")
            return None

        for file_name in srt_files:
            with zip_file.open(file_name) as file:
                content = file.read()
                chardet_result = chardet.detect(content)
                
                if "encoding" in chardet_result:
                    text = content.decode(chardet_result["encoding"])  # type: ignore
                else:
                    # fallback to utf-8
                    text = content.decode("utf-8")

                return text


def format_subtitle_data_into_text(subtitle_data):
    numbers = set("0123456789")

    parts = []
    for line in subtitle_data.split("\n"):
        if len(set(line.strip()) - numbers) == 0:
            continue
        if "-->" in line:
            continue
        parts.append(line.strip())

    string = " ".join(parts)
    # string = string.replace("</i> <i>", " ")
    string = string.replace("</i>", " ").replace("<i>", " ")
    return string


def get_subtitle_text(compressed_text):
    try:
        text = decompress_subtitle_zip(compressed_text)
    except Exception as e:
        print(f"Error decompressing subtitle: {e}")
        text = None

    if text is not None:
        subtitle_text = format_subtitle_data_into_text(text)
        return subtitle_text
    else:
        return None



def get_total_num_entries(database_path, table_name="zipfiles"):
    con = sqlite3.connect(database_path)
    cur = con.cursor()
    cur.execute(f"SELECT COUNT(*) FROM {table_name}")

    return cur.fetchone()[0]


def main(args):
    num_entries = get_total_num_entries(args.dump_path, table_name="zipfiles")

    with Pool() as pool:
        for text in tqdm(pool.imap(get_subtitle_text, stream_subtitle_data_from_database(args.dump_path)), total=num_entries):
            if text is not None:
                print(text)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("dump_path", type=Path)
    args = parser.parse_args()

    main(args)
