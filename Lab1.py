import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

#1

np.random.seed(42)

latency = np.random.normal(loc=50, scale=5, size=200)

stats_table = {
    "Объем выборки": len(latency),
    "Минимум": np.min(latency),
    "Максимум": np.max(latency),
    "Среднее": np.mean(latency),
    "Медиана": np.median(latency),
    "Дисперсия": np.var(latency, ddof=1),
    "СКО": np.std(latency, ddof=1)
}
print(pd.DataFrame(stats_table.items(),
                   columns=["Характеристика", "Значение"]))

plt.figure(figsize=(10, 5))
plt.plot(latency, marker='o', markersize=3)
plt.title("Последовательность измерений задержки")
plt.xlabel("Номер измерения")
plt.ylabel("Задержка, мс")
plt.grid(True)
plt.tight_layout()
plt.show()

plt.figure(figsize=(8, 5))
plt.hist(latency, bins=15, edgecolor='black')
plt.title("Гистограмма распределения задержки")
plt.xlabel("Задержка, мс")
plt.ylabel("Частота")
plt.grid(True)
plt.tight_layout()
plt.show()

#2 

sample_sizes = [20, 50, 100, 150, 200]

results = []

for n in sample_sizes:
    sample = latency[:n]

    mean = np.mean(sample)
    std = np.std(sample, ddof=1)

    confidence = 0.95

    t_value = stats.t.ppf(
        (1 + confidence) / 2,
        df=n - 1
    )

    margin = t_value * std / np.sqrt(n)

    ci_low = mean - margin
    ci_high = mean + margin

    width = ci_high - ci_low

    results.append([
        n,
        mean,
        std,
        ci_low,
        ci_high,
        width
    ])

df_ci = pd.DataFrame(
    results,
    columns=[
        "N",
        "Среднее",
        "СКО",
        "Нижняя граница",
        "Верхняя граница",
        "Ширина интервала"
    ]
)

print(df_ci)

plt.figure(figsize=(8, 5))
plt.plot(
    df_ci["N"],
    df_ci["Ширина интервала"],
    marker='o'
)
plt.title("Ширина доверительного интервала")
plt.xlabel("Количество измерений")
plt.ylabel("Ширина интервала")
plt.grid(True)
plt.tight_layout()
plt.show()

#3

latency_with_outliers = np.concatenate([
    latency,
    [10, 12, 110, 120, 150]
])

mean_before = np.mean(latency_with_outliers)
median_before = np.median(latency_with_outliers)
std_before = np.std(latency_with_outliers, ddof=1)

#iqr


Q1 = np.percentile(latency_with_outliers, 25)
Q3 = np.percentile(latency_with_outliers, 75)

IQR = Q3 - Q1

lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

clean_data = latency_with_outliers[
    (latency_with_outliers >= lower_bound) &
    (latency_with_outliers <= upper_bound)
]

mean_after = np.mean(clean_data)
median_after = np.median(clean_data)
std_after = np.std(clean_data, ddof=1)

comparison = pd.DataFrame({
    "Показатель": [
        "Среднее",
        "Медиана",
        "СКО"
    ],
    "До удаления": [
        mean_before,
        median_before,
        std_before
    ],
    "После удаления": [
        mean_after,
        median_after,
        std_after
    ]
})

print(comparison)

print("\nОбнаружено выбросов:",
      len(latency_with_outliers) - len(clean_data))

plt.figure(figsize=(10, 5))
plt.boxplot(latency_with_outliers)
plt.title("Выборка с выбросами")
plt.grid(True)
plt.show()

plt.figure(figsize=(10, 5))
plt.boxplot(clean_data)
plt.title("Выборка после удаления выбросов")
plt.grid(True)
plt.show()