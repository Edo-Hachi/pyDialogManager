import pyxel
import time

class WidgetBase:
    """すべてのウィジェットの基底クラス"""
    def __init__(self, dialog, definition):
        self.dialog = dialog
        self.id = definition.get("id")
        self.x = definition.get("x", 0)
        self.y = definition.get("y", 0)
        self.width = definition.get("width", 0)
        self.height = definition.get("height", 0)
        self.text = definition.get("text", "")

    def update(self):
        pass

    def draw(self):
        pass

class LabelWidget(WidgetBase):
    """静的テキストを表示するラベルウィジェット"""
    def __init__(self, dialog, definition):
        super().__init__(dialog, definition)
        # テキストの長さに合わせて幅を自動調整（widthが未指定の場合）
        if self.width == 0:
            self.width = len(self.text) * pyxel.FONT_WIDTH
        if self.height == 0:
            self.height = pyxel.FONT_HEIGHT

    def draw(self):
        # ダイアログの座標系に合わせて描画
        pyxel.text(self.dialog.x + self.x, self.dialog.y + self.y, self.text, pyxel.COLOR_BLACK)

class ButtonWidget(WidgetBase):
    """クリック可能なボタンウィジェット"""
    def __init__(self, dialog, definition):
        super().__init__(dialog, definition)
        self.is_hover = False
        self.is_pressed = False

    def update(self):
        # マウスカーソルがボタンの領域内にあるかチェック
        mx, my = pyxel.mouse_x, pyxel.mouse_y
        dx, dy = self.dialog.x, self.dialog.y
        
        self.is_hover = (dx + self.x <= mx < dx + self.x + self.width and
                         dy + self.y <= my < dy + self.y + self.height)

        # ホバー中に左クリックされたかチェック
        if self.is_hover and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            self.is_pressed = True
            # ここでコールバックなどを呼び出すことができる
            print(f"Button '{self.id}' pressed!")
        else:
            self.is_pressed = False

    def draw(self):
        dx, dy = self.dialog.x, self.dialog.y
        x, y = dx + self.x, dy + self.y
        
        # 状態に応じて色を変える
        bg_color = pyxel.COLOR_LIGHT_BLUE
        if self.is_hover:
            bg_color = pyxel.COLOR_GRAY
        if self.is_pressed:
            bg_color = pyxel.COLOR_DARK_GRAY

        # ボタンの描画
        pyxel.rect(x, y, self.width, self.height, bg_color)
        pyxel.rectb(x, y, self.width, self.height, pyxel.COLOR_BLACK)

        # テキストを中央に配置
        text_x = x + (self.width - len(self.text) * pyxel.FONT_WIDTH) / 2
        text_y = y + (self.height - pyxel.FONT_HEIGHT) / 2
        pyxel.text(text_x, text_y, self.text, pyxel.COLOR_BLACK)

