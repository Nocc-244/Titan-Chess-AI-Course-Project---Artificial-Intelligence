import tkinter as tk
import tkinter.messagebox as messagebox
import chess
import chess.pgn  
import random
import threading 
import datetime    
from GUI import ChessGUI
from minimax import find_best_move 

# =====================================================================
# 🎮 BỘ ĐIỀU KHIỂN GAME (GIỮ NGUYÊN TOÀN BỘ LOGIC GIAO DIỆN)
# =====================================================================
class GameController:
    def __init__(self):
        self.root = tk.Tk()
        self.root.controller = self  
        
        # === CẤU HÌNH TÊN VÀ ELO BAN ĐẦU ===
        self.player_name = "You"
        self.player_elo = 1500
        self.bot_name = "TITAN CHESS AI"
        self.bot_elo = 2000  
        
        self.root.title(f"🦾 {self.bot_name} ({self.bot_elo}) v4.0 PRO 🦾")
        self.root.geometry("830x620") 
        self.root.configure(bg="#2c3e50")
        
        self.board = chess.Board()
        self.AI_DEPTH = 4  
        
        self.gui = None
        self.move_history = []     
        self.move_history_san = []
        self.player_resigned = False 
        self.player_color = chess.WHITE 
        self.ai_is_thinking = False  
        self.selected_time_mode = "infinite" 

        self.create_start_menu()
        
    def create_start_menu(self):
        self.root.geometry("830x620")
        for widget in self.root.winfo_children():
            widget.destroy()
            
        self.menu_frame = tk.Frame(self.root, bg="#2c3e50")
        self.menu_frame.pack(expand=True, fill=tk.BOTH)
        
        center_frame = tk.Frame(self.menu_frame, bg="#2c3e50")
        center_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
            
        tk.Label(center_frame, text=self.bot_name, font=("Courier", 26, "bold"), bg="#2c3e50", fg="#e74c3c").pack(pady=(10, 5))
        tk.Label(center_frame, text=f"BOT ELO: {self.bot_elo} | YOUR ELO: {self.player_elo}", font=("Arial", 11, "italic"), bg="#2c3e50", fg="#ecf0f1").pack(pady=(0, 20))
        
        tk.Label(center_frame, text="⚔️ CHỌN PHE CHIẾN ĐẤU (KHÔNG GIỚI HẠN THỜI GIAN)", font=("Arial", 11, "bold"), bg="#2c3e50", fg="#bdc3c7").pack(pady=(10, 5))
        
        btn_frame = tk.Frame(center_frame, bg="#2c3e50")
        btn_frame.pack(pady=10)
        
        btn_white = tk.Button(btn_frame, text="♔ TRẰNG", font=("Arial", 12, "bold"), bg="#ecf0f1", fg="#2c3e50", width=10, height=2, cursor="hand2", command=lambda: self.start_game(chess.WHITE))
        btn_white.grid(row=0, column=0, padx=8)
        
        btn_random = tk.Button(btn_frame, text="❓ NGẪU NHIÊN", font=("Arial", 12, "bold"), bg="#3498db", fg="white", width=12, height=2, cursor="hand2", command=self.start_random_game)
        btn_random.grid(row=0, column=1, padx=8)
        
        btn_black = tk.Button(btn_frame, text="♚ ĐEN", font=("Arial", 12, "bold"), bg="#1a252f", fg="#ecf0f1", width=10, height=2, cursor="hand2", command=lambda: self.start_game(chess.BLACK))
        btn_black.grid(row=0, column=2, padx=8)

    def start_random_game(self):
        self.start_game(random.choice([chess.WHITE, chess.BLACK]))

    def start_game(self, color):
        self.player_color = color
        self.board = chess.Board() 
        self.move_history.clear()
        self.move_history_san.clear()
        self.player_resigned = False
        self.ai_is_thinking = False
        self.init_chess_ui()

    def init_chess_ui(self):
        for widget in self.root.winfo_children():
            widget.destroy()
            
        self.root.geometry("") 
        self.root.configure(bg="#2c3e50") 
        
        self.gui = ChessGUI(
            root=self.root, 
            board=self.board, 
            move_callback=self.handle_player_move, 
            player_color=self.player_color,
            time_mode=self.selected_time_mode,
            undo_callback=self.undo_move,
            resign_callback=self.resign_game,
            on_back_to_menu_callback=self.reset_game
        )
        
        self.gui.is_player_turn = (self.player_color == chess.WHITE)
        self.gui.draw()
        self.update_title()
        
        if hasattr(self.gui, 'update_move_log'):
            self.gui.update_move_log(self.move_history_san)
            
        self.root.update()

        if self.player_color == chess.BLACK:
            self.trigger_ai_thread()

    def update_title(self):
        if self.ai_is_thinking:
            turn_text = f"⚡ {self.bot_name} CHƯA NGHĨ XONG, ĐANG QUÉT CỜ..."
        else:
            if self.board.turn == self.player_color:
                turn_text = f"LƯỢT CỦA BẠN ({self.player_elo})"
            else:
                turn_text = f"⚡ {self.bot_name} CHƯA NGHĨ XONG, ĐANG QUÉT CỜ..."
                
        color_text = "[TRẰNG]" if self.player_color == chess.WHITE else "[ĐEN]"
        self.root.title(f"🦾 {turn_text} {color_text} 🦾")

    def check_is_draw_active(self):
        if self.board.is_stalemate() or self.board.is_insufficient_material():
            return True
        if hasattr(self.board, 'can_claim_threefold_repetition') and self.board.can_claim_threefold_repetition():
            return True
        if hasattr(self.board, 'can_claim_fifty_moves') and self.board.can_claim_fifty_moves():
            return True
        if hasattr(self.board, 'is_fivefold_repetition') and self.board.is_fivefold_repetition():
            return True
        return False

    def handle_player_move(self, from_square, to_square):
        if self.ai_is_thinking or (self.board.turn != self.player_color):
            return

        move = chess.Move(from_square, to_square)
        piece = self.board.piece_at(from_square)
        
        if piece and piece.piece_type == chess.PAWN:
            if (piece.color == chess.WHITE and chess.square_rank(to_square) == 7) or \
               (piece.color == chess.BLACK and chess.square_rank(to_square) == 0):
                move.promotion = chess.QUEEN

        if move in self.board.legal_moves:
            san_move = self.board.san(move)
            self.move_history_san.append(san_move)
            self.board.push(move)
            self.move_history.append(self.board.fen())  
            
            self.gui.is_player_turn = False
            self.gui.draw()
            
            if self.board.is_game_over() or self.check_is_draw_active():
                self.check_game_over()
                return
                
            if hasattr(self.gui, 'update_move_log'):
                self.gui.update_move_log(self.move_history_san)
            
            self.trigger_ai_thread()
        else:
            self.gui.draw()

    def trigger_ai_thread(self):
        self.ai_is_thinking = True
        self.update_title()
        threading.Thread(target=self.async_ai_task, daemon=True).start()

    def async_ai_task(self):
        ai_color = chess.BLACK if self.player_color == chess.WHITE else chess.WHITE
        
        if self.board.fullmove_number == 1 and ai_color == chess.WHITE:
            opening_moves = ["e2e4", "d2d4", "g1f3", "c2c4"]
            ai_move = chess.Move.from_uci(random.choice(opening_moves))
        else:
            board_copy = self.board.copy()
            ai_move = find_best_move(board_copy, depth=self.AI_DEPTH, history=self.move_history, ai_color=ai_color)
            
        if ai_move and not self.player_resigned:
            self.root.after(0, self.apply_ai_move, ai_move)

    def apply_ai_move(self, ai_move):
        if self.player_resigned:
            self.ai_is_thinking = False
            self.update_title()
            return
            
        san_move = self.board.san(ai_move)
        self.move_history_san.append(san_move)
        self.board.push(ai_move)
        self.move_history.append(self.board.fen())
        
        self.gui.draw()
        
        if self.board.is_game_over() or self.check_is_draw_active():
            self.ai_is_thinking = False
            self.update_title()
            self.check_game_over()
            return

        if hasattr(self.gui, 'update_move_log'):
            self.gui.update_move_log(self.move_history_san)
            
        self.ai_is_thinking = False
        self.gui.is_player_turn = True
        self.update_title()

    def undo_move(self):
        if self.board.is_game_over() or self.player_resigned or self.ai_is_thinking or self.check_is_draw_active():
            return
        if len(self.board.move_stack) >= 2:
            self.board.pop()  
            self.board.pop()  
            if len(self.move_history) >= 2:
                self.move_history.pop()
                self.move_history.pop()
            if len(self.move_history_san) >= 2:
                self.move_history_san.pop()
                self.move_history_san.pop()
            self.gui.selected_square = None
            
            self.gui.is_player_turn = True
            self.gui.draw()
            if hasattr(self.gui, 'update_move_log'):
                self.gui.update_move_log(self.move_history_san) 
            self.update_title()

    def save_game_to_pgn(self):
        game = chess.pgn.Game.from_board(self.board)
        game.headers["Event"] = "Titan AI friendly match"
        game.headers["Site"] = "Titan Engine Pro"
        game.headers["Date"] = datetime.datetime.now().strftime("%Y.%m.%d")
        game.headers["Round"] = "1"
        
        if self.player_color == chess.WHITE:
            game.headers["White"] = self.player_name
            game.headers["Black"] = self.bot_name
            game.headers["WhiteElo"] = str(self.player_elo)
            game.headers["BlackElo"] = str(self.bot_elo)
        else:
            game.headers["White"] = self.bot_name
            game.headers["Black"] = self.player_name
            game.headers["WhiteElo"] = str(self.bot_elo)
            game.headers["BlackElo"] = str(self.player_elo)

        if self.player_resigned:
            game.headers["Result"] = "0-1" if self.player_color == chess.WHITE else "1-0"
            game.headers["Termination"] = "Normal (Resignation)"
        elif self.board.is_checkmate():
            game.headers["Result"] = "0-1" if self.board.turn == chess.WHITE else "1-0"
            game.headers["Termination"] = "Normal (Checkmate)"
        elif self.board.is_game_over() or self.check_is_draw_active():
            game.headers["Result"] = "1/2-1/2"
            game.headers["Termination"] = "Normal (Draw)"
        else:
            game.headers["Result"] = "*"
            
        with open("latest_game.pgn", "w", encoding="utf-8") as f:
            exporter = chess.pgn.FileExporter(f)
            game.accept(exporter)
        print(f"\n=== [SYSTEM]: ĐÃ GHI FILE PGN CHO {self.player_name} ===")

    def resign_game(self):
        if self.board.is_game_over() or self.player_resigned or self.check_is_draw_active(): 
            return
        confirm = messagebox.askyesno("Xác Nhận", f"Bạn muốn đầu hàng {self.bot_name}?")
        if confirm:
            self.player_resigned = True 
            self.ai_is_thinking = False
            self.gui.is_player_turn = False
            self.save_game_to_pgn() 
            
            # --- ÉP GIAO DIỆN CẬP NHẬT LẠI KẾT QUẢ ĐẦU HÀNG ---
            if self.gui:
                self.gui.draw()
                if hasattr(self.gui, 'update_move_log'):
                    self.gui.update_move_log(self.move_history_san)
                    
            self.show_result_popup("TITAN AI WIN!", f"Bạn đã đầu hàng trước {self.bot_name}.", "#e74c3c")

    def check_game_over(self):
        self.save_game_to_pgn()
        
        # --- ÉP GIAO DIỆN CẬP NHẬT LẠI KẾT QUẢ KHI HẾT VÁN ---
        if self.gui:
            self.gui.draw()
            if hasattr(self.gui, 'update_move_log'):
                self.gui.update_move_log(self.move_history_san)

        if self.board.is_checkmate():
            if self.board.turn == self.player_color:
                title = "TITAN AI WIN!"
                msg = f"Bạn đã bị {self.bot_name} chiếu hết."
                color = "#e74c3c"
            else:
                title = "YOU WIN!"
                msg = f"Chúc mừng! Bạn đã chiếu hết {self.bot_name}."
                color = "#2ecc71"
        elif self.board.is_stalemate():
            title = "KẾT QUẢ: HÒA!"
            msg = "Trận đấu hòa do rơi vào thế bí (Stalemate)."
            color = "#f1c40f"
        elif self.board.is_insufficient_material():
            title = "KẾT QUẢ: HÒA!"
            msg = "Trận đấu hòa do cả hai bên không đủ lực lượng chiếu hết."
            color = "#f1c40f"
        elif hasattr(self.board, 'can_claim_fifty_moves') and self.board.can_claim_fifty_moves():
            title = "KẾT QUẢ: HÒA!"
            msg = "Trận đấu hòa theo luật 50 nước đi không ăn quân và không đi Tốt."
            color = "#f1c40f"
        elif hasattr(self.board, 'can_claim_threefold_repetition') and self.board.can_claim_threefold_repetition():
            title = "KẾT QUẢ: HÒA!"
            msg = "Trận đấu hòa do lặp lại thế cờ 3 lần."
            color = "#f1c40f"
        else:
            title = "KẾT QUẢ: HÒA!"
            msg = "Trận đấu kết thúc với kết quả hòa!"
            color = "#f1c40f"
            
        self.show_result_popup(title, msg, color)

    def show_result_popup(self, title_text, msg_text, theme_color):
        popup = tk.Toplevel(self.root)
        popup.title("KẾT QUẢ TRẬN ĐẤU")
        popup.geometry("420x240")
        popup.configure(bg="#1a252f")
        
        popup.transient(self.root)
        popup.grab_set()
        
        tk.Label(popup, text=title_text, font=("Courier", 24, "bold"), fg=theme_color, bg="#1a252f").pack(pady=(25, 10))
        tk.Label(popup, text=msg_text, font=("Arial", 11, "bold"), fg="#ecf0f1", bg="#1a252f", wraplength=380).pack(pady=10)
        
        tk.Button(popup, text="LÀM VÁN MỚI", font=("Arial", 11, "bold"), bg=theme_color, fg="white", bd=0, padx=15, pady=6, cursor="hand2", command=lambda: [popup.destroy(), self.reset_game()]).pack(pady=(15, 0))

    def reset_game(self):
        self.board = chess.Board()
        self.move_history.clear()
        self.move_history_san.clear() 
        self.player_resigned = False  
        self.ai_is_thinking = False
        self.create_start_menu() 

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    game = GameController()
    game.run()