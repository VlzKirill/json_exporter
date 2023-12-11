from django.http import HttpResponse
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
                cpu_time = benchmark_data.get('bytes_per_second', 0.0)

                # Преобразуйте benchmark_name в нижний регистр и замените пробелы на нижние подчеркивания
                benchmark_name = benchmark_name.lower().replace(' ', '_')

                # Оставьте только те benchmark_name, у которых есть /real_time_median на конце
                if benchmark_name.endswith('/real_time_mean'):
                    benchmark_name = benchmark_name.replace('/real_time_mean', '').strip()
                    Benchmark.objects.create(version=version, name=benchmark_name, cpu_time=cpu_time)

def index(request):
    base_folder = '/benchmarks'

    # Получите все поддиректории
    version_folders = [f.path for f in os.scandir(base_folder) if f.is_dir()]

    # Инициализируйте переменные для хранения информации о самой последней версии
    max_version_name = None
    max_last_digit = float('-inf')

    # Найдите версию с самым большим last_digit
    for version_folder in version_folders:
        version_name = extract_version_name(version_folder)
        last_digit = extract_last_digit(version_name)

        if last_digit > max_last_digit:
            max_last_digit = last_digit
            max_version_name = version_folder

    # Очистите базу данных перед обработкой новой версии
    Benchmark.objects.all().delete()

    # Обработайте только выбранную версию
    process_folder(max_version_name)

    benchmarks = Benchmark.objects.all()

    #context = {'benchmarks': benchmarks}
    #return render(request, 'index.html', context)
    response_content = ''
    for benchmark in benchmarks:
        response_content += f'{benchmark.name}{{version="{benchmark.version.name}"}} {benchmark.cpu_time}\n'

    return HttpResponse(response_content, content_type='text/plain')