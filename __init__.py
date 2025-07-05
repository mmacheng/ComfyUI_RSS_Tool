# __init__.py

import os
import shutil
from newspaper import Article
import nltk
from lxml import etree
import requests
from io import StringIO

# 新增节点 1：RSS/Atom Feed 解析器（使用 lxml + requests）
class RSSFeedParserNode:
    """
    RSS/Atom Feed 解析器

    使用 lxml + requests 解析远程 Feed，提取每篇文章的链接。
    支持 RSS 和 Atom 格式，兼容 Python 3.x。
    """
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("feed_links",)
    FUNCTION = "execute"
    CATEGORY = "Data Fetching"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "feed_url": ("STRING", {
                    "multiline": False,
                    "default": "https://news.ycombinator.com/rss "
                }),
                "timeout": ("INT", {
                    "default": 10,
                    "min": 1,
                    "max": 60,
                    "step": 1,
                    "display": "slider"
                })
            }
        }

    def execute(self, feed_url, timeout):
        try:
            response = requests.get(feed_url, timeout=timeout)
            response.raise_for_status()
            response.encoding = 'utf-8'  # 强制设置编码
            
            # 移除 XML 声明（如 <?xml version="1.0" encoding="UTF-8"?>）
            xml_content = response.text.replace('<?xml version="1.0" encoding="UTF-8"?>', '')
            
            # 使用 parse 处理完整 XML 文档（避免因不完整内容导致的错误）
            tree = etree.parse(StringIO(xml_content))
            root = tree.getroot()
            
            # 提取链接
            links = []
            if root.tag == 'rss':
                links = self.parse_rss(root)
            elif root.tag.startswith('{http://www.w3.org/2005/Atom}'):
                links = self.parse_atom(root)
            else:
                raise ValueError(f"Unsupported feed format: {root.tag}")
            
            return ("\n".join(links),)
        except Exception as e:
            return (f"Error parsing feed: {str(e)}",)

    def parse_rss(self, root):
        return [item.findtext('link') for item in root.xpath('.//item') if item.find('link') is not None]

    def parse_atom(self, root):
        ns = {'atom': 'http://www.w3.org/2005/Atom'}
        return [entry.findtext('.//atom:link[@rel="alternate"]/@href', namespaces=ns) 
                for entry in root.findall('.//atom:entry', ns)]

# 新增节点 2：文章内容提取器（使用 newspaper3k + 清理开关）
class ArticleContentExtractorNode:
    """
    文章内容提取器

    使用 newspaper3k 根据链接抓取文章内容，支持按需提取标题/正文/摘要。
    新增功能：是否清理 nltk_data 历史数据（防止占用过多磁盘空间）。
    """
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("extracted_content",)
    FUNCTION = "execute"
    CATEGORY = "Data Fetching"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "feed_links": ("STRING", {
                    "multiline": True,
                    "default": "https://example.com/article1 \nhttps://example.com/article2 "
                }),
                "extract_title": ("BOOLEAN", {"default": True}),
                "extract_summary": ("BOOLEAN", {"default": True}),
                "extract_text": ("BOOLEAN", {"default": True}),
                # 新增开关：是否清理 nltk_data 历史数据
                "clear_nltk_data": ("BOOLEAN", {"default": False})
            }
        }

    def execute(self, feed_links, extract_title, extract_summary, extract_text, clear_nltk_data):
        # 获取当前文件所在目录（即 ComfyUI_RSS_Tool 文件夹）
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # 构建 nltk_data 路径
        nltk_data_path = os.path.join(current_dir, 'nltk_data')
        # 强制指定 NLTK 数据路径（解决路径冲突问题）
        nltk.data.path.insert(0, nltk_data_path)

        # 自动验证 punkt 是否可用
        try:
            nltk.data.find('tokenizers/punkt')
            print("punkt 资源已找到！")
        except LookupError:
            print("punkt 资源未找到，正在尝试自动下载...")
            nltk.download('punkt', download_dir=nltk_data_path, quiet=True)

        links = [link.strip() for link in feed_links.split('\n') if link.strip()]
        results = []
        for link in links:
            try:
                article = Article(link)
                article.download()
                article.parse()
                content = f"URL: {link}\n"
                if extract_title:
                    content += f"Title: {article.title}\n"
                if extract_summary:
                    article.nlp()
                    content += f"Summary: {article.summary}\n"
                if extract_text:
                    content += f"Text: {article.text[:500]}...\n"
                content += "-" * 50 + "\n"
                results.append(content)
            except Exception as e:
                results.append(f"Error processing {link}: {str(e)}\n" + "-" * 50 + "\n")

        # 新增逻辑：是否清理 nltk_data 历史数据
        if clear_nltk_data:
            try:
                # 仅清理 tokenizers/punkt 子目录（保留目录结构）
                punkt_path = os.path.join(nltk_data_path, 'tokenizers', 'punkt')
                if os.path.exists(punkt_path):
                    shutil.rmtree(punkt_path)
                    print(f"已清理 nltk_data 历史数据：{punkt_path}")
                else:
                    print(f"未找到 punkt 目录，跳过清理。")
            except Exception as e:
                print(f"清理 nltk_data 失败：{str(e)}")

        return ("\n".join(results),)

# ========== 节点映射 ==========
NODE_CLASS_MAPPINGS = {
    "RSSFeedParserNode": RSSFeedParserNode,
    "ArticleContentExtractorNode": ArticleContentExtractorNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RSSFeedParserNode": "RSS/Atom Feed 解析器",
    "ArticleContentExtractorNode": "文章内容提取器"
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]