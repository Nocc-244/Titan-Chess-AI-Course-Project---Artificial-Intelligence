import tkinter as tk
import tkinter.messagebox as messagebox
import chess
import os
from PIL import Image, ImageTk

class ChessGUI:
    def __init__(self, root, board, move_callback, player_color, time_mode="infinite", undo_callback=None, resign_callback=None, on_back_to_menu_callback=None):
        self.root = root
        self.board = board
        self.move_callback = move_callback
        self.undo_callback = undo_callback      
        self.resign_callback = resign_callback  
        self.on_back_to_menu_callback = on_back_to_menu_callback 
        self.player_color = player_color
        
        self.selected_square = None
        self.square_size = 60
        self.board_size = self.square_size * 8
        self.is_player_turn = (self.player_color == chess.WHITE)
        
        self.color_light = "#f0d9b5"
        self.color_dark = "#b58863"
        self.color_highlight = "#baca44"
        self.color_bg_panel = "#2c3e50"    
        self.color_sidebar = "#34495e"     
        
        self.assets_dir = "assets"
        self.piece_images = {}
        self.load_piece_images()
        
        # === CẤU HÌNH LƯỚI CHO LỚP BỌC CHÍNH ĐỂ TỰ ĐỘNG GIÃN THEO CỬA SỔ ===
        self.main_frame = tk.Frame(self.root, bg=self.color_bg_panel)
        self.main_frame.pack(expand=True, fill=tk.BOTH)
        
        self.main_frame.rowconfigure(0, weight=1)    # Hàng bàn cờ và sidebar tự giãn hết chiều cao
        self.main_frame.rowconfigure(1, weight=0)    # Hàng nút điều khiển giữ nguyên chiều cao vừa đủ
        self.main_frame.columnconfigure(0, weight=3) # Cột bên trái (Bàn cờ) chiếm phần lớn không gian
        self.main_frame.columnconfigure(1, weight=1) # Cột bên phải (Sidebar) chiếm phần ít hơn
        
        self.create_widgets()
        self.draw()
        
        # Bắt sự kiện thay đổi kích thước cửa sổ để co giãn bàn cờ động
        self.canvas.bind("<Configure>", self.on_resize)

    def load_piece_images(self):
        name_mapping = {
            'P': 'w_pawn', 'N': 'w_knight', 'B': 'w_bishop', 'R': 'w_rook', 'Q': 'w_queen', 'K': 'w_king',
            'p': 'b_pawn', 'n': 'b_knight', 'b': 'b_bishop', 'r': 'b_rook', 'q': 'b_queen', 'k': 'b_king'
        }
        for p, prefix in name_mapping.items():
            file_name = f"{prefix}_png_shadow_128px.png"
            img_path = os.path.join(self.assets_dir, file_name)
            if os.path.exists(img_path):
                img = Image.open(img_path).convert("RGBA")
                # Resize theo kích thước ô hiện tại
                img = img.resize((self.square_size, self.square_size), Image.Resampling.LANCZOS)
                self.piece_images[p] = ImageTk.PhotoImage(img)
            else:
                self.piece_images[p] = None

    def create_widgets(self):
        # Canvas bàn cờ sử dụng sticky="nsew" để bám sát và giãn ra mọi hướng
        self.canvas = tk.Canvas(self.main_frame, width=self.board_size, height=self.board_size, bd=0, highlightthickness=0)
        self.canvas.grid(row=0, column=0, padx=15, pady=10, sticky="nsew")
        self.canvas.bind("<Button-1>", self.on_square_click)
        
        self.control_bar = tk.Frame(self.main_frame, bg=self.color_bg_panel)
        self.control_bar.grid(row=1, column=0, pady=(0, 15), padx=15, sticky="ew")
        self.control_bar.columnconfigure(0, weight=1)
        self.control_bar.columnconfigure(1, weight=1)
        
        self.btn_undo = tk.Button(self.control_bar, text="⇆ XIN ĐI LẠI", font=("Arial", 11, "bold"), 
                                  bg="#d35400", fg="white", bd=0, height=2, cursor="hand2", command=self.trigger_undo)
        self.btn_undo.grid(row=0, column=0, padx=(0, 8), sticky="ew")
        
        self.btn_resign = tk.Button(self.control_bar, text="🏳️ ĐẦU HÀNG", font=("Arial", 11, "bold"), 
                                    bg="#c0392b", fg="white", bd=0, height=2, cursor="hand2", command=self.trigger_resign)
        self.btn_resign.grid(row=0, column=1, padx=(8, 0), sticky="ew")
        
        # Sidebar bên phải chứa Biên bản ván đấu (Cấu hình sticky="nsew" để giãn hết chiều cao)
        self.sidebar = tk.Frame(self.main_frame, bg=self.color_sidebar, width=280)
        self.sidebar.grid(row=0, column=1, rowspan=2, padx=(10, 15), pady=10, sticky="nsew")
        
        self.lbl_title = tk.Label(self.sidebar, text="BIÊN BẢN VÁN ĐẤU", font=("Arial", 11, "bold"), bg=self.color_sidebar, fg="white")
        self.lbl_title.pack(pady=(15, 5))
        
        self.log_text = tk.Text(self.sidebar, font=("Courier", 10), bg="#243342", fg="#ecf0f1", bd=0, highlightthickness=0, height=8, wrap=tk.WORD)
        self.log_text.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
        
        self.btn_copy = tk.Button(self.sidebar, text="💾 SAO CHÉP BIÊN BẢN", font=("Arial", 10, "bold"), bg="#3498db", fg="white", bd=0, height=2, cursor="hand2", command=self.copy_to_clipboard)
        self.btn_copy.pack(fill=tk.X, padx=10, pady=5)
        
        self.separator2 = tk.Frame(self.sidebar, height=2, bg="#2c3e50")
        self.separator2.pack(fill=tk.X, padx=10, pady=8)
        
        self.btn_back_menu = tk.Button(self.sidebar, text="🏠 QUAY LẠI MENU CHÍNH", font=("Arial", 10, "bold"), bg="#e67e22", fg="white", bd=0, height=2, cursor="hand2", command=self.return_to_start_menu)
        self.btn_back_menu.pack(fill=tk.X, padx=10, pady=(5, 15))
        
        self.update_move_log([])

    def on_resize(self, event):
        min_size = min(event.width, event.height)
        if min_size < 200:  
            return
            
        self.square_size = min_size // 8
        self.board_size = self.square_size * 8
        
        self.load_piece_images()
        self.draw()

    def trigger_undo(self):
        if self.board.is_game_over() or self.board.is_stalemate() or self.board.is_insufficient_material():
            return
        if self.undo_callback:
            self.undo_callback()

    def trigger_resign(self):
        if self.board.is_game_over() or self.board.is_stalemate() or self.board.is_insufficient_material():
            return
        if self.resign_callback:
            self.resign_callback()

    def return_to_start_menu(self):
        self.main_frame.pack_forget()
        self.main_frame.destroy()
        if self.on_back_to_menu_callback:
            self.on_back_to_menu_callback()

    def draw(self):
        self.canvas.delete("all")
        last_move = self.board.peek() if self.board.move_stack else None
        
        for rank in range(8):
            for file in range(8):
                display_rank = rank if self.player_color == chess.BLACK else 7 - rank
                display_file = 7 - file if self.player_color == chess.BLACK else file
                
                square = chess.square(display_file, display_rank)
                x1, y1 = file * self.square_size, rank * self.square_size
                x2, y2 = x1 + self.square_size, y1 + self.square_size
                
                color = self.color_light if (rank + file) % 2 == 0 else self.color_dark
                if self.selected_square == square:
                    color = self.color_highlight
                elif last_move and (square == last_move.from_square or square == last_move.to_square):
                    color = "#d4d673"
                    
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")
                
                piece = self.board.piece_at(square)
                if piece:
                    p_sym = piece.symbol()
                    if self.piece_images.get(p_sym):
                        self.canvas.create_image(x1, y1, anchor=tk.NW, image=self.piece_images[p_sym])
                        
        self.root.update_idletasks()

    def on_square_click(self, event):
        if not self.is_player_turn or self.board.is_game_over() or self.board.is_stalemate() or self.board.is_insufficient_material():
            return  
            
        file, rank = event.x // self.square_size, event.y // self.square_size
        if file > 7 or rank > 7: 
            return
            
        display_rank = rank if self.player_color == chess.BLACK else 7 - rank
        display_file = 7 - file if self.player_color == chess.BLACK else file
        clicked_square = chess.square(display_file, display_rank)
        
        if self.selected_square is None:
            piece = self.board.piece_at(clicked_square)
            if piece and piece.color == self.board.turn:
                self.selected_square = clicked_square
                self.draw()
        else:
            from_sq = self.selected_square
            self.selected_square = None
            self.move_callback(from_sq, clicked_square)

    # === 🔥 ĐÃ FIX LỖI HIỂN THỊ KẾT QUẢ ĐẦU HÀNG TRÊN BIÊN BẢN VĂN ĐẤU ===
    def update_move_log(self, move_history_san):
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete("1.0", tk.END)
        
        white_name = "You" if self.player_color == chess.WHITE else "TITAN AI"
        black_name = "TITAN AI" if self.player_color == chess.WHITE else "You"
        
        # Kiểm tra xem bộ điều khiển chính có cờ hiệu đầu hàng hay chưa
        is_resigned = False
        if hasattr(self.root, 'controller') and self.root.controller:
            is_resigned = getattr(self.root.controller, 'player_resigned', False)
        
        # Tính toán chuỗi kết quả chuẩn xác nhất
        if is_resigned:
            # Nếu người chơi chọn phe Trắng đầu hàng -> Đen thắng (0-1), ngược lại Trắng thắng (1-0)
            result_tag = "0-1" if self.player_color == chess.WHITE else "1-0"
        elif self.board.is_game_over() or self.board.is_stalemate() or self.board.is_insufficient_material() or self.board.can_claim_threefold_repetition():
            result_tag = self.board.result()
            if result_tag == "*": 
                result_tag = "1/2-1/2"
        else:
            result_tag = "*"
            
        w_elo = "1500" if white_name == "You" else "2000"
        b_elo = "1500" if black_name == "You" else "2000"
        
        pgn_data =  f'[White "{white_name}"]\n[WhiteElo "{w_elo}"]\n'
        pgn_data += f'[Black "{black_name}"]\n[BlackElo "{b_elo}"]\n[Result "{result_tag}"]\n\n'
        
        move_list = []
        for i in range(0, len(move_history_san), 2):
            w_move = move_history_san[i]
            b_move = move_history_san[i+1] if (i + 1) < len(move_history_san) else ""
            move_list.append(f"{(i//2)+1}.{w_move} {b_move}".strip())
            
        pgn_data += " ".join(move_list)
        self.log_text.insert(tk.END, pgn_data)
        self.log_text.see(tk.END)  
        self.log_text.config(state=tk.DISABLED)

    def copy_to_clipboard(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.log_text.get("1.0", tk.END).strip())
        messagebox.showinfo("Thành Công", "Đã sao chép biên bản PGN!")