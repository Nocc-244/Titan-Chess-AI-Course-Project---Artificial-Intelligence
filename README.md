# Titan Chess AI - Đồ án môn Trí tuệ Nhân tạo

## Giới thiệu

Titan Chess AI là chương trình cờ vua được phát triển trong khuôn khổ học phần Trí tuệ Nhân tạo. Mục tiêu của dự án là nghiên cứu và triển khai các thuật toán tìm kiếm trạng thái trong môi trường đối kháng, đồng thời xây dựng một AI có khả năng chơi cờ vua bằng cách kết hợp các kỹ thuật tìm kiếm và đánh giá vị trí.

Chương trình cho phép người dùng chơi cờ vua với máy thông qua giao diện đồ họa trực quan. AI được xây dựng dựa trên thuật toán Minimax kết hợp Alpha-Beta Pruning và các kỹ thuật tối ưu hóa nhằm nâng cao chất lượng nước đi.

---

## Mục tiêu dự án

* Tìm hiểu và triển khai thuật toán Minimax trong trò chơi đối kháng.
* Áp dụng Alpha-Beta Pruning để giảm số lượng trạng thái cần tìm kiếm.
* Xây dựng hàm đánh giá vị trí cờ vua dựa trên tri thức chuyên môn.
* Thiết kế giao diện người dùng thân thiện.
* Lưu và xuất ván đấu dưới định dạng PGN.

---

## Các kỹ thuật được sử dụng

### 1. Minimax Search

Thuật toán Minimax được sử dụng để mô phỏng quá trình ra quyết định của hai người chơi đối kháng. AI giả định đối thủ luôn thực hiện nước đi tối ưu và lựa chọn nước đi mang lại kết quả tốt nhất cho bản thân.

### 2. Alpha-Beta Pruning

Alpha-Beta Pruning được tích hợp nhằm loại bỏ các nhánh không cần thiết trong cây tìm kiếm, giúp giảm đáng kể thời gian tính toán mà vẫn đảm bảo kết quả tương đương Minimax đầy đủ.

### 3. Move Ordering

Các nước đi được sắp xếp theo mức độ ưu tiên trước khi tìm kiếm, giúp Alpha-Beta Pruning hoạt động hiệu quả hơn.

### 4. Quiescence Search

Kỹ thuật Quiescence Search được sử dụng để xử lý các vị trí chiến thuật chưa ổn định (bắt quân, đổi quân liên tiếp), giúp giảm hiện tượng Horizon Effect và nâng cao độ chính xác của hàm đánh giá.

### 5. Check Extension

Trong các tình huống vua đang bị chiếu, độ sâu tìm kiếm được mở rộng thêm nhằm tránh việc đánh giá sai các vị trí quan trọng.

---

## Hàm đánh giá vị trí

Chương trình đánh giá vị trí dựa trên nhiều yếu tố:

* Giá trị vật chất của quân cờ.
* Piece-Square Tables (giá trị vị trí của từng quân trên bàn cờ).
* Độ linh hoạt của quân cờ (Mobility).
* Mức độ an toàn của vua.
* Thưởng cho cặp tượng (Bishop Pair Bonus).
* Đánh giá chuyên biệt cho giai đoạn tàn cuộc.

---

## Kiến trúc hoạt động của AI

```text
Tới lượt AI
        │
        ▼
Sinh các nước đi hợp lệ
        │
        ▼
Move Ordering
        │
        ▼
Minimax + Alpha-Beta Pruning
        │
        ▼
Quiescence Search
        │
        ▼
Đánh giá vị trí
        │
        ▼
Chọn nước đi tốt nhất
```

---

## Cấu trúc dự án

```text
Titan Chess AI
│
├── main.py
├── minimax.py
├── GUI.py
├── assets/
├── latest_game.pgn
└── README.md
```

### Chức năng các thành phần

| Tệp             | Chức năng                                  |
| --------------- | ------------------------------------------ |
| main.py         | Điều khiển chương trình và quản lý ván đấu |
| minimax.py      | Thuật toán AI và hàm đánh giá              |
| GUI.py          | Giao diện đồ họa                           |
| assets          | Hình ảnh quân cờ và tài nguyên giao diện   |
| latest_game.pgn | Lưu ván đấu gần nhất                       |

---

## Thành viên nhóm

| Thành viên      | Phân công                                                                      |
| --------------- | ------------------------------------------------------------------------------ |
| Nguyễn Thị Hà   | Thiết kế và phát triển chương trình, xây dựng thuật toán AI |
| Trần Danh Đoàn  | Viết báo cáo, thiết kế slide thuyết trình                                      |
| Nguyễn Tuấn Đạt | Viết báo cáo, thiết kế slide thuyết trình                                      |
| Phạm Minh Trí   | Hỗ trợ code, Kiểm thử                                    |

---

## Hướng dẫn chạy mã nguồn

### Yêu cầu

* Python 3.10 trở lên

### Cài đặt thư viện

```bash
pip install python-chess
```

### Chạy chương trình

```bash
python main.py
```

---

## Phiên bản thực thi (EXE)

Đối với người dùng không muốn cài đặt Python, có thể sử dụng phiên bản EXE được đóng gói sẵn:

https://drive.google.com/file/d/1bWk9hxkc68zcqGe0ikTn-bFGGj2dpjp6/view?usp=sharing


Hướng dẫn:

1. Tải file Titan AI.zip.
2. Giải nén thư mục.
3. Chạy file thực thi.
4. Bắt đầu chơi cờ với AI.

---

## Kiểm thử và đánh giá

Chương trình được kiểm thử thông qua các ván đấu thực tế và phân tích bằng Chess.com Analysis Board.

Kết quả cho thấy AI có khả năng:

* Thực hiện các chiến thuật cơ bản.
* Khai thác lợi thế vật chất.
* Xử lý các tình huống đổi quân hợp lý.
* Đưa ra nhiều nước đi trùng với đề xuất của công cụ phân tích.

---

## Công nghệ sử dụng

* Python
* Tkinter
* python-chess
* PyInstaller

---

## Tài liệu tham khảo

[1] Chess.com Analysis Board.
Công cụ phân tích ván cờ và đánh giá chất lượng nước đi.
https://www.chess.com/analysis

[2] Chess Programming Wiki – Simplified Evaluation Function.
Tomasz Michniewski.
Tài liệu về giá trị quân cờ (Piece Values), bảng điểm vị trí (Piece-Square Tables) và hàm đánh giá trong Chess Engine.
https://www.chessprogramming.org/Simplified_Evaluation_Function

[3] python-chess Documentation.
Tài liệu chính thức của thư viện python-chess.
https://python-chess.readthedocs.io

[4] GeeksforGeeks.
Minimax Algorithm in Game Theory.
https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-1-introduction/

[5] GeeksforGeeks.
Alpha-Beta Pruning for Minimax Algorithm.
https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-4-alpha-beta-pruning/

[6] Russell, S., & Norvig, P.
Artificial Intelligence: A Modern Approach.
Pearson Education.

[7] Shannon, C. E. (1950).
Programming a Computer for Playing Chess.
Philosophical Magazine.

[8] Knuth, D. E., & Moore, R. W. (1975).
An Analysis of Alpha-Beta Pruning.
Artificial Intelligence Journal.

[9] Maharaj, S., Polson, N., & Turk, A. (2021).
Chess AI: Competing Paradigms for Machine Intelligence.

[10] Monroe, D., Eilender, G., Chalmers, P., Tang, Z., & Anderson, A. (2026).
Chessformer: A Unified Architecture for Chess Modeling.
