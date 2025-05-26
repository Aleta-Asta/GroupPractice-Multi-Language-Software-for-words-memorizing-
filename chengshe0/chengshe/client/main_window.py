import sys

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtWidgets import QFrame, QHBoxLayout, QApplication, QWidget, QDialog
from qfluentwidgets import NavigationItemPosition, FluentWindow, SubtitleLabel, setFont, SettingCardGroup, qconfig, \
    ColorSettingCard, setThemeColor, OptionsSettingCard, FluentIcon, setTheme, Theme, FluentStyleSheet, HyperlinkCard
from qfluentwidgets import FluentIcon as FIF
from setAPI import StrSettingCard
from client.login import Ui_Dialog
from client.users_manager import users, save_users
from home import Ui_home_widget
from userConfig import UserConfig
from startup_screen import Splash_Screen
from tiankong import Ui_fanyi
from deepseek import Ai_Widget
class LoginDialog(QDialog):

    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        # 初始化错误标签为隐藏状态
        self.ui.label_2.setVisible(False)
        self.ui.label_2.setStyleSheet("color: red;")
        # 连接登录按钮点击事件
        self.ui.PrimaryPushButton.clicked.connect(self.check_credentials)
    def check_credentials(self):
        # 获取输入的用户名和密码
        username = self.ui.LineEdit_2.text().strip()
        password = self.ui.LineEdit.text().strip()
        # 清除之前的错误提示
        self.ui.label_2.setVisible(False)
        if username=="":
            self.ui.label_2.setText("请输入用户名")
            self.ui.label_2.setVisible(True)
        elif username not in users:
            users[username] = password
            save_users(users)
            self.accept()
        elif users[username] == password:
            self.accept()
        else:
            # 显示错误标签
            self.ui.label_2.setText("用户名或密码错误！")
            self.ui.label_2.setVisible(True)
            # 清空密码输入框
            self.ui.LineEdit.setText("")
class HomeWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_home_widget()
        self.ui.setupUi(self)

        # 可以在这里进行自定义设置
        self.ui.ProgressRing.setValue(65)  # 设置进度值
class xuanze_Widget(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_fanyi()
        self.ui.setupUi(self)
class Widget(QFrame):

    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.label = SubtitleLabel(text, self)
        self.hBoxLayout = QHBoxLayout(self)

        setFont(self.label, 24)
        self.label.setAlignment(Qt.AlignCenter)
        self.hBoxLayout.addWidget(self.label, 1, Qt.AlignCenter)

        # 必须给子界面设置全局唯一的对象名
        self.setObjectName(text.replace(' ', '-'))


class Window(FluentWindow):
    """ 主界面 """
    def __init__(self,User):
        super().__init__()
        ###设置颜色卡添加部分
        self.cfg = UserConfig()
        self.username = User
        try:
            qconfig.load(f"../user/{User}/{User}.json", self.cfg)
        except Exception as e:
            qconfig.save()
        # 创建设置卡片
        self.cardcolor = ColorSettingCard(
            configItem=self.cfg.primaryColor,
            icon=FIF.PALETTE,
            title="主题色",
            content="调整应用主题的颜色",
            enableAlpha=True,
            parent=self
        )
        self.APIcard=StrSettingCard(
            '',
            configItem=self.cfg.API,
            icon=FluentIcon.ADD_TO,
            title="API",
            content="调整AI的API",
            enableAlpha=True,
            parent=self)
        self.deepseekcard = HyperlinkCard(
            url="https://platform.deepseek.com/usage",
            text="打开deepseekAPI页面",
            icon="./resource/deepseek.png",
            title="getAPI",
            content="获得属于自己的deepseek的API，并启用ai功能"
        )
        # 创建子界面，实际使用时将 Widget 换成自己的子界面
        self.homeInterface = HomeWidget()
        self.xuanzeInterface = xuanze_Widget()
        self.aiInterface = Ai_Widget(self.cfg,self.username)
        self.albumInterface = Widget('Album Interface', self)
        self.albumInterface1 = Widget('Album Interface 1', self)

        self.cfg.primaryColor.valueChanged.connect(lambda x: setThemeColor(x))
        self.settingInterface = SettingCardGroup("设置", self)
        self.settingInterface.setObjectName("settingInterface")
        self.settingInterface.addSettingCard(self.cardcolor)
        self.settingInterface.addSettingCards([self.APIcard, self.deepseekcard])

        ###
        self.initNavigation()
        self.initWindow()
        self.center()
    def initNavigation(self):
        #创建图标
        self.addSubInterface(self.homeInterface, FIF.HOME, 'Home')


        self.navigationInterface.addSeparator()
        self.addSubInterface(self.xuanzeInterface, FluentIcon.CHECKBOX, 'Multiple - choice')
        self.addSubInterface(self.albumInterface, FIF.ALBUM, 'Albums', NavigationItemPosition.SCROLL)
        self.addSubInterface(self.albumInterface1, FIF.ALBUM, 'Album 1', parent=self.albumInterface)
        self.addSubInterface(self.aiInterface, "./resource/deepseek.png", 'deepseek',NavigationItemPosition.BOTTOM)
        self.addSubInterface(self.settingInterface, FIF.SETTING, 'Settings', NavigationItemPosition.BOTTOM)

    def initWindow(self):
        self.setFixedSize(1024, 768)
        self.navigationInterface.setExpandWidth(200)
        self.setWindowIcon(QIcon('./resource/logo.png'))
        self.setWindowTitle('PyQt-Fluent-Widgets')
        self.navigationInterface.expand(useAni=False)

    def center(self):
        """将窗口居中显示的方法"""
        # 获取屏幕的几何信息（分辨率）
        screen_geometry = QApplication.desktop().screenGeometry()
        # 获取窗口的几何信息
        window_geometry = self.frameGeometry()
        # 计算居中位置：屏幕中心减去窗口一半大小
        window_geometry.moveCenter(screen_geometry.center())
        # 将窗口移动到计算好的位置
        self.move(window_geometry.topLeft())