import re
from pyecharts import options as opts
from pyecharts.charts import Pie, Bar
from src.Config import  AutoLabelRules 

class Magic:
    def __init__(self):
        self.rules = AutoLabelRules().rules

    def _check_rules(self, df, rules) -> bool:
        #从列表中遍历字典元素
        for condition_dict in rules:
            field_match_ok = False
            #从字典中遍历键值对，字典需要至少一个键值对的规则成立
            for column, condition in condition_dict.items():
                if column in ['来源', '收支', '支付状态', '支付方式', '交易对方', '商品', '大类']:
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
        #遍历完所有字典,且每个字典至少有一对通过,表示符合
        return True


    def do_annotation(self, df):
        row_size = df.shape[0]
        for row in range(row_size):
            df_row = df.iloc[row]
            for label, rules in self.rules.items():
                #规则列表放入_check_rules 函数
                can_annotate = self._check_rules(df_row, rules)
                if can_annotate:
                    df.iloc[row, 10] = label
                    continue
        return df

    def do_visualization (self,df):
        # 计算月总支出
        month_total_expenditure = round(df[df['收支'] == '支出']['金额'].sum(), 2)
        expenditure_by_category = df[df['收支'] == '支出'].groupby('大类')['金额'].sum().reset_index()
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
                [list(z) for z in zip(expenditure_by_category['大类'], expenditure_by_category['金额'])],
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

        # 使用条形图显示每个分类的支出情况
        bar = (
            Bar()
            .add_xaxis(list(expenditure_by_category['大类']))  # 将 Series 转换为列表
            .add_yaxis("支出", list(expenditure_by_category['金额']), label_opts=opts.LabelOpts(formatter="{c}元"))
            .set_global_opts(title_opts=opts.TitleOpts(title="月支出情况"))
        )

        # 渲染图表
        print(f'渲染图表导出')
        pie.render("expenditure_pie.html")
        bar.render("expenditure_bar.html")

'''
    def do_visualization (self,df):
        # 计算月总支出
        month_total_expenditure = round(df[df['收支'] == '支出']['金额'].sum(), 2)

        # 按照大类分组计算每个分类的总支出，并将金额保留两位小数
        expenditure_by_category = df[df['收支'] == '支出'].groupby('大类')['金额'].sum().reset_index()
        expenditure_by_category['金额'] = round(expenditure_by_category['金额'], 2)

        # 使用饼图显示支出分类占比
        pie = (
            Pie()
            .add(
                "",
                [list(z) for z in zip(expenditure_by_category['大类'], expenditure_by_category['金额'])],
                radius=["40%", "75%"],  # 设置饼图的内外半径，显示为环形图
                label_opts=opts.LabelOpts(formatter="{b}: {c}元\n{d}%"),
            )
            .set_global_opts(
                title_opts=opts.TitleOpts(title="月支出分类占比", subtitle=f"总支出：{month_total_expenditure}元")
            )
        )

        # 使用条形图显示每个分类的支出情况
        bar = (
            Bar()
            .add_xaxis(list(expenditure_by_category['大类']))  # 将 Series 转换为列表
            .add_yaxis("支出", list(expenditure_by_category['金额']), label_opts=opts.LabelOpts(formatter="{c}元"))
            .set_global_opts(title_opts=opts.TitleOpts(title="月支出情况"))
        )

        # 渲染图表
        print(f'渲染图表导出')
        pie.render("expenditure_pie.html")
        bar.render("expenditure_bar.html")
'''