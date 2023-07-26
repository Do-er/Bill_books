#### Date:20230715   
#### Author:LeoChin

from src.Magic import Magic
from src.Config import GlobalConfig
from src.BatchBills import BatchBills

def main():
    magic = Magic()
    cfg = GlobalConfig()
    make = BatchBills(cfg)

    # 将CSV数据全部抓取到 bills ,准备批量处理
    make.create_records()

    #优化收支项
    make.adjust_balance()

    #数据过滤，排除不计算的表格
    make.data_filtering() 

    #加分类
    make.bills = magic.do_annotation(make.bills)
    # df = make.bills
    # df = df.iloc[:, [4,5,6,9,10]]  #从原表格中抓取列
    # make.dfprint(df,"打印结果")
    
    #导出为Excel
    # make.export_excel()

    #导出可视化图表
    magic.do_visualization(make.bills)

if __name__ == '__main__':
    main()
