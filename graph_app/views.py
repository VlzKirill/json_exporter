import os
import json
from django.shortcuts import render
from django.views import View
from matplotlib import pyplot as plt
from .models import BenchmarkData

class GraphView(View):
    template_name = 'graph_app/graph.html'

    def get(self, request, *args, **kwargs):
        data_dir = '/путь/к/вашей/директории'  # Замените на актуальный путь
        all_files = os.listdir(data_dir)
        all_data = []

        for file_name in all_files:
            if file_name.endswith('.json'):
                with open(os.path.join(data_dir, file_name)) as json_file:
                    data = json.load(json_file)

                version_value = int(data['version']['values'][0])
                benchmarks = data['benchmarks']

                for benchmark in benchmarks:
                    benchmark_name = benchmark['name']
                    real_time = benchmark['real_time']

                    BenchmarkData.objects.create(
                        version_value=version_value,
                        benchmark_name=benchmark_name,
                        real_time=real_time
                    )

                    all_data.append({'benchmark_name': benchmark_name, 'version_value': version_value, 'real_time': real_time})

        # Рисование графика
        unique_names = set(d['benchmark_name'] for d in all_data)
        colors = plt.cm.viridis(range(len(unique_names)))

        for i, name in enumerate(unique_names):
            subset_data = [d for d in all_data if d['benchmark_name'] == name]
            x = [d['benchmark_name'] for d in subset_data]
            y = [d['version_value'] for d in subset_data]
            plt.scatter(x, y, label=name, color=colors[i])

        plt.xlabel('Benchmark Name')
        plt.ylabel('Version Value')
        plt.legend()
        plt.savefig('graph_app/static/graph.png')  # Сохранение графика в статическую директорию
        plt.close()

        return render(request, self.template_name, {})
