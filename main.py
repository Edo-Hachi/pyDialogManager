import pyxel
from dialog_manager import DialogManager

class App:
    def __init__(self):
        pyxel.init(256, 256, title="Dialog System Demo")

        # ダイアログマネージャーを初期化
        self.dialog_manager = DialogManager("dialogs.json")
        
        # 最初のダイアログを表示
        self.dialog_manager.show("IDD_MAIN_DIALOG")

        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        # 数字キーで表示するダイアログを切り替え
        if pyxel.btnp(pyxel.KEY_1):
            self.dialog_manager.show("IDD_MAIN_DIALOG")
        if pyxel.btnp(pyxel.KEY_2):
            self.dialog_manager.show("IDD_FILE_OPEN")
        if pyxel.btnp(pyxel.KEY_3):
            self.dialog_manager.show("IDD_SAVE_AS")

        # ダイアログマネージャーの更新処理を呼び出す
        self.dialog_manager.update()

    def draw(self):
        # 背景を少し暗い色で塗りつぶし
        pyxel.cls(1) # Dark Blue

        # ダイアログマネージャーの描画処理を呼び出す
        self.dialog_manager.draw()

App()
