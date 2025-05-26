from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QTextCursor, QColor, QTextCharFormat, QTextBlockFormat
from openai import OpenAI
from qfluentwidgets import PushButton, SwitchButton, TextEdit, TextBrowser
import json
import os
import time

from client.AI import Ui_ai

HISTORY_DIR = "chat_history"


class ChatTextEdit(TextBrowser):
    # 保持你原有的ChatTextEdit实现不变
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QTextBrowser {
                background: #f5f7fb;
                border: none;
                padding: 10px;
            }
        """)
        self.document().setDefaultStyleSheet("hr { border: 0; border-top: 1px solid #cccccc; margin: 5px 0; }")
        self.ai_format = self.create_text_format(QColor("#2d2d2d"))
        self.user_format = self.create_text_format(QColor("#0078D4"))

    def create_text_format(self, color):
        char_format = QTextCharFormat()
        char_format.setForeground(color)
        return char_format

    def append_message(self, text, is_ai=True):
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.End)

        if not self.document().isEmpty():
            cursor.insertText("\n")
            time_format = QTextCharFormat()
            time_format.setFontPointSize(8)
            time_format.setForeground(QColor("#666666"))

            block_format = QTextBlockFormat()
            block_format.setAlignment(Qt.AlignLeft)
            cursor.mergeBlockFormat(block_format)

            current_time = QtCore.QDateTime.currentDateTime().toString("HH:mm:ss")
            cursor.insertText(f"{current_time}\n")

        block_format = QTextBlockFormat()
        alignment = Qt.AlignLeft if is_ai else Qt.AlignRight
        block_format.setAlignment(alignment)
        cursor.mergeBlockFormat(block_format)

        char_format = self.ai_format if is_ai else self.user_format
        cursor.setCharFormat(char_format)
        cursor.insertText(text + "\n")
        self.setTextCursor(cursor)
        self.ensureCursorVisible()
        return cursor.position()

    def append_temp_message(self, text, is_ai=True):
        """ 插入临时消息并返回起始位置 """
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.End)
        start = cursor.position()
        self.append_message(text, is_ai)
        return start

    def replace_temp_message(self, start_pos, new_text):
        """ 替换临时消息 """
        cursor = self.textCursor()
        cursor.setPosition(start_pos)
        cursor.movePosition(QTextCursor.End, QTextCursor.KeepAnchor)
        cursor.removeSelectedText()
        self.append_message(new_text, is_ai=True)


class AiWorker(QThread):
    finished = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, client, messages,model):
        super().__init__()
        self.client = client
        self.messages = messages
        self.model = model
    def run(self):
        max_retries = 3
        retry_delay = 5

        for attempt in range(max_retries):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=self.messages,
                    stream=False,
                    timeout=30
                )
                reply = response.choices[0].message.content
                self.finished.emit(reply)
                break
            except Exception as e:
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                else:
                    self.error.emit(f"请求失败: {str(e)}")


class Ai_Widget(QtWidgets.QWidget):
    def __init__(self, cfg,User,tab_id=0):
        super().__init__()
        self.Username = User
        self.cfg = cfg
        self.client =OpenAI(api_key=cfg.API.value, base_url="https://api.deepseek.com")
        self.tab_id = tab_id
        self.messages = []
        self.history_file = os.path.join(HISTORY_DIR, f"../../user/{User}/chat_history.json")
        history_dir = os.path.dirname(self.history_file)
        if not os.path.exists(history_dir):
            os.makedirs(history_dir)

        if not os.path.exists(self.history_file):
            with open(self.history_file, 'w') as f:
                f.write('[]')  # 写入空数组
        # 初始化UI
        self.ui = Ui_ai()
        self.ui.setupUi(self)
        self.ui.TextEdit_2.setPlaceholderText("请输入你的问题")
        # 替换原有TextEdit为自定义聊天框
        self.ui.TextEdit = ChatTextEdit(self)
        self.ui.TextEdit.setGeometry(QtCore.QRect(0, 0, 811, 548))
        # 连接信号
        self.ui.PushButton.clicked.connect(self.send_message)
        self.current_model = "deepseek-chat"
        self.ui.SwitchButton.checkedChanged.connect(self.on_model_changed)
        # 初始化历史记录
        self.load_history()

    def on_model_changed(self, is_checked: bool):
        """ SwitchButton状态变化处理 """
        if is_checked:
            self.current_model = "deepseek-reasoner"  # 开启时使用大模型
            print("[DEBUG] 切换到深度模式")
        else:
            self.current_model = "deepseek-chat"  # 关闭时使用标准模型
            print("[DEBUG] 切换到标准模式")

    def send_message(self):
        user_input = self.ui.TextEdit_2.toPlainText().strip()
        if not user_input:
            return

        # 添加用户消息
        self.messages.append({"role": "user", "content": user_input})
        self.ui.TextEdit.append_message(user_input, is_ai=False)
        self.ui.TextEdit_2.clear()
        thinking_text = "正在深度思考..." if self.current_model == "deepseek-reasoner" else "正在思考..."
        self.temp_msg_pos = self.ui.TextEdit.append_temp_message(thinking_text, is_ai=True)
        # 禁用发送按钮
        self.ui.PushButton.setEnabled(False)

        # 创建并启动工作线程
        self.worker = AiWorker(self.client, self.messages,self.current_model)
        self.worker.finished.connect(self.handle_response)
        self.worker.error.connect(self.handle_error)
        self.worker.start()

    def handle_response(self, reply):
        self.ui.TextEdit.replace_temp_message(self.temp_msg_pos, reply)
        self.messages.append({"role": "assistant", "content": reply})
        self.ui.PushButton.setEnabled(True)
        self.save_history()

    def handle_error(self, error_msg):
        self.ui.TextEdit.replace_temp_message(self.temp_msg_pos, error_msg)
        QtWidgets.QMessageBox.critical(self, "错误", error_msg)
        self.ui.PushButton.setEnabled(True)

    def load_history(self):
        try:
            with open(self.history_file, "r") as f:
                self.messages = json.load(f)
                for msg in self.messages:
                    if msg["role"] == "user":
                        self.ui.TextEdit.append_message(msg["content"], is_ai=False)
                    elif msg["role"] == "assistant":
                        self.ui.TextEdit.append_message(msg["content"], is_ai=True)
        except (FileNotFoundError, json.JSONDecodeError):
            self.messages = [{"role": "system", "content": "You are a helpful assistant."}]

    def save_history(self):
        os.makedirs(HISTORY_DIR, exist_ok=True)
        with open(self.history_file, "w") as f:
            json.dump(self.messages, f)