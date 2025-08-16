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
        pyxel.text(self.dialog.x + self.x, self.dialog.y + self.y, self.text, 0) # COLOR_BLACK -> 0

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
        # COLOR_LIGHT_GRAY -> 13, COLOR_GRAY -> 6, COLOR_DARK_GRAY -> 5
        bg_color = 13
        if self.is_hover:
            bg_color = 6
        if self.is_pressed:
            bg_color = 5

        # ボタンの描画 (COLOR_BLACK -> 0)
        pyxel.rect(x, y, self.width, self.height, bg_color)
        pyxel.rectb(x, y, self.width, self.height, 0)

        # テキストを中央に配置 (COLOR_BLACK -> 0)
        text_x = x + (self.width - len(self.text) * pyxel.FONT_WIDTH) / 2
        text_y = y + (self.height - pyxel.FONT_HEIGHT) / 2
        pyxel.text(text_x, text_y, self.text, 0)
