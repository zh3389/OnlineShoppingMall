# OnlineShoppingMall
在线商城 后台管理


#### Docker 打包部署

```commandline
git clone 本项目
cd 本项目路径
docker build -t shopmall:latest .
docker run -p 8000:80 -v $(PWD)/data/drawingbed:/app/drawingbed -v $(PWD)/data/database:/app/database -d shopmall:latest

保存镜像到本地
docker save -o shopmall.tar shopmall
上传镜像
scp shopmall.tar root@192.168.1.1:/root/XXX/XXX
登录到 root@192.168.1.1 加载镜像
docker load -i ueba-ml.tar
接口文档
http://192.168.1.1:8000/docs
```