# Gondwana开发计划

## order
- [x] Event v0.9.0
    - [x] 订单可以同时存在多个状态
    - [x] 添加order-event many_to_many relationship
    - [x] 插入event数据并保存
    - [x] 模板显示订单event 下拉列表显示
    - [x] 显示订单已经存在的event
    - [x] 勾选ajax更新order的event
    - [x] 可以作为过滤订单的条件
    - [x] 在搜索栏中添加event过滤器
    - [x] 测试order删除后,events关联也应删除
- [x] Tracking No. v0.10.0
    - [x] 快递单号
    - [x] model: order.tracking_no string(64)
    - [x] 模板显示tracking NO
    - [x] 可ajax编辑
- [x] Express
    - [x] 直接从cscart同步,同步后不需要修改
    - [x] 从Cscart中的ship method获取
    - [x] model: order.ship_method string(255) v0.7.0
- [x] Tracking info v0.11.0
    - [x] 快递备注信息
    - [x] model: order.tracking_info text
    - [x] 模板显示tracking NO
    - [x] 可ajax编辑
- [x] Ship Time v0.12.0
    - [x] model order.ship_time datetime
    - [x] 模板显示Ship Time
- [x] Memo v0.8.0
    - [x] 对订单进行备注
    - [x] model: order.memo text
    - [x] 添加默认值--,在视图中只显示前8个字符,tooltip全文 v0.7.1
    - [x] 备注要可编辑
- [x] References No. v0.13.0
    - [x] model: order.references_no string(64)
    - [x] 模板显示References NO.
    - [x] 可ajax编辑
- [x] Total 订单总金额
- [ ] Time
- [ ] 分页显示订单

## import track notes
- [ ] tracking_no 快递单号 USPS直接写这里 DHL先写在References No.查到单号后写这里
- [ ] tracking_info 快递备注
- [ ] ship_time 导入快递单号的时间
- [ ] references_no 当Express是DHL时,单号先填写在这里
