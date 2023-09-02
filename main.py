import pandas as pd
import matplotlib.pyplot as plt
import os
import requests
import json


class GraphBuilder:
    def __init__(self):
        self.plots_folder = 'plots'

    def _create_folder(self):
        if not os.path.exists(self.plots_folder):
            os.makedirs(self.plots_folder)

    def draw_plots(self, json_file):
        self._create_folder()

        # Чтение json-файла в качестве кадра данных pandas
        r = requests.get(json_file)
        if r.status_code == 200:
            data = json.loads(r.content)
        else:
            print("Ошибка при получении JSON-файла")

        df = pd.DataFrame(data)

        # Построение графиков для сравнения различных столбцов
        plots_path = []
        for column in df.columns:
            plt.figure()
            plt.plot(df[column])
            plt.xlabel('Index')
            plt.ylabel(column)
            plot_path = os.path.join(self.plots_folder, f"{column}.png")
            plt.savefig(plot_path)
            plt.close()
            plots_path.append(plot_path)

        return plots_path


url = 'https://ai-process-sandy.s3.eu-west-1.amazonaws.com/purge/deviation.json'

# Пример использования
graph_builder = GraphBuilder()
plot_paths = graph_builder.draw_plots(url)
print(plot_paths)
