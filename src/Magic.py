import re
from pyecharts import options as opts
from pyecharts.charts import Pie, Bar
from src.Config import  AutoLabelRules 
from src.Config import  GlobalConfig 

from pyecharts.charts import Liquid

class Magic:
    def __init__(self):
        self.cfg = GlobalConfig()
        self.rules = AutoLabelRules().rules

    def _check_rules(self, df, rules) -> bool:
        for condition_dict in rules:#从列表中遍历字典元素
            field_match_ok = False
            
            for column, condition in condition_dict.items():#从字典中遍历键值对，字典需要至少一个键值对的规则成立
                if column in ['来源', '收支', '支付状态', '支付方式', '交易对方', '商品', '分类']:
                    condition_ok = bool(re.search(condition, df[column]))
                elif column in ['金额', '修订金额']:
                    condition_ok = condition[0] < df[column] <= condition[1]
                else:
                    raise ValueError('Wrong rules format.')
                if condition_ok:
                    field_match_ok = True
                    break
            if not field_match_ok:
                return False
        return True     #遍历完所有字典,且每个字典至少有一对通过,表示符合

    def is_Sublist(self, rules):
        for lst_value in rules:  #读取第一层列表的值
            if isinstance(lst_value, list):  # 判断列表中是否有子列表
                return  1
        return  0


    def do_annotation(self, df):
        for index, df_row in df.iterrows(): #迭代每行数据
            for label, rules in self.rules.items():  #分解分类名和分类规则
                IsSublist = self.is_Sublist(rules)      #判断分类规则包含子列表(一个名多个规则)
                can_annotate = 0

                if IsSublist:
                    for sublist in rules:  #迭代子列表
                        can_annotate = self._check_rules(df_row, sublist)
                        if can_annotate:
                            break  #有子列表符合即可跳出
                else:
                    can_annotate = self._check_rules(df_row, rules)

                if can_annotate:
                        df.at[index, "智能分类"] = label
                        break  #下一行数据
        return df

    def do_visualization (self,df):
        # 计算月总支出
        month_total_expenditure = round(df[df['收支'] == '支出']['金额'].sum(), 2)
        expenditure_by_category = df[df['收支'] == '支出'].groupby('智能分类')['金额'].sum().reset_index()
        expenditure_by_category['金额'] = round(expenditure_by_category['金额'], 2)

        title_opts = opts.TitleOpts(
            title="月支出分类占比",
            subtitle=f"总支出：{month_total_expenditure}元",
            pos_top="top",     # 标题距顶部的距离
        )

        # 使用饼图显示支出分类占比
        pie = (
            Pie()
            .add(
                "",
                [list(z) for z in zip(expenditure_by_category['智能分类'], expenditure_by_category['金额'])],
                radius=["40%", "75%"],  # 设置饼图的内外半径，显示为环形图
                label_opts=opts.LabelOpts(formatter="{b}: {c}元\n{d}%"),
            )
            .set_global_opts(
                title_opts=title_opts,
                legend_opts=opts.LegendOpts(
                    pos_bottom="10%",     # 饼图距顶部的距离
                    pos_right="0", # 饼图水平居中
                    orient="vertical", # 饼图图例垂直排列
                    item_gap=15        # 饼图图例项之间的间隔
                )
            )
        )

        # 渲染图表
        print(f'渲染图表导出到文件: {self.cfg.SAVEHTML}')
        pie.render(self.cfg.SAVEHTML)
