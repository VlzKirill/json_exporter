import os
import json


def parse_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data


def extract_version_name(folder_path):
    return os.path.basename(folder_path)


def extract_last_digit(version_name):
    return int(version_name.split('.')[-1])


def process_folder():
    #base_folder = '/benchmarks'
    base_folder = 'C:\\Users\\Пользователь\\Desktop\\benchmarks'
    version_folders = [f.path for f in os.scandir(base_folder) if f.is_dir()]

    max_version_folder = None
    max_last_digit = float('-inf')

    for version_folder in version_folders:
        version_name = extract_version_name(version_folder)
        last_digit = extract_last_digit(version_name)

        if last_digit > max_last_digit:
            max_last_digit = last_digit
            max_version_folder = version_folder

    benchmarks = {}

    version = extract_version_name(max_version_folder)
    build_number = extract_last_digit(version)

    files = os.listdir(max_version_folder)

    for file_name in files:
        file_path = os.path.join(max_version_folder, file_name)
        if os.path.isfile(file_path):
            data = parse_json_file(file_path)
            json_benchmarks = data.get('benchmarks', [])

            for benchmark_data in json_benchmarks:
                benchmark_name = benchmark_data.get('name', '')
                bytes_per_second = benchmark_data.get('bytes_per_second', 0.0)

                benchmark_name = benchmark_name.lower().replace(' ', '_').replace("-", "_")
                if benchmark_name.endswith('/real_time_mean'):
                    benchmark_name = benchmark_name.replace('/real_time_mean', '').strip()
                    benchmarks[benchmark_name] = bytes_per_second

    return [benchmarks, version, build_number]