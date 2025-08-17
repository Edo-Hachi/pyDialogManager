"""
ファイル保存ダイアログの連携機能

ファイルシステムとダイアログウィジェットを連携させる機能を提供
"""
import os
from file_utils import FileManager
from dialog_manager import DialogManager
from system_settings import settings

class FileSaveDialogController:
    """ファイル保存ダイアログのコントローラークラス"""
    
    def __init__(self, dialog_manager: DialogManager, initial_directory: str = None):
        self.dialog_manager = dialog_manager
        self.file_manager = FileManager(initial_directory)
        self.active_dialog = None
        
    def show_save_dialog(self, default_filename: str = ""):
        """ファイル保存ダイアログを表示し、ファイルシステムと連携"""
        # ダイアログを表示
        self.dialog_manager.show("IDD_SAVE_AS")
        self.active_dialog = self.dialog_manager.active_dialog
        
        if self.active_dialog:
            # 初期化処理
            self._initialize_dialog(default_filename)
    
    def _initialize_dialog(self, default_filename: str):
        """ダイアログの初期化"""
        if not self.active_dialog:
            return
            
        # ファイル名入力ウィジェットにデフォルトファイル名を設定
        filename_widget = self._find_widget("IDC_FILENAME")
        if filename_widget:
            if default_filename:
                filename_widget.text = default_filename
            elif not filename_widget.text:
                filename_widget.text = "untitled.txt"
    
    def _find_widget(self, widget_id: str):
        """ウィジェットIDでウィジェットを検索"""
        if not self.active_dialog:
            return None
            
        for widget in self.active_dialog.widgets:
            if hasattr(widget, 'id') and widget.id == widget_id:
                return widget
        return None
    
    def handle_save_button(self):
        """Saveボタンが押された時の処理"""
        filename_widget = self._find_widget("IDC_FILENAME")
        if not filename_widget or not filename_widget.text.strip():
            print("No filename entered")
            return None
            
        filename = filename_widget.text.strip()
        
        # 絶対パスでない場合は現在のディレクトリと結合
        if not os.path.isabs(filename):
            full_path = os.path.join(self.file_manager.get_current_path(), filename)
        else:
            full_path = filename
        
        # ファイルが既に存在する場合の確認（今回は簡単に警告のみ）
        if os.path.exists(full_path):
            print(f"Warning: File already exists: {full_path}")
        
        print(f"Saving file to: {full_path}")
        return full_path
    
    def handle_cancel_button(self):
        """Cancelボタンが押された時の処理"""
        print("Save dialog cancelled")
        return None
    
    def update(self):
        """フレームごとの更新処理"""
        if not self.active_dialog:
            return
            
        # ボタンクリックのチェック
        self._check_button_clicks()
    
    def _check_button_clicks(self):
        """ボタンクリックをチェックして対応する処理を実行"""
        if not self.active_dialog:
            return
            
        # 各ボタンのクリック状態をチェック
        for widget in self.active_dialog.widgets:
            if hasattr(widget, 'id') and hasattr(widget, 'is_pressed') and widget.is_pressed:
                if widget.id == "IDOK":
                    result = self.handle_save_button()
                    if result:
                        print(f"File selected for saving: {result}")
                elif widget.id == "IDCANCEL":
                    self.handle_cancel_button()