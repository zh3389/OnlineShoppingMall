## API接口文档

#### 后台
查询 GET /api/backend/ | 新增 POST /api/backend/ | 修改 PATCH /api/backend/ | 删除 DELETE /api/backend/
1. 仪表盘: GET /api/backend/dashboard
2. 分类管理: GET /api/backend/classification | 新增 POST /api/backend/class_add | 修改 PATCH /api/backend/class_update | 删除 DELETE /api/backend/class_delete
3. 商品管理: GET /api/backend/product | 新增 POST /api/backend/product_add | 修改 PATCH /api/backend/product_update | 删除 DELETE /api/backend/product_delete
4. 卡密管理: GET /api/backend/cami | 新增 POST /api/backend/cami_add | 修改 PATCH /api/backend/cami_update | 删除 DELETE /api/backend/cami_delete
5. 优惠券: GET /api/backend/coupon | 新增 POST /api/backend/coupon_add | 修改 PATCH /api/backend/coupon_update | 删除 DELETE /api/backend/_delete
6. 订单列表: GET /api/backend/order | 搜索 GET /api/backend/order_search | 删除 DELETE /api/backend/order_delete
7. 用户管理: GET /api/backend/user | 搜索 GET /api/backend/user_search | 重置密码 PATCH /api/backend/user_reset | 删除 DELETE /api/backend/
8. 图床管理: GET /api/backend/drawingbed | 新增 POST /api/backend/drawingbed_add | 删除 DELETE /api/backend/drawingbed_delete
9. 佣金记录: GET /api/backend/invite | 搜索 GET /api/backend/invite_search | 删除 DELETE /api/backend/invite_delete
10. 主题设置: GET /api/backend/theme | 更新 PATCH /api/backend/theme_update
11. 支付接口: GET /api/backend/payment | 回调地址保存 PATCH /api/backend/payment_update | 修改 PATCH /api/backend/payment_update
12. 消息通知: GET /api/backend/message | SMTP测试 POST /api/backend/message_smtp_test | SMTP保存 PATCH /api/backend/message_smtp_save | Admin测试 POST /api/backend/message_admin_test | Admin设置 PATCH /api/backend/message_admin_set | 消息开关 PATCH /api/backend/message_switch 
13. 综合设置: GET /api/backend/other | 店铺公告 PATCH /api/backend/shop_notice | 底部备案 PATCH /api/backend/icp | 可选参数 PATCH /api/backend/other_optional | 管理员账密修改 PATCH /api/backend/admin_reset
14. 返回商店: 主页URL
15. 退出登录: 清除COOKIE

#### 前台

1. 首页 GET /api/frontend/home
2. 用户注册 POST /api/frontend/user_register
3. 用户登录 POST /api/frontend/user_login
4. 忘记密码 POST /api/frontend/user_forgetpassword
5. 邀请好友 GET /api/frontend/user_invitation
6. 个人中心 GET /api/frontend/user_center
7. 我的钱包 GET /api/frontend/user_wallet
8. 重置密码 PATCH /api/frontend/user_reset
9. 订单中心 GET /api/frontend/user_order
10. 订单查询 GET /api/frontend/user_order_query
11. 退出登录: 清除COOKIE
