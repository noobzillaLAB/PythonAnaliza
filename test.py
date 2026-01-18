import pandas
import sys
import matplotlib.pyplot
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk

file_path = "data/US_Accidents_March23.csv"
print("Wczytywanie danych... Ze wzgledu na duza liczbe rekordow trwa ono dluzej niz zwykle.")

chunksize = 500_000
chunks = []

total_rows = 7_728_394

for i, chunk in enumerate(pandas.read_csv(file_path, chunksize=chunksize)):
    chunks.append(chunk)
    progress = min((i+1) * chunksize / total_rows * 100, 100)
    sys.stdout.write(f"\rProgress: {progress:.1f}%")
    sys.stdout.flush()

df = pandas.concat(chunks, ignore_index=True)
print("\nDane gotowe.")

df['Start_Time'] = pandas.to_datetime(df['Start_Time'], errors='coerce')
df = df.dropna(subset=['Start_Time'])

df["Is_Weekend"] = df["Start_Time"].dt.dayofweek >= 5

def plot_accidents_by_year(ax):
    ax.clear()
    df['Year'] = df['Start_Time'].dt.year
    counts = df['Year'].value_counts().sort_index()
    counts.plot(kind='bar', ax=ax)
    ax.set_title("Liczba wypadków w latach")
    ax.set_xlabel("Rok")
    ax.set_ylabel("Liczba wypadków")
    for bar, value in zip(ax.patches, counts):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height(),
                f"{value:,}", ha='center', va='bottom', fontsize=9)

def plot_accidents_by_year_procent(ax):
    ax.clear()
    counts = df['Start_Time'].dt.year.value_counts().sort_index()
    total = counts.sum()
    percentages = (counts / total) * 100
    percentages.plot(kind='bar', ax=ax)
    ax.set_title("Liczba wypadków w latach wg %")
    ax.set_xlabel("Rok")
    ax.set_ylabel("Udział wypadków (%)")
    for bar, pct in zip(ax.patches, percentages):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height(),
                f"{pct:.2f}%", ha='center', va='bottom', fontsize=9)

def plot_accidents_by_state(ax):
    ax.clear()
    counts = df['State'].value_counts().head(20)
    counts.plot(kind='bar', ax=ax)
    ax.set_title("Top 20 stanów wg liczby wypadków")
    ax.set_xlabel("Stan")
    ax.set_ylabel("Liczba wypadków")
    for bar, value in zip(ax.patches, counts):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height(),
                f"{value:,}", ha='center', va='bottom', fontsize=9)

def plot_accidents_by_state_procent(ax):
    ax.clear()
    counts = df['State'].value_counts()
    top_counts = counts.head(20).copy()
    top_counts['Inne'] = counts.iloc[20:].sum()
    percentages = (top_counts / top_counts.sum()) * 100
    percentages.plot(kind='bar', ax=ax)
    ax.set_title("Top 20 stanów wg procentu wypadków")
    ax.set_xlabel("Stan")
    ax.set_ylabel("Udział wypadków (%)")
    for bar, pct in zip(ax.patches, percentages):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height(),
                f"{pct:.2f}%", ha='center', va='bottom', fontsize=9)

def plot_accidents_by_city(ax):
    ax.clear()
    counts = df['City'].value_counts().head(20)
    counts.plot(kind='bar', ax=ax)
    ax.set_title("Top 20 miast wg liczby wypadków")
    ax.set_xlabel("Miasto")
    ax.set_ylabel("Liczba wypadków")
    for bar, value in zip(ax.patches, counts):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height(),
                f"{value:,}", ha='center', va='bottom', fontsize=9)

def plot_accidents_by_city_procent(ax):
    ax.clear()
    counts = df['City'].value_counts()
    top_counts = counts.head(20).copy()
    top_counts['Inne'] = counts.iloc[20:].sum()
    percentages = (top_counts / top_counts.sum()) * 100
    percentages.plot(kind='bar', ax=ax)
    ax.set_title("Top 20 miast wg procentu wypadków")
    ax.set_xlabel("Miasto")
    ax.set_ylabel("Udział wypadków (%)")
    for bar, pct in zip(ax.patches, percentages):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height(),
                f"{pct:.2f}%", ha='center', va='bottom', fontsize=9)

def plot_accidents_by_hour(ax):
    ax.clear()
    counts = df['Start_Time'].dt.hour.value_counts().sort_index()
    counts.plot(kind='bar', ax=ax)
    ax.set_title("Wypadki wg godziny dnia")
    ax.set_xlabel("Godzina")
    ax.set_ylabel("Liczba wypadków")
    for bar, value in zip(ax.patches, counts):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height(),
                f"{value:,}", ha='center', va='bottom', fontsize=9)

