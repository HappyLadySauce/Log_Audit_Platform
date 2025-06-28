# 登录页面背景图片说明

## 使用自定义背景图片

### 1. 添加背景图片
将你想要用作登录页面背景的图片文件放在这个目录下，建议文件名为 `login-bg.jpg` 或 `login-bg.png`

### 2. 修改代码
编辑 `src/views/login/index.vue` 文件，在 `.login-container` 样式中：

```css
.login-container {
  /* 注释掉网络图片背景 */
  /* background: url('https://images.unsplash.com/photo-1451187580459-43490279c0fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=2072&q=80') center/cover no-repeat; */
  
  /* 启用本地图片背景 */
  background: url('/images/login-bg.jpg') center/cover no-repeat;
}
```

### 3. 图片要求
- **推荐尺寸**: 1920x1080 或更高分辨率
- **文件格式**: JPG, PNG, WebP
- **文件大小**: 建议小于 2MB，以确保加载速度
- **内容建议**: 
  - 科技感背景（如数据中心、网络、代码等）
  - 商务办公场景
  - 抽象几何图案
  - 避免过于复杂的图片，以免影响登录框的可读性

### 4. 示例图片来源
如果需要免费的高质量背景图片，可以参考：
- [Unsplash](https://unsplash.com/) - 免费高质量图片
- [Pexels](https://www.pexels.com/) - 免费图片资源
- [Pixabay](https://pixabay.com/) - 免费图片库

搜索关键词建议：
- "technology background"
- "data center"
- "network security"
- "digital background"
- "abstract tech" 