A simple RSS widget that can parse the URL of the article based on the RSS subscription source you provide, and can also get the article content based on the parsed URL.
![image](https://github.com/user-attachments/assets/d4d91202-0571-4dca-98b2-f8c9837095f9)
注意：
需要手动下载 punkt 资源
使用浏览器访问以下链接下载 punkt 压缩包
https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/tokenizers/punkt.zip 
下载成功后需要解压到~\custom_nodes\ComfyUI_RSS_Tool\nltk_data\tokenizers下面
成功后目录是如下：
ComfyUI/
└── custom_nodes/
    └── ComfyUI_RSS_Tool/
        ├── __init__.py
        └── nltk_data/
            └── tokenizers/
                └── punkt/
