# 🔥 MLX90640 Thermal Visualizer  
**Version:** v1.0  
**Author:** HyunJong Ryoo (guswhd6656@naver.com)  
**Last Updated:** 2025-11-04  

---

## 🧩 프로젝트 개요
이 프로젝트는 **Melexis MLX90640 열화상 센서**로부터 시리얼(UART)을 통해 온도 데이터를 수신하고  
실시간으로 히트맵(Heatmap)을 시각화하는 **Python 기반 툴**입니다.

실시간으로 센서의 온도 분포를 표시하며,  
`S` 키 또는 **Matplotlib의 저장 버튼**을 누르면 자동으로 아래 파일들이 생성됩니다:

- `frame_YYYYMMDD_HHMMSS.txt` → HEX 데이터 + 온도값 저장  
- `frame_YYYYMMDD_HHMMSS.png` → 현재 열화상 화면 캡처 이미지 저장  

---

## ⚙️ 개발 환경 및 사용 툴

| 항목 | 내용 |
|------|------|
| **OS** | Windows 10 / 11 |
| **Language** | Python 3.11 |
| **IDE** | PyCharm Community Edition |
| **Version Control** | Git / GitHub |
| **Sensor** | Melexis MLX90640 (32×24 열화상 센서) |
| **Dependencies** | `pyserial`, `numpy`, `matplotlib`, `scipy`, `keyboard` |

> 설치 명령어  
> ```bash
> pip install -r requirements.txt
> ```

---

## 🚀 실행 방법

1️⃣ 코드 상단의 시리얼 포트 및 통신 속도 설정:
```python
COM_PORT = 'COM4'
BAUD_RATE = 115200
