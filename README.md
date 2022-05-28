极验一键通过模式与滑动模式-float JS逆向破解
-
#### 说明：本项目主要使用python和nodejs开发,以极验官网demo作为案例,为避免滥用已对JS文件做混淆处理
#### 启动：先运行 `./static/js/api.js` ,然后选择运行 `geetest_wugan.py` 或者 `geetest_slide.py`
#### 版本：`fullpage 9.0.8` `slide 7.8.6`

    geetest_wugan.py  # 一键通过模式  
       
    geetest_slide.py  # 滑动模式 
    
    ./static/js/api.js # api接口 
  
更新
-
#### 2022.1.08 更新日志  
在一位朋友的帮助下,对geetest_slide.py做了部分优化,主要提高了成功率和运行效率(目前成功率80%左右)  

----
#### 2022.5.28 更新日志
目前官网已更新到 `fullpage.9.1.0` `slide 7.8.6`,可能会出现已经通过滑块但是`validate`不能用的情况。这时需要更改`captcha_token`：打开
`./static/js/fullpage.js`,搜索并替换`381215664`即可。(如果你知道`w`的加密位置的话)  
ps：后续可能会更新四代的，敬请期待  

----

免责声明
-
#### 该项目仅用于学术交流，不得任何商业使用！如有疑问，请通过邮箱联系本人
