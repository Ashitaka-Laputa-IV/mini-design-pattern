"""
================================================================================
Lesson 7: Proxy (代理模式) — 反模式篇
================================================================================
  ⚠ 本课展示"反模式"：图片查看器中一次性加载所有大图片，导致内存暴涨。

  场景：图片查看器
  - 用户打开一个文件夹，里面有 50 张图片，每张约 10MB
  - 每张图片有缩略图（thumbnail）和原图（full image）
  - 用户打开文件夹时只需要看缩略图，点击后才查看原图

  问题：同事直接加载所有图片（包括原图），导致：
  1. 内存暴涨：50 × 10MB = 500MB
  2. 启动极慢：需要等待所有图片加载完成
  3. 用户其实只需要缩略图，加载原图完全是浪费

  这就是"资源密集型对象的延迟加载"问题，
  也是 Proxy 模式要解决的核心问题之一。
================================================================================
"""

import time
import sys


# ==============================================================================
# 反模式：直接加载所有大图片
# ==============================================================================
"""
▸ 坏味道：不管用不用，先全部加载到内存
▸ 后果：内存浪费、启动缓慢
"""


class HighResolutionImage:
    """
    高分辨率图片（10MB 级别）
    加载一张图片需要较长时间，占用大量内存
    """

    def __init__(self, filename: str):
        self._filename = filename
        self._image_data = None  # 模拟图片数据
        self._load_from_disk()  # ⚠ 构造时就加载！不管用不用

    def _load_from_disk(self):
        """模拟从磁盘加载图片"""
        print(f"  [加载] {self._filename} 从磁盘加载中... (10MB)", end="")
        time.sleep(0.5)  # 模拟 IO 延迟
        # 模拟 10MB 内存占用
        self._image_data = bytearray(10 * 1024 * 1024)  # 10MB
        print(" ✅ 完成")

    def display(self):
        """显示图片"""
        print(f"[显示] {self._filename} ({len(self._image_data) / 1024 / 1024:.0f}MB)")

    def get_size(self) -> str:
        return f"{len(self._image_data) / 1024 / 1024:.0f}MB"


# ==============================================================================
# 图片查看器 — 直接加载所有图片
# ==============================================================================

class PhotoViewer:
    """
    图片查看器（反模式版本）
    ⚠ 一启动就加载所有图片的原图
    """

    def __init__(self, filenames: list):
        print("\n" + "=" * 50)
        print("❌ 反模式：PhotoViewer 启动，正在加载所有图片...")
        print("=" * 50)
        start = time.time()

        # ❌ 直接创建所有 HighResolutionImage 对象
        #  构造函数内部立即从磁盘加载原图
        self._images = [HighResolutionImage(f) for f in filenames]

        elapsed = time.time() - start
        total_mb = len(filenames) * 10
        print(f"\n💥 所有图片加载完成！耗时 {elapsed:.1f}s，内存占用约 {total_mb}MB")

    def show_thumbnails(self):
        """显示缩略图（但其实已经加载了原图）"""
        print("\n[缩略图模式] 显示所有图片缩略图...")
        for img in self._images:
            # 显示缩略图，但内存中已经存了原图
            print(f"  📋 缩略图: {img._filename}")

    def open_image(self, index: int):
        """打开指定图片"""
        if 0 <= index < len(self._images):
            self._images[index].display()
        else:
            print("索引超出范围")


# ==============================================================================
# 测试
# ==============================================================================

def main():
    print("=" * 60)
    print("❌ 反模式：直接加载所有大图片的问题")
    print("=" * 60)

    # 模拟 5 张图片（实际可能 50+）
    photos = [f"photo_{i}.jpg" for i in range(1, 6)]

    print(f"\n图片列表: {photos}")
    print(f"预计每张图片 10MB，共 {len(photos) * 10}MB")

    viewer = PhotoViewer(photos)

    print("\n" + "-" * 40)
    print("用户操作：只查看缩略图")
    print("-" * 40)
    viewer.show_thumbnails()

    print("\n" + "-" * 40)
    print("用户操作：打开第 3 张图片")
    print("-" * 40)
    viewer.open_image(2)

    print("\n" + "=" * 60)
    print("💥 问题分析")
    print("=" * 60)
    print("""
  1. 内存浪费：用户可能只看 1-2 张图片，但所有 50 张都加载了
  2. 启动缓慢：必须等所有图片加载完才能操作
  3. 响应迟钝：用户只是想看缩略图，却要等原图加载

  解决方案：虚拟代理 (Virtual Proxy)
    - 一开始只创建"轻量级代理对象"
    - 代理对象有同样的接口，但内部不加载真实数据
    - 只有在真正需要显示时才去加载真实图片
    - 这就是"延迟加载" (Lazy Loading)
  """)


if __name__ == "__main__":
    main()
