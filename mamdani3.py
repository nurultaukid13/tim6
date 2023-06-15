import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt

# Variable
suhu = np.arange(20, 41, 1)
kelembapan = np.arange(0, 101, 1)
kecepatan = np.arange(0, 186, 1)

# Range himpunan fuzzy dari grafik
suhu_dingin = fuzz.trapmf(suhu, [20, 20, 25, 30])
suhu_hangat = fuzz.trimf(suhu, [25, 30, 35])
suhu_panas = fuzz.trapmf(suhu, [30, 35, 40, 40])

kelembapan_kering = fuzz.trapmf(kelembapan, [0, 0, 25, 50])
kelembapan_normal = fuzz.trimf(kelembapan, [25, 50, 75])
kelembapan_basah = fuzz.trapmf(kelembapan, [50, 75, 100, 100])

kecepatan_lambat = fuzz.trapmf(kecepatan, [0, 0, 40, 60])
kecepatan_normal = fuzz.trapmf(kecepatan, [50, 70, 90, 110])
kecepatan_cepat = fuzz.trapmf(kecepatan, [100, 120, 150, 150])
# Menentukan Input
input_suhu = float(input("Masukkan suhu (20-40): "))
input_kelembapan = float(input("Masukkan kelembapan (50-100): "))

# Menentukan Derajat Keanggotaan (fuzzifikasi)
x = []
x.append(fuzz.interp_membership(suhu, suhu_dingin, input_suhu))
x.append(fuzz.interp_membership(suhu, suhu_hangat, input_suhu))
x.append(fuzz.interp_membership(suhu, suhu_panas, input_suhu))

y = []
y.append(fuzz.interp_membership(kelembapan, kelembapan_kering, input_kelembapan))
y.append(fuzz.interp_membership(kelembapan, kelembapan_normal, input_kelembapan))
y.append(fuzz.interp_membership(kelembapan, kelembapan_basah, input_kelembapan))

print("==========================")
print("Derajat Keanggotaan suhu")
if x[0] > 0:
    print("Dingin: " + str(round(x[0], 3)))
if x[1] > 0:
    print("Hangat: " + str(round(x[1], 3)))
if x[2] > 0:
    print("Panas: " + str(round(x[2], 3)))

print("Derajat Keanggotaan kelembapan")
if y[0] > 0:
    print("Kering: " + str(round(y[0], 3)))
if y[1] > 0:
    print("Normal: " + str(round(y[1], 3)))
if y[2] > 0:
    print("Basah: " + str(round(y[2], 3)))


# Memodelkan Rule Base dan Inferensi Mamdani

# Rule 1: IF suhu dingin AND kelembapan kering THEN kecepatan lambat
rule1 = np.fmin(x[0], y[0])
output_lambat = np.fmin(rule1, kecepatan_lambat)

# Rule 2: IF suhu dingin AND kelembapan normal THEN kecepatan sedang
rule2 = np.fmin(x[0], y[1])
output_sedang = np.fmin(rule2, kecepatan_sedang)

# Rule 3: IF suhu dingin AND kelembapan basah THEN kecepatan sedang
rule3 = np.fmin(x[1], y[2])
output_sedang = np.fmin(rule3, kecepatan_sedang)

# Rule 4: IF suhu hangat AND kelembapan kering THEN kecepatan sedang
rule4 = np.fmin(x[1], y[0])
output_sedang = np.fmin(rule4, kecepatan_sedang)

# Rule 5: IF suhu hangat AND kelembapan normal THEN kecepatan sedang
rule5 = np.fmin(x[1], y[1])
output_sedang = np.fmin(rule5, kecepatan_sedang)

# Rule 6: IF suhu hangat AND kelembapan basah THEN kecepatan cepat
rule6 = np.fmin(x[1], y[2])
output_cepat = np.fmin(rule6, kecepatan_cepat)

# Rule 7: IF suhu panas AND kelembapan kering THEN kecepatan cepat
rule7 = np.fmin(x[2], y[0])
output_cepat = np.fmin(rule7, kecepatan_cepat)

# Rule 8: IF suhu panas AND kelembapan normal THEN kecepatan cepat
rule8 = np.fmin(x[2], y[1])
output_cepat = np.fmin(rule8, kecepatan_cepat)

# Rule 9: IF suhu panas AND kelembapan normal THEN kecepatan cepat
rule9 = np.fmin(x[2], y[2])
output_cepat = np.fmin(rule9, kecepatan_cepat)

# Menggabungkan aturan-aturan dengan operasi maksimum
output_combined = np.maximum(output_cepat, output_lambat)

# Defuzzifikasi menggunakan metode Mamdani
z = fuzz.defuzz(kecepatan, output_combined, 'centroid')

# Menampilkan hasil output
print("==========================")
print("Output:")
print("Kecepatan Kipas:", round (z, 3))

if z >= 150:
    print("Kondisi: Cepat")
else:
    print("Kondisi: Lambat")

# Mengatur plot dan kurva
plt.figure()

# Menampilkan fungsi keanggotaan suhu
plt.plot(suhu, suhu_dingin, 'r', label='Dingin')
plt.plot(suhu, suhu_panas, 'b', label='Panas')
plt.axvline(x=input_suhu, color='g', linestyle='--', label='Input Suhu')
plt.legend()

# Menampilkan fungsi keanggotaan kelembapan
plt.figure()
plt.plot(kelembapan, kelembapan_kering, 'r', label='Kering')
plt.plot(kelembapan, kelembapan_basah, 'b', label='Basah')
plt.axvline(x=input_kelembapan, color='g', linestyle='--', label='Input Kelembapan')
plt.legend()

# Menampilkan grafik output kecepatan kipas
plt.figure()
plt.plot(kecepatan, kecepatan_lambat, 'r', label='Lambat')
plt.plot(kecepatan, kecepatan_cepat, 'b', label='Cepat')

if(z>=150):
    output_membership = fuzz.interp_membership(kecepatan, kecepatan_cepat, z)
    plt.plot(z, fuzz.interp_membership(kecepatan, kecepatan_cepat, z), 'ko', label='Output')
elif(z<150):
    output_membership = fuzz.interp_membership(kecepatan, kecepatan_lambat, z)
    plt.plot(z, fuzz.interp_membership(kecepatan, kecepatan_lambat, z), 'ko', label='Output')
plt.annotate(f"z = {round(z, 3)}", (z, output_membership), textcoords="offset points", xytext=(0,10), ha='center')
plt.legend()

# Menampilkan grafik
plt.show()