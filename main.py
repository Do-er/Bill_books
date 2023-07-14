#! /usr/bin/python3
#### 20230715    -By LeoChin

import time
from src.config import GlobalConfig
from src.AccountBook import AccountBook

def main():
    config = GlobalConfig()
    data = AccountBook(config)

    # 将CSV导出数据追加到 data_to_append ,准备批量处理
    data.create_records()

    #优化收支项
    data.adjust_balance()

    #数据过滤，排除不计算的表格
    data.data_filtering() 

    #加分类
    data.data_to_append = data.annotator.do_auto_annotation(data.data_to_append)


    #将CSV导出数据追加到 data.database暂存，准备导出到Excel
    data.append()

    # print()
    # print(data)
    # print()
    # 数据存储
    if config.OVERWRITE:
        data.save_database(data.save_path)
    else:
        new_path = f"{config.BASECSV[:-5]}_{time.strftime('%Y%m%d_%H%M%S', time.localtime())}.xlsx"
        data.save_database(new_path)

    # print('Program finished and will exit after 30 seconds.')
    # time.sleep(10)


if __name__ == '__main__':
    main()
