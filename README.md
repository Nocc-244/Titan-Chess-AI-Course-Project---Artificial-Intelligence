# Titan Chess AI – Project Nhập Môn Trí tuệ nhân tạo

## Giới thiệu

Titan Chess AI là chương trình cờ vua được xây dựng trong khuôn khổ học phần Trí tuệ nhân tạo.

Chương trình sử dụng thuật toán Minimax kết hợp Alpha-Beta Pruning, Quiescence Search và các hàm đánh giá vị trí để tìm nước đi tối ưu.

## Chức năng

* Chơi cờ vua với máy.
* Giao diện trực quan.
* Lưu ván đấu dưới định dạng PGN.
* Đánh giá vị trí dựa trên giá trị quân cờ và vị trí quân cờ.
* Hỗ trợ tìm kiếm nước đi bằng Minimax và Alpha-Beta Pruning.
* Hiệu năng của chương trình được đánh giá thông qua các ván đấu thử nghiệm và phân tích bằng Chess.com Analysis Board. AI có khả năng thực hiện các chiến thuật cơ bản, tận dụng lợi thế vật chất và xử lý các tình huống trung cuộc, tàn cuộc ở mức độ khá.

## Cấu trúc dự án

* `main.py`: Điều khiển chương trình và quản lý ván đấu.
* `minimax.py`: Thuật toán tìm kiếm và đánh giá.
* `GUI.py ở trong folder .ven`: Giao diện người dùng.
* `assets/`: Hình ảnh và tài nguyên giao diện.
* `latest_game.pgn`: Lưu ván đấu gần nhất.

## Kiến trúc thuật toán

```
Tới lượt AI
        ↓
Tìm các nước đi hợp lệ
        ↓
Sắp xếp nước đi
        ↓
Minimax + Alpha-Beta Pruning
        ↓
Quiescence Search
        ↓
Đánh giá vị trí
        ↓
Chọn nước đi tốt nhất
```

## Thành viên nhóm

| Thành viên      | Phân công                                                 |
| --------------- | --------------------------------------------------------- |
| Nguyễn Thị Hà   | Xây dựng chương trình, triển khai thuật toán AI|
| Trần Danh Đoàn  | Viết báo cáo, thiết kế slide thuyết trình                 |
| Nguyễn Tuấn Đạt | Viết báo cáo, thiết kế slide thuyết trình                 |
| Phạm Minh Trí   |Hỗ trợ code , kiểm thử               |

## Hướng dẫn sử dụng

Người dùng có thể tải file nén **Titan AI.zip**, giải nén thư mục và chạy chương trình để trải nghiệm chơi cờ với AI.

## Công nghệ sử dụng

* Python
* Tkinter
* python-chess

## Tài liệu tham khảo

1. Chess.com Analysis Board
2. Chess Programming Wiki
3. python-chess Documentation
4. Minimax Algorithm – GeeksforGeeks
5. Alpha-Beta Pruning – GeeksforGeeks
6. Artificial Intelligence: A Modern Approach
7. An Analysis of Alpha-Beta Pruning
8. Programming a Computer for Playing Chess
9. Chess AI: Competing Paradigms for Machine Intelligence
10. Chessformer: A Unified Architecture for Chess Modeling
