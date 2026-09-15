# 完整课程文字提取
插件视频页点击“提取完整课程文字”下载任务 JSON，然后：
`python3 -m pip install -r requirements.txt`
`python3 extract.py ~/Downloads/课程.pku-video.json`
输出 `outputs/<课程名>/全文.txt`。首次运行会下载 Whisper 模型。
