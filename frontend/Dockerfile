# 使用 Nginx 基础镜像
FROM nginx:alpine

# 复制自定义 nginx 配置
COPY docker/nginx.conf /etc/nginx/nginx.conf

# 复制本地构建的静态文件到 nginx 默认目录
COPY dist/ /usr/share/nginx/html/

# 暴露端口
EXPOSE 80

# 启动 nginx
CMD ["nginx", "-g", "daemon off;"] 