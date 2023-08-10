#### Date:20230715   
#### Author:LeoChin

import sys
from src.Magic import Magic
from src.Config import GlobalConfig
from src.BatchBills import BatchBills

def main():
    magic = Magic()
    cfg = GlobalConfig()
    make = BatchBills(cfg)
    
    if len(sys.argv)  == 2:                                                                      #单独制作可视化图表
        Excel = sys.argv[1]
        df = make.import_records_excel(Excel)
        magic.do_visualization(df)

    else:
        make.create_records()                                                                   #将CSV数据全部抓取到 bills ,准备批量处理
        
        make.adjust_balance()                                                                   #优化收支项
       
        make.data_filtering()                                                                   #数据过滤，排除不计算的表格
        
        make.bills = magic.do_annotation(make.bills)                           #加分类


        #---------------------调试输出
        # df = make.bills
        # df = df.iloc[:, [4,5,6,7,10]]  
        # make.dfprint(df,"打印结果")
        

        make.export_excel()                                                                     #导出为Excel
        
        # magic.do_visualization(make.bills)                                          #导出可视化图表
        
        cfg.cfgprint()                                                                              #输出重要配置信息

if __name__ == '__main__':
    main()

