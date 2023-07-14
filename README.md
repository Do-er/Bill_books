
# 批量自动化微信&支付宝账单
```
### 目标：
统计每月甚至每年的开支，看看自己钱都花在哪了，一个月到底存下了多少。
焦点在哪，钱就在哪，人生就在哪...

### 实现：
1.支持自动去除上传的订单重复部分
2.支持支付宝的余额宝、结息算入收入
3.支持设置一张工资卡：
      工资卡转入、转出到微信或者支付宝算作支出里面
4.支持配置账单过滤规则
      默认退款、还信用卡、还花呗、交易关闭的订单不计入统计
      默认金额为0或0.1的不计统计
5.支持自动化生成分类，生成规则同样支持DIY
```
# Getting Start
## 1. 配置环境
   * 开发版本: python 3.11
```
      pip install -r os enum time numpy pandas openpyxl
```
   
## 2. 配置 src/config.py
   * GlobalConfig: 全局路径、配置
   * MajorLabels: 分类标签-大类
   * BillLabels: 分类标签-小类
   * AutoLabelRules: 自动标注规则

## 3. 下载账单
   * 微信账单
      1. 进入手机版微信，选择 “我”
      2. 点击 “服务” -> “钱包”-> 右上角“账单” 
      3. 点击右上角“常见问题” 
      4. 点击“下载账单”->“用于个人对账”
      4. 设置要导出账单日期范围->填写接收账单邮箱
      5. 前往邮箱下载压缩包,解压密码在微信消息里面
      6.  解压后.csv 格式就是微信账单。
   
   * 支付宝账单
      1. 进入手机支付宝，选择 “我的”
      2. 点击 “账单” -> 右上角“···”三个点 
      3. 点击“开具交易流水证明” 
      4. 选择“用于个人对账”->输入密码
      4. 设置要导出账单日期范围->填写接收账单邮箱
      5. 前往邮箱下载压缩包,解压密码为身份证后四位
      6.  解压后.csv 格式就是支付宝账单。
   
## 4. 按目录结构存放账单：
```
    │  .gitignore
    │  main.py
    │  README.md
    ├─AccountBooks
    │  │   KeepAccountDataBase.xlsx
    ├─records
    │  │  alipay_record_20230115_1641_1.csv (可存放多个csv)
    │  │  微信支付账单(20221216-20230115).csv (可存放多个csv)
    │  └─.old_records (请勿删除此目录)
    └─src
        │  AccountBook.py
        │  Annotator.py
        │  config.py
    
```

## 5. 虚拟机运行`./main.py` 或者`python3 main.py`
## 6. KeepAccountDataBase.xlsx中手动订正、追加records
## 7. 可视化图表 (此部分作者暂无模板)
### Enjoy!
------


# Development ideas

```
一、开始之前将重复文件全部删除

二、调整"收支"列表
支付宝  收益发放  收入
支付宝  赔付成功  收入
支付宝  账户结息  收入

微信 已退款 算出差价 支出  #非全额退款，需要算出实际扣款

支付方式包含0139   收支为不记收支
    商品为转出转入 对应  支出收入

支付方式包含0139    收支为\
    支付状态 充值和提现 计入支出收入

三、过滤无效数据
1.支付状态
      退款成功
      交易关闭
      还款成功
      对方已退还
      已全额退款
      已退款￥xx.xx  #微信的不完全退款无效行需要删掉，有效行格式不同，为"已退款￥(xx.xx)"
      
2.金额
      0.1,0

3.收支    #调整之后的
      “\”
      “不记支出”    
```

