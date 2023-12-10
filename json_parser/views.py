from django.shortcuts import render

# Create your views here.
import os
import json
from .models import Version, Benchmark


def parse_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def extract_version_name(folder_path):
    return os.path.basename(folder_path)

def extract_last_digit(version_name):
    return int(version_name.split('.')[-1])

def process_folder(folder_path):
    version_name = extract_version_name(folder_path)
    last_digit = extract_last_digit(version_name)

    version, created = Version.objects.get_or_create(name=version_name, last_digit=last_digit)

    files = os.listdir(folder_path)
    for file_name in files:
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            data = parse_json_file(file_path)
            benchmarks = data.get('benchmarks', [])

            for benchmark_data in benchmarks:
                benchmark_name = benchmark_data.get('name', '')
                cpu_time = benchmark_data.get('cpu_time', 0.0)

                Benchmark.objects.create(version=version, name=benchmark_name, cpu_time=cpu_time)

def index(request):
    versions_folder = '/path/to/your/versions/folder/'
    folders = [f.path for f in os.scandir(versions_folder) if f.is_dir()]

    for folder in folders:
        process_folder(folder)

    benchmarks = Benchmark.objects.all()

    context = {'benchmarks': benchmarks}
    return render(request, 'index.html', context)