def plot_accidents_by_severity(ax):
    ax.clear()
    counts = df['Severity'].value_counts().sort_index()
    counts.plot(kind='bar', ax=ax)
    ax.set_title("Rozkład powagi wypadków")
    ax.set_xlabel("Skala wypadku (1–4)")
    ax.set_ylabel("Liczba wypadków")
    for bar, value in zip(ax.patches, counts):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height(),
                f"{value:,}", ha='center', va='bottom', fontsize=9)

def plot_accidents_by_weekday(ax):
    ax.clear()
    weekdays = ['Poniedziałek','Wtorek','Środa','Czwartek','Piątek','Sobota','Niedziela']
    df['Weekday'] = df['Start_Time'].dt.dayofweek
    counts = df['Weekday'].value_counts().sort_index()
    counts.index = [weekdays[i] for i in counts.index]
    counts.plot(kind='bar', ax=ax)
    ax.set_title("Wypadki wg dnia tygodnia")
    ax.set_xlabel("Dzień tygodnia")
    ax.set_ylabel("Liczba wypadków")
    for bar, value in zip(ax.patches, counts):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height(),
                f"{value:,}", ha='center', va='bottom', fontsize=9)

def plot_accidents_by_weather(ax):
    ax.clear()
    counts = df['Weather_Condition'].fillna("Unknown").value_counts().head(20)
    counts.plot(kind='bar', ax=ax)
    ax.set_title("Top 20 warunków pogodowych przy wypadkach")
    ax.set_xlabel("Pogoda")
    ax.set_ylabel("Liczba wypadków")
    for bar, value in zip(ax.patches, counts):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height(),
                f"{value:,}", ha='center', va='bottom', fontsize=9)

def plot_accidents_by_road_feature(ax):
    ax.clear()
    cols = ["Crossing","Junction","Traffic_Signal","Station","Stop"]
    counts = df[cols].sum().sort_values(ascending=False)
    counts.plot(kind='bar', ax=ax)
    ax.set_title("Liczba wypadków wg drogi")
    ax.set_xlabel("Cecha drogi")
    ax.set_ylabel("Liczba wypadków")
    for bar, value in zip(ax.patches, counts):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height(),
                f"{value:,}", ha='center', va='bottom', fontsize=9)

def plot_severity_weekend(ax):
    ax.clear()
    means = df.groupby("Is_Weekend")["Severity"].mean()
    means.index = ["Dni robocze", "Weekend"]
    means.plot(kind="bar", ax=ax)
    ax.set_title("Średnia ciężkość wypadków wg dnia tygodnia")
    ax.set_ylabel("Średnia Severity")
    for bar, value in zip(ax.patches, means):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height(),
                f"{value:.2f}", ha="center", va="bottom")

def plot_severity_by_weather(ax):
    ax.clear()
    weather_sev = (
        df.groupby("Weather_Condition")["Severity"]
        .mean()
        .sort_values(ascending=False)
        .head(15)
    )
    weather_sev.plot(kind="bar", ax=ax)
    ax.set_title("Średnia ciężkość wypadków wg pogody")
    ax.set_ylabel("Średnia Severity")
    ax.set_xlabel("Pogoda")
    for bar, value in zip(ax.patches, weather_sev):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height(),
                f"{value:.2f}", ha="center", va="bottom", fontsize=9)

plots = [
    plot_accidents_by_year,
    plot_accidents_by_year_procent,
    plot_accidents_by_state,
    plot_accidents_by_state_procent,
    plot_accidents_by_city,
    plot_accidents_by_city_procent,
    plot_accidents_by_hour,
    plot_accidents_by_severity,
    plot_accidents_by_weekday,
    plot_accidents_by_weather,
    plot_accidents_by_road_feature,
    plot_severity_weekend,
    plot_severity_by_weather
]

plot_names = [
    "Liczba wypadków w latach",
    "Liczba wypadków w latach wg %",
    "Top 20 stanów",
    "Top 20 stanów wg %",
    "Top 20 miast",
    "Top 20 miast wg %",
    "Wypadki wg godziny",
    "Rozkład powagi wypadków",
    "Wypadki wg dnia tygodnia",
    "Top 20 warunków pogodowych",
    "Wypadki wg drogi",
    "Severity: weekend vs dni robocze",
    "Severity vs pogoda"
]

root = tk.Tk()
root.title("Analiza US Accidents")

fig, ax = matplotlib.pyplot.subplots(figsize=(8, 5))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

current_plot = 0
plots[current_plot](ax)
canvas.draw()

def show_plot(i):
    global current_plot
    current_plot = i
    plots[current_plot](ax)
    canvas.draw()

btn_frame = tk.Frame(root)
btn_frame.pack(side=tk.BOTTOM, fill=tk.X)

for i, name in enumerate(plot_names):
    tk.Button(
        btn_frame,
        text=name,
        command=lambda i=i: show_plot(i)
    ).pack(side=tk.LEFT, padx=5, pady=5)

root.mainloop()
