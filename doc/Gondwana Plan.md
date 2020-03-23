# Gondwana开发计划

## order
- [ ] Event
    - [ ] 订单可以同时存在多个状态
    - [ ] 可以作为过滤订单的条件
- [ ] Tracking No.
    - [ ] 快递单号 USPS直接写这里 DHL先写在References No.查到单号后写这里
- [x] Express v0.0.7
    * [x] 直接从cscart同步,同步后不需要修改
    - [x] 从Cscart中的ship method获取
    - [x] model: order.ship_method string(255)
- [ ] Tracking info
    - [ ] 快递备注信息
- [ ] Ship Time
    - [ ] 导入快递单号的时间
- [ ] Memo v0.0.8
    - [x] 对订单进行备注
    - [x] model: order.memo text
    - [ ] 备注要可编辑
- [ ] References No.
    - [ ] 当Express是DHL时,单号先填写在这里
- [x] Total 订单总金额
- [ ] Time
- [ ] 分页显示订单
