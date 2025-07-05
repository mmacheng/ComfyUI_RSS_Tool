A simple RSS widget that can parse the URL of the article based on the RSS subscription source you provide, and can also get the article content based on the parsed URL.
![image](https://github.com/user-attachments/assets/d4d91202-0571-4dca-98b2-f8c9837095f9)
Note:
You need to manually download the punkt resource
Use the browser to visit the following link to download the punkt compressed package
https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/tokenizers/punkt.zip
After the download is successful, you need to unzip it to ~\custom_nodes\ComfyUI_RSS_Tool\nltk_data\tokenizers
After success, the directory is as follows:
ComfyUI/
└── custom_nodes/
    └── ComfyUI_RSS_Tool/
        ├── __init__.py
        └── nltk_data/
            └── tokenizers/
                └── punkt/
