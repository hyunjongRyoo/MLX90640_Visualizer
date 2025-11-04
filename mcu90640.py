import serial
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import zoom
import datetime
import keyboard

# === 포트 설정 ===
COM_PORT = 'COM4'
BAUD_RATE = 115200

# === 시리얼 열기 ===
ser = serial.Serial(COM_PORT, BAUD_RATE, timeout=1)

# === 히트맵 초기 설정 ===
plt.ion()
fig, ax = plt.subplots()
frame = np.zeros((24, 32))
img = ax.imshow(frame, cmap='inferno', vmin=20, vmax=60)
cb = plt.colorbar(img)

# ================================================================
# 저장 함수 (HEX + TEMPERATURE + PNG)

# ================================================================
def save_frame(raw, frame, resized_frame):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"frame_{timestamp}.txt"

    # 2바이트씩 묶어서 헥사값 생성
    hex_values = [(raw[i+1] << 8 | raw[i]) for i in range(0, len(raw), 2)]
    temps = [v / 100.0 for v in hex_values]  # °C 변환

    # TXT 파일 저장
    with open(filename, "w") as f:
        # HEX 영역
        f.write("=== START HEX ===\n")
        for y in range(24):
            line = ""
            for x in range(32):
                val = hex_values[y * 32 + x]
                line += f"{val:04X} "
                if (x + 1) % 8 == 0:
                    line += " "
            f.write(line.strip() + "\n")
        f.write("=== END HEX ===\n\n")

        # 온도 영역
        f.write("=== TEMPERATURE (°C) ===\n")
        for y in range(24):
            line = ""
            for x in range(32):
                temp = temps[y * 32 + x]
                line += f"{temp:05.2f} "
            f.write(line.strip() + "\n")

    # PNG 저장 (현재 화면 그대로)
    plt.imsave(f"frame_{timestamp}.png", resized_frame, cmap='inferno')
    print(f"[💾 저장 완료] {filename}, frame_{timestamp}.png")

# ================================================================
# Matplotlib '저장 버튼' 이벤트 연결
# ================================================================
def on_save_button(event):
    """ Matplotlib toolbar의 저장 버튼 눌렀을 때 호출 """
    try:
        save_frame(last_raw, last_frame, last_resized)
    except Exception as e:
        print("❌ 저장 실패:", e)

# Matplotlib toolbar에서 'save' 버튼 클릭 이벤트 감시
fig.canvas.mpl_connect('key_press_event', lambda event: save_frame(last_raw, last_frame, last_resized) if event.key == 's' else None)
fig.canvas.manager.toolbar.save_figure = lambda *args, **kwargs: save_frame(last_raw, last_frame, last_resized)

# ================================================================
# 시리얼 프레임 읽기 함수
# ================================================================
def read_frame():
    while True:
        head = ser.read(2)
        if head in [b'\x5A\x5A', b'\x5A\x5B']:  # 헤더 예외 허용
            size = ser.read(2)
            if len(size) < 2:
                continue
            length = size[1] * 256 + size[0]
            data = ser.read(length)
            if len(data) >= 1536:
                return data[:1536]


# ================================================================
# 메인 루프
# ================================================================
last_raw, last_frame, last_resized = None, None, None

while True:
    try:
        raw = read_frame()
        temps = [(raw[i+1] << 8 | raw[i]) / 100.0 for i in range(0, 1536, 2)]
        frame = np.array(temps).reshape((24, 32))
        resized_frame = zoom(frame, (10, 10))  # 10배 확대

        # 화면 업데이
        img.set_data(resized_frame)
        img.set_clim(20, 60)
        ax.set_title(f"🔥 Max: {np.max(frame):.1f}°C | ❄️ Min: {np.min(frame):.1f}°C | 📊 Avg: {np.mean(frame):.1f}°C")
        plt.pause(0.05)

        # 최신 프레임 저장 (이벤트에서 접근 가능하도록)
        last_raw, last_frame, last_resized = raw, frame, resized_frame

        # S 키 누르면 저장
        if keyboard.is_pressed('s'):
            save_frame(raw, frame, resized_frame)

    except Exception as e:
        print("Error:", e)
        break
