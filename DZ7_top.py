import pandas as pd
import matplotlib.pyplot as plt
import os

# === 1. Загрузка данных ===
man_path = "C:/Users/n8122/Downloads/Number_of_names_man.csv"
woman_path = "C:/Users/n8122/Downloads/Number_of_names_woman.csv"

df_man = pd.read_csv(man_path, sep=None, engine="python", encoding="utf-8")
df_woman = pd.read_csv(woman_path, sep=None, engine="python", encoding="utf-8")

df_man.columns = [c.strip().lower() for c in df_man.columns]
df_woman.columns = [c.strip().lower() for c in df_woman.columns]

for df, label in [(df_man, "man"), (df_woman, "woman")]:
    possible_cols = [c for c in df.columns if "number" in c or "кол" in c or "person" in c]
    print(f"{label} — возможные числовые колонки:", possible_cols)


count_col = "numberofpersons" if "numberofpersons" in df_man.columns else possible_cols[0]


for df in (df_man, df_woman):
    df["year"] = pd.to_numeric(df["year"], errors="coerce")
    if "month" in df.columns:
        df["month"] = pd.to_numeric(df["month"], errors="coerce")


    df[count_col] = (
        df[count_col]
        .astype(str)
        .str.replace(",", "")
        .str.replace(" ", "")
        .str.replace("Количествочеловек", "", case=False)
    )


    df = df[df[count_col].str.match(r"^[0-9]+$")]
    df[count_col] = df[count_col].astype(float)


dfm = df_man[df_man["year"].between(2015, 2025)].copy()
dfw = df_woman[df_woman["year"].between(2015, 2025)].copy()

dfm["name"] = dfm["name"].astype(str).str.strip().str.lower()
dfw["name"] = dfw["name"].astype(str).str.strip().str.lower()


# === 2. Аггрегация данных ===

agg_man = dfm.groupby('name')['numberofpersons'].sum().reset_index().sort_values('numberofpersons', ascending=False)
agg_woman = dfw.groupby('name')['numberofpersons'].sum().reset_index().sort_values('numberofpersons', ascending=False)
agg_combined = (
    pd.concat([dfm[['name', 'numberofpersons']], dfw[['name', 'numberofpersons']]])
    .groupby('name')['numberofpersons'].sum()
    .reset_index()
    .sort_values('numberofpersons', ascending=False)
)

# === 3. Визуализация ===
out_dir = "name_plots"
os.makedirs(out_dir, exist_ok=True)

# 1. Топ-100 имён за весь период
top100 = agg_combined.head(100)
plt.figure(figsize=(12, 14))
plt.barh(top100['name'][::-1], top100['numberofpersons'][::-1])
plt.title('Топ 100 имён (2015–2025) — все вместе')
plt.xlabel('Количество новорожденных')
plt.tight_layout()
plt.savefig(f"{out_dir}/top100_combined.png")
plt.close()

# 2. Топ-10 мужских имён
top10_man = agg_man.head(10)
plt.figure(figsize=(8, 6))
plt.barh(top10_man['name'][::-1], top10_man['numberofpersons'][::-1])
plt.title('Топ 10 мужских имён (2015–2025)')
plt.xlabel('Количество новорожденных')
plt.tight_layout()
plt.savefig(f"{out_dir}/top10_man.png")
plt.close()

# 3. Топ-10 женских имён
top10_woman = agg_woman.head(10)
plt.figure(figsize=(8, 6))
plt.barh(top10_woman['name'][::-1], top10_woman['numberofpersons'][::-1])
plt.title('Топ 10 женских имён (2015–2025)')
plt.xlabel('Количество новорожденных')
plt.tight_layout()
plt.savefig(f"{out_dir}/top10_woman.png")
plt.close()


# === 4. Итоги ===
print(" Анализ завершён!")
print("Сохранённые файлы с графиками находятся в папке:", out_dir)
print("Файлы:")
for f in os.listdir(out_dir):
    print(" -", f)

print("\nТоп 10 мужских имён:")
print(top10_man)

print("\nТоп 10 женских имён:")
print(top10_woman)
