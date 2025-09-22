import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("pet_wine_921_m12.csv", dtype=str, low_memory=False)

df.columns = ["Time", "Operation", "Value"]

df["Time"] = pd.to_numeric(df["Time"], errors="coerce")
df["Value"] = pd.to_numeric(df["Value"], errors="coerce")
df["Operation"] = df["Operation"].astype(str).str.strip()

# 限縮時間範圍，濾掉一些奇怪的值 這裡你可以看你時間的範圍看要怎麼改
df = df[df["Time"] < 600].reset_index(drop=True)

A, B = 0, 0  #兩條線的記憶體累積值
time_list, A_list, B_list = [], [], []

for _, row in df.iterrows():
    op, val = row["Operation"], row["Value"]

    if pd.isna(val):
        continue

    # (A)
    if op == "Alloca":
        A += val
    elif op == "Realloc+":
        A += val
    elif op == "free":
        A -= val

    # (B)
    elif op == "AllocDynarecMap":
        B += val
    elif op == "FreeDynarecMap":
        B -= val

    # 紀錄
    time_list.append(row["Time"])
    A_list.append(A)
    B_list.append(B)

print("A 累積最大值:", max(A_list), "Byte")
print("B 累積最大值:", max(B_list), "Byte")

# 畫圖
plt.figure(figsize=(14, 7))
plt.plot(time_list, A_list, label="General (Alloca/Realloc+/free)", color="blue", linewidth=1)
plt.plot(time_list, B_list, label="Dynarec (AllocaDynarecMap/FreeDynarecMap)", color="red", linewidth=1)

plt.xlabel("Time (seconds)")
plt.ylabel("Cumulative Memory")
plt.title("Memory Allocation Over Time (pet_wine_921_m12.csv)") # 你要改標題就直接把檔名替換掉就可以了
plt.legend()
plt.grid(True, which="both", linestyle="--", linewidth=0.5)
plt.minorticks_on()  
plt.tight_layout()
plt.show()
