"""
music_analyzer.py - Анализатор статистики прослушиваний музыки
"""

import json
from collections import Counter
import matplotlib.pyplot as plt


class MusicAnalyzer:
    """Класс для анализа музыкальной статистики"""
    
    def __init__(self, filepath="music.json"):
        """
        Загружает данные из JSON-файла
        """
        self.tracks = []
        self.load_data(filepath)
    
    def load_data(self, filepath):
        """Загружает данные из JSON-файла"""
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                self.tracks = json.load(file)
            print(f"✅ Загружено {len(self.tracks)} треков")
        except FileNotFoundError:
            print(f"❌ Файл {filepath} не найден")
            self.tracks = []
        except json.JSONDecodeError:
            print(f"❌ Ошибка в формате JSON файла {filepath}")
            self.tracks = []
    
    def calculate_total_time(self):
        """
        Задание 3.1: Суммарное время прослушивания
        Считаем: duration_minutes * listens для каждого трека
        """
        total_minutes = 0
        for track in self.tracks:
            total_minutes += track['duration_minutes'] * track['listens']
        
        total_hours = total_minutes / 60
        total_days = total_hours / 24
        
        return {
            "minutes": round(total_minutes, 2),
            "hours": round(total_hours, 2),
            "days": round(total_days, 2)
        }
    
    def get_top_genre(self):
        """
        Задание 3.2: Топ-жанр
        Жанр, который встречается чаще всего
        """
        genres = [track['genre'] for track in self.tracks]
        genre_counts = Counter(genres)
        
        # Находим самый популярный жанр
        top_genre = max(genre_counts.items(), key=lambda x: x[1])
        
        return {
            "genre": top_genre[0],
            "count": top_genre[1],
            "all_genres": dict(genre_counts)
        }
    
    def get_most_listened_track(self):
        """
        Задание 3.3: Самый прослушиваемый трек
        Трек с наибольшим количеством прослушиваний
        """
        if not self.tracks:
            return None
        
        # Находим трек с максимальным listens
        most_listened = max(self.tracks, key=lambda x: x['listens'])
        
        return {
            "track_name": most_listened['track_name'],
            "artist": most_listened['artist'],
            "listens": most_listened['listens'],
            "genre": most_listened['genre']
        }
    
    def get_top_artists(self, top_n=5):
        """Топ N исполнителей по прослушиваниям"""
        artist_listens = {}
        for track in self.tracks:
            artist = track['artist']
            if artist in artist_listens:
                artist_listens[artist] += track['listens']
            else:
                artist_listens[artist] = track['listens']
        
        # Сортируем и берём top_n
        sorted_artists = sorted(artist_listens.items(), key=lambda x: x[1], reverse=True)
        return sorted_artists[:top_n]
    
    def generate_report(self):
        """
        Генерирует полный отчёт
        """
        print("\n" + "=" * 50)
        print("📊 ОТЧЁТ ПО СТАТИСТИКЕ ПРОСЛУШИВАНИЙ")
        print("=" * 50)
        
        # 1. Общая информация
        print(f"\n📁 Всего треков: {len(self.tracks)}")
        
        # 2. Суммарное время
        total_time = self.calculate_total_time()
        print(f"\n⏱️ СУММАРНОЕ ВРЕМЯ ПРОСЛУШИВАНИЯ:")
        print(f"   {total_time['minutes']} минут")
        print(f"   {total_time['hours']} часов")
        print(f"   {total_time['days']} дней")
        
        # 3. Топ-жанр
        top_genre = self.get_top_genre()
        print(f"\n🎵 ТОП-ЖАНР:")
        print(f"   {top_genre['genre']} — {top_genre['count']} треков")
        print(f"\n   Все жанры:")
        for genre, count in top_genre['all_genres'].items():
            print(f"      {genre}: {count} треков")
        
        # 4. Самый прослушиваемый трек
        top_track = self.get_most_listened_track()
        if top_track:
            print(f"\n🏆 САМЫЙ ПРОСЛУШИВАЕМЫЙ ТРЕК:")
            print(f"   {top_track['track_name']} — {top_track['artist']}")
            print(f"   Прослушиваний: {top_track['listens']}")
            print(f"   Жанр: {top_track['genre']}")
        
        # 5. Топ-исполнители
        print(f"\n👨‍🎤 ТОП-ИСПОЛНИТЕЛИ:")
        top_artists = self.get_top_artists(5)
        for i, (artist, listens) in enumerate(top_artists, 1):
            print(f"   {i}. {artist} — {listens} прослушиваний")
        
        print("\n" + "=" * 50)
    
    def visualize(self):
        """
        Задание 4: Визуализация статистики
        """
        if not self.tracks:
            print("❌ Нет данных для визуализации")
            return
        
        # Создаём фигуру с 3 графиками
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('📊 Анализ прослушиваний музыки', fontsize=16, fontweight='bold')
        
        # График 1: Топ-исполнители
        ax1 = axes[0, 0]
        top_artists = self.get_top_artists(7)
        artists = [artist for artist, _ in top_artists]
        listens = [count for _, count in top_artists]
        
        colors = plt.cm.viridis(range(len(artists)))
        ax1.bar(artists, listens, color=colors)
        ax1.set_title('Топ-исполнители по прослушиваниям', fontsize=12)
        ax1.set_xlabel('Исполнитель')
        ax1.set_ylabel('Количество прослушиваний')
        ax1.tick_params(axis='x', rotation=45, labelsize=9)
        
        # Добавляем значения на столбцы
        for i, v in enumerate(listens):
            ax1.text(i, v + 2, str(v), ha='center', fontsize=9)
        
        # График 2: Распределение по жанрам (круговая диаграмма)
        ax2 = axes[0, 1]
        genre_counts = Counter([track['genre'] for track in self.tracks])
        genres = list(genre_counts.keys())
        counts = list(genre_counts.values())
        
        colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#ff99cc', '#99ccff']
        ax2.pie(counts, labels=genres, autopct='%1.1f%%', colors=colors[:len(genres)])
        ax2.set_title('Распределение по жанрам', fontsize=12)
        
        # График 3: Самые прослушиваемые треки
        ax3 = axes[1, 0]
        sorted_tracks = sorted(self.tracks, key=lambda x: x['listens'], reverse=True)[:8]
        track_names = [f"{t['track_name']}\n({t['artist']})" for t in sorted_tracks]
        track_listens = [t['listens'] for t in sorted_tracks]
        
        colors = plt.cm.plasma(range(len(track_names)))
        bars = ax3.barh(track_names, track_listens, color=colors)
        ax3.set_title('Топ-8 самых прослушиваемых треков', fontsize=12)
        ax3.set_xlabel('Количество прослушиваний')
        ax3.tick_params(axis='y', labelsize=8)
        
        # Добавляем значения
        for bar, v in zip(bars, track_listens):
            ax3.text(v + 2, bar.get_y() + bar.get_height()/2, 
                    str(v), va='center', fontsize=8)
        
        # График 4: Суммарное время по жанрам
        ax4 = axes[1, 1]
        genre_time = {}
        for track in self.tracks:
            genre = track['genre']
            time = track['duration_minutes'] * track['listens']
            if genre in genre_time:
                genre_time[genre] += time
            else:
                genre_time[genre] = time
        
        genres = list(genre_time.keys())
        times = [t / 60 for t in genre_time.values()]  # Переводим в часы
        
        colors = plt.cm.coolwarm(range(len(genres)))
        ax4.bar(genres, times, color=colors)
        ax4.set_title('Время прослушивания по жанрам (часы)', fontsize=12)
        ax4.set_xlabel('Жанр')
        ax4.set_ylabel('Часы')
        ax4.tick_params(axis='x', rotation=45, labelsize=9)
        
        # Добавляем значения
        for i, v in enumerate(times):
            ax4.text(i, v + 0.5, f'{v:.1f}ч', ha='center', fontsize=8)
        
        plt.tight_layout()
        plt.show()
    
    def export_stats(self, filename="stats_report.txt"):
        """Экспортирует статистику в текстовый файл"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("ОТЧЁТ ПО СТАТИСТИКЕ ПРОСЛУШИВАНИЙ\n")
            f.write("=" * 50 + "\n\n")
            
            total_time = self.calculate_total_time()
            f.write(f"Всего треков: {len(self.tracks)}\n")
            f.write(f"Общее время: {total_time['hours']} часов\n\n")
            
            top_genre = self.get_top_genre()
            f.write(f"Топ-жанр: {top_genre['genre']} ({top_genre['count']} треков)\n")
            
            top_track = self.get_most_listened_track()
            if top_track:
                f.write(f"Самый прослушиваемый трек: {top_track['track_name']} - {top_track['artist']} ({top_track['listens']} прослушиваний)\n")
            
            f.write("\nТоп-исполнители:\n")
            for i, (artist, listens) in enumerate(self.get_top_artists(5), 1):
                f.write(f"  {i}. {artist} - {listens} прослушиваний\n")
        
        print(f"✅ Отчёт сохранён в {filename}")


def main():
    """Главная функция"""
    print("🎵 АНАЛИЗАТОР СТАТИСТИКИ ПРОСЛУШИВАНИЙ")
    print("-" * 40)
    
    # Создаём анализатор
    analyzer = MusicAnalyzer("music.json")
    
    if not analyzer.tracks:
        print("❌ Нет данных для анализа")
        return
    
    # Генерируем отчёт
    analyzer.generate_report()
    
    # Экспортируем в файл
    analyzer.export_stats()
    
    # Визуализация
    print("\n📊 Открываю графики...")
    analyzer.visualize()


if __name__ == "__main__":
    main()