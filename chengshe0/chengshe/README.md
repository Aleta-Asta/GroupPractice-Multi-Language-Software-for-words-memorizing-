我们文件有3个文件夹，client为前端，server为后端，user为用户数据，其中users.json文件储存了用户名和密码，使用方法可在login.py与users_manager.py文件中参考，

每位用户有单独的一个文件夹，其中另有一个f"用户名".json文件储存数据，现储存了用户的颜色偏好,后面也可以扩展，这个json文件使用方法可参考UserConfig.py文件与main_window.py中设置卡的添加部分以及文档[配置类 | QFluentWidgets](https://qfluentwidgets.com/zh/pages/components/config)（我也不懂原理，但程序能跑），

主要需要设计的是main_window中如下部分![image-20250523162338493](C:\Users\50376\AppData\Roaming\Typora\typora-user-images\image-20250523162338493.png)

用自己的页面替换music等。

请参考[流畅窗口 | QFluentWidgets](https://qfluentwidgets.com/zh/pages/components/fluentwindow)

此外，若qfluentwdigets的图标无法使用，可以换成普通图标，遇到问题可以在群里问问

除此之外吗，我认为我们分工可能需要调整一下，学习QT与json的代价太高，简单按之前分工三人都要学QT,效率太低，我觉得可以分为1,背诵以外的所有图形界面；2，背诵的图形界面3，后端，包括数据接口和数据处理