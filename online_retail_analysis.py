# 本脚本由 online_retail_analysis.ipynb 中的封装过程AI辅助封装而成
# 原作者：贺庄
# 功能：加载电商数据，清洗后按国家统计平均消费和购买次数，并绘制柱状图+饼图
# 原始分析过程和详细注释请见同目录下的 onlne_retail_analysis.ipynb
import matplotlib.pyplot as plt
import pandas as pd
from mpl_toolkits.axes_grid1.mpl_axes import Axes

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False


def load_and_clean_data(filepath: str) -> pd.DataFrame:

    dt = pd.read_csv(filepath)

    # 去除缺失值
    dt = dt.dropna()
    dt['CustomerID'] = dt['CustomerID'].astype(int)

    # UnitPrice：去负 + 箱线去异常
    dt = dt.drop(dt[dt['UnitPrice'] < 0].index)
    q1 = dt['UnitPrice'].quantile(0.25)
    q3 = dt['UnitPrice'].quantile(0.75)
    iqr = q3 - q1
    upper = q3 + 1.5 * iqr
    lower = q3 - 1.5 * iqr
    high_out = dt[dt['UnitPrice'] > upper]
    low_out = dt[dt['UnitPrice'] < lower]
    dt = dt.drop(high_out.index)
    dt = dt.drop(low_out.index)

    # Quantity：去负 + 去上异常
    dt = dt.drop(dt[dt['Quantity'] < 0].index)
    d1 = dt['Quantity'].quantile(0.25)
    d3 = dt['Quantity'].quantile(0.75)
    iqr = d3 - d1
    upper = d3 + 1.5 * iqr
    high_out = dt[dt['Quantity'] > upper]
    dt = dt.drop(high_out.index)

    # 日期转换
    dt['InvoiceDate_converted'] = pd.to_datetime(dt['InvoiceDate'], errors='coerce')

    return dt


def aggregate_by_country(dt: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:

    c_m = dt.groupby('Country')['UnitPrice'].agg(['sum', 'mean'])  # 总额、平均
    c_c = dt.groupby('Country')['Country'].count()                  # 次数
    return c_m, c_c



def plot_country_analysis(c_m: pd.DataFrame, c_c: pd.Series, threshold: float = 0.05):
    figure, axes = plt.subplots(nrows=1, ncols=2, figsize=(16, 6))
    axes1: Axes = axes[0]
    axes2: Axes = axes[1]

    # -------- 左图：平均消费柱状图 --------
    x_countries = c_m.index.tolist()
    x_average_pay = c_m['mean'].tolist()

    axes1.bar(x_countries, x_average_pay, color='blue', width=0.4)
    axes1.set_title('不同国家平均消费')
    axes1.set_xlabel('国家')
    axes1.set_ylabel('平均花费')
    axes1.tick_params(axis='x', rotation=90, labelsize=9)
    axes1.grid(linestyle='-', linewidth=0.2, alpha=1)

    # -------- 右图：网购次数饼图（小比例合并为“其他”） --------
    total = c_c.sum()
    large_c = c_c.loc[c_c >= total * threshold]
    small_c = c_c.loc[c_c < total * threshold]

    if small_c.shape[0] > 0:
        large_c['其他'] = small_c.sum()

    x1_countries = large_c.index.tolist()
    y1_cou = large_c.values.tolist()

    axes2.pie(y1_cou, labels=x1_countries, autopct='%1.1f%%', shadow=False, startangle=90)
    axes2.set_title('各国之间网购次数对比')
    axes2.legend()

    plt.tight_layout()
    plt.show()


# ---------------------- 主函数：一键执行 ----------------------
def main():
    """主入口：改这里的文件路径即可"""
    csv_path = "data.csv"   # 你的数据文件
    dt = load_and_clean_data(csv_path)
    c_m, c_c = aggregate_by_country(dt)
    plot_country_analysis(c_m, c_c, threshold=0.05)


if __name__ == "__main__":
    main()