class TextBoxWidget(WidgetBase):
    """テキスト入力が可能なテキストボックスウィジェット"""
    def __init__(self, dialog, definition):
        super().__init__(dialog, definition)
        self.has_focus = False
        self.cursor_pos = len(self.text)
        self.cursor_visible = True
        self.cursor_blink_timer = 0
        self.cursor_blink_interval = 0.5
        self.last_blink_time = time.time()
        self.max_length = definition.get("max_length", 50)
        
        # デフォルトサイズ設定
        if self.width == 0:
            self.width = 100
        if self.height == 0:
            self.height = 20

    def update(self):
        # マウスクリックでフォーカス取得
        mx, my = pyxel.mouse_x, pyxel.mouse_y
        dx, dy = self.dialog.x, self.dialog.y
        
        # フォーカス制御
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            if (dx + self.x <= mx < dx + self.x + self.width and
                dy + self.y <= my < dy + self.y + self.height):
                self.has_focus = True
                # クリック位置にカーソルを移動
                click_x = mx - (dx + self.x) - 4  # パディングを考慮
                char_index = max(0, min(click_x // 4, len(self.text)))  # 4は文字幅
                self.cursor_pos = char_index
            else:
                self.has_focus = False

        # カーソル点滅制御
        if self.has_focus:
            current_time = time.time()
            if current_time - self.last_blink_time >= self.cursor_blink_interval:
                self.cursor_visible = not self.cursor_visible
                self.last_blink_time = current_time

        # フォーカス中のキー入力処理
        if self.has_focus:
            self._handle_keyboard_input()

    def _handle_keyboard_input(self):
        """キーボード入力を処理"""
        # Backspace処理
        if pyxel.btnp(pyxel.KEY_BACKSPACE) and self.cursor_pos > 0:
            self.text = self.text[:self.cursor_pos-1] + self.text[self.cursor_pos:]
            self.cursor_pos -= 1
            self.cursor_visible = True
            self.last_blink_time = time.time()

        # Delete処理  
        if pyxel.btnp(pyxel.KEY_DELETE) and self.cursor_pos < len(self.text):
            self.text = self.text[:self.cursor_pos] + self.text[self.cursor_pos+1:]
            self.cursor_visible = True
            self.last_blink_time = time.time()

        # 左矢印キー
        if pyxel.btnp(pyxel.KEY_LEFT) and self.cursor_pos > 0:
            self.cursor_pos -= 1
            self.cursor_visible = True
            self.last_blink_time = time.time()

        # 右矢印キー
        if pyxel.btnp(pyxel.KEY_RIGHT) and self.cursor_pos < len(self.text):
            self.cursor_pos += 1
            self.cursor_visible = True
            self.last_blink_time = time.time()

        # 文字入力処理（英数字、記号）
        for key in range(256):
            if pyxel.btnp(key):
                char = self._convert_key_to_char(key)
                if char and len(self.text) < self.max_length:
                    self.text = self.text[:self.cursor_pos] + char + self.text[self.cursor_pos:]
                    self.cursor_pos += 1
                    self.cursor_visible = True
                    self.last_blink_time = time.time()

    def _convert_key_to_char(self, key):
        """キーコードを文字に変換"""
        # 英字 (a-z)
        if pyxel.KEY_A <= key <= pyxel.KEY_Z:
            char = chr(ord('a') + (key - pyxel.KEY_A))
            if pyxel.btn(pyxel.KEY_SHIFT):
                return char.upper()
            return char
        
        # 数字 (0-9)
        if pyxel.KEY_0 <= key <= pyxel.KEY_9:
            if pyxel.btn(pyxel.KEY_SHIFT):
                # Shift+数字の記号
                shift_symbols = ')!@#$%^&*('
                return shift_symbols[key - pyxel.KEY_0]
            return chr(ord('0') + (key - pyxel.KEY_0))
        
        # 基本的な記号
        symbol_map = {
            pyxel.KEY_SPACE: ' ',
            pyxel.KEY_PERIOD: '.' if not pyxel.btn(pyxel.KEY_SHIFT) else '>',
            pyxel.KEY_COMMA: ',' if not pyxel.btn(pyxel.KEY_SHIFT) else '<',
            pyxel.KEY_MINUS: '-' if not pyxel.btn(pyxel.KEY_SHIFT) else '_',
            pyxel.KEY_EQUALS: '=' if not pyxel.btn(pyxel.KEY_SHIFT) else '+',
            pyxel.KEY_SLASH: '/' if not pyxel.btn(pyxel.KEY_SHIFT) else '?',
            pyxel.KEY_SEMICOLON: ';' if not pyxel.btn(pyxel.KEY_SHIFT) else ':',
            pyxel.KEY_QUOTE: "'" if not pyxel.btn(pyxel.KEY_SHIFT) else '"',
            pyxel.KEY_LEFTBRACKET: '[' if not pyxel.btn(pyxel.KEY_SHIFT) else '{',
            pyxel.KEY_RIGHTBRACKET: ']' if not pyxel.btn(pyxel.KEY_SHIFT) else '}',
            pyxel.KEY_BACKSLASH: '\\' if not pyxel.btn(pyxel.KEY_SHIFT) else '|',
            pyxel.KEY_BACKQUOTE: '`' if not pyxel.btn(pyxel.KEY_SHIFT) else '~',
        }
        
        return symbol_map.get(key)

    def draw(self):
        dx, dy = self.dialog.x, self.dialog.y
        x, y = dx + self.x, dy + self.y
        
        # テキストボックスの背景と枠
        pyxel.rect(x, y, self.width, self.height, pyxel.COLOR_WHITE)  # 白背景
        pyxel.rectb(x, y, self.width, self.height, pyxel.COLOR_BLACK)  # 黒枠
        
        # フォーカス時は青い枠
        if self.has_focus:
            pyxel.rectb(x-1, y-1, self.width+2, self.height+2, pyxel.COLOR_LIGHT_BLUE)  # 青枠
        
        # テキスト描画
        text_x = x + 4  # 左パディング
        text_y = y + (self.height - pyxel.FONT_HEIGHT) // 2  # 垂直中央
        pyxel.text(text_x, text_y, self.text, pyxel.COLOR_BLACK)  # 黒テキスト
        
        # カーソル描画（フォーカス中かつ表示状態）
        if self.has_focus and self.cursor_visible:
            cursor_x = text_x + self.cursor_pos * 4  # 4は文字幅
            cursor_y = y + 2
            pyxel.line(cursor_x, cursor_y, cursor_x, cursor_y + self.height - 4, pyxel.COLOR_BLACK)  # 黒いカーソル
