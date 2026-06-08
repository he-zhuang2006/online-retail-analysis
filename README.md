项目背景
基于Kaggle的E-commerce数据集，分析不同国家的平均消费金额和购买频次，为跨国营销策略提供参考。

## 我的数据处理思路
1. **数据清洗**：删除CustomerID缺失记录；剔除UnitPrice≤0的异常订单；用箱线法去掉极端高价/高销量订单。
2. **聚合分析**：按国家分组，计算平均消费金额和总购买次数。
3. **可视化**：柱状图展示各国平均消费；饼图展示购买次数占比（小国家合并为“其他”）。

## 项目文件说明
- `online_retial_analysis.ipynb`：我逐行调试的原始Jupyter，包含完整的思考过程。
- `online_retial_analysis.ipynb.py`：将分析流程封装为函数，便于复用。

## 项目数据来源
从kaggle中E-Commerce Data中下载
Actual transactions from UK retaile

## 学到了什么
- 之前一直没有接触过pandas,做这个项目时学习了整个常用的pandas和mayplotlib
- 理解了箱线图阈值（1.5倍IQR）的实际意义。
- 熟练掌握了Jupyter代码重构为可复用的脚本。

## 运行方式
讲kaggle中E-Commerce Data数据下载,将上传文件中的read路径改为下载的文件路径即可
