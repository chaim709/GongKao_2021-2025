#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
资料分析题型深度分析系统
作者: 行测考试研究专家
功能: 对2021-2025年江苏省考资料分析真题进行系统性分析
"""

import json
import re
from collections import defaultdict, Counter
from typing import Dict, List, Any

class ZiLiaoAnalyzer:
    """资料分析题型分析器"""

    def __init__(self, json_path: str):
        self.json_path = json_path
        self.data = []
        self.load_data()

    def load_data(self):
        """加载JSON数据"""
        with open(self.json_path, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
        print(f"已加载 {len(self.data)} 道题目")

    def identify_question_type(self, item: Dict) -> str:
        """
        题型识别: 一眼看出是什么题、用什么方法
        资料分析常见题型:
        1. 增长量计算 2. 增长率计算
        3. 基期量计算
        4. 现期量计算
        5. 比重计算
        6. 平均数计算
        7. 倍数计算
        8. 年均增长
        9. 隔年增长
        10. 综合分析
        11. 图表分析
        """
        question = item.get('题干', '')
        analysis = item.get('解析', '')

        # 综合分析题(通常是最后一题)
        if re.search(r'(能够.*推出|不能.*推出|正确的是|错误的是)', question):
            return "综合分析题"

        # 图表分析题
        if '饼图' in question or '柱状图' in question or '折线图' in question or 'jpg' in question.lower():
            return "图表分析题"

        # 年均增长题
        if re.search(r'年均增长|年均增速', question) or '年均增长' in analysis:
            return "年均增长计算"

        # 隔年增长题
        if re.search(r'隔年增长|比.*年.*增长', question):
            return "隔年增长计算"

        # 增长量题
        if re.search(r'增加.*元|增加.*个|增加.*人|增长.*百分点|增长.*元|增长.*个|增长量', question):
            if '百分点' in question:
                return "增长量计算(百分点)"
            return "增长量计算"

        # 增长率题
        if re.search(r'增长率|增速|增幅|同比增长.*%', question):
            return "增长率计算"

        # 基期量题
        if re.search(r'上年|去年|.*年.*为', question) and '增长' in analysis:
            return "基期量计算"

        # 比重题
        if re.search(r'占.*比重|占比|所占.*%|比例|份额', question):
            if re.search(r'比重.*变化|比重.*上升|比重.*下降', question):
                return "比重变化计算"
            return "比重计算"

        # 平均数题
        if re.search(r'平均|人均|每', question):
            if re.search(r'平均.*增长|人均.*增长', question):
                return "平均数增长率计算"
            return "平均数计算"

        # 倍数题
        if re.search(r'倍|是.*的.*倍', question):
            return "倍数计算"

        # 比较题
        if re.search(r'最大|最小|最多|最少|最高|最低|排序|排名', question):
            return "数据比较题"

        # 现期量计算
        if re.search(r'为多少|是多少|达到|共有', question):
            return "现期量计算"

        return "其他类型"

    def identify_exam_content(self, item: Dict, question_type: str) -> str:
        """
        考察内容: 理解为什么这么考、考什么思维、命题人考察的能力
        """
        exam_content_map = {
            "增长量计算": "考察考生对增长概念的理解和计算能力,要求快速识别现期量和增长率,运用公式计算增长量。核心能力:数据定位、公式应用、估算技巧",
            "增长量计算(百分点)": "考察考生对百分点概念的理解,区分百分点与百分数的差异。核心能力:概念辨析、直接做差运算",
            "增长率计算": "考察考生对增长率公式的掌握和逆向思维能力,要求从现期量和基期量反推增长率。核心能力:公式变形、估算能力",
            "基期量计算": "考察考生的逆向计算能力,要求从现期量和增长率反推基期量。核心能力:公式逆推、分母估算",
            "现期量计算": "考察考生对资料的理解和数据提取能力,要求准确找到题目所需数据。核心能力:材料理解、数据定位",
            "比重计算": "考察考生对比重概念的理解,要求识别部分量和整体量的关系。核心能力:关系识别、除法估算",
            "比重变化计算": "考察考生对比重变化公式的理解,需要判断比重上升还是下降。核心能力:复合公式应用、增长率比较",
            "平均数计算": "考察考生对平均数概念的理解和计算能力。核心能力:总量与份数识别、除法运算",
            "平均数增长率计算": "考察考生对平均数增长率公式的掌握,属于复合型考点。核心能力:复合公式应用、多步骤计算",
            "倍数计算": "考察考生对倍数关系的理解和计算能力。核心能力:除法运算、数量级判断",
            "年均增长计算": "考察考生对年均增长率概念的理解和复利计算能力。核心能力:指数运算、估算技巧",
            "隔年增长计算": "考察考生对隔年增长公式的掌握和复合增长率的理解。核心能力:复合公式应用、乘积估算",
            "数据比较题": "考察考生的快速比较能力和估算技巧,要求在短时间内完成多组数据比较。核心能力:估算技巧、排除法",
            "图表分析题": "考察考生的图表阅读能力和数据敏感度,要求快速从图表中提取关键信息。核心能力:图表理解、数据提取、逻辑推理",
            "综合分析题": "考察考生的综合运用能力,要求对多个选项逐一验证,综合运用各类公式。核心能力:多公式综合应用、选项排查、时间管理",
            "其他类型": "考察考生的综合分析能力和灵活应变能力"
        }
        return exam_content_map.get(question_type, "考察数据分析与计算能力")

    def identify_thinking_method(self, item: Dict, question_type: str) -> str:
        """
        思维方式: 哪种思维方式更快、更稳定
        """
        thinking_map = {
            "增长量计算": "优先判断数量级→观察增长率大小→选择合适估算方法(n+1原则/特征数字法/百化分)",
            "增长量计算(百分点)": "直接做差思维→无需计算基期→看清单位(百分点vs百分数)",
            "增长率计算": "观察选项差距→选择估算精度→优先使用特征数字法或截位直除",
            "基期量计算": "观察增长率特征→选择分母处理方式(直除/化除为乘/特征数字)→注意数量级",
            "现期量计算": "精准定位材料→识别陷阱(时间/单位/范围)→直接读数或简单加减",
            "比重计算": "识别部分与整体→优先看数量级→选择除法估算方法(首位法/截位直除)",
            "比重变化计算": "优先判断升降(比较部分增长率与整体增长率)→若需精确计算再用公式→观察选项差距",
            "平均数计算": "识别总量和份数→观察选项差距→选择合适除法估算",
            "平均数增长率计算": "优先记忆公式结构→分子分母分别识别→估算时注意符号",
            "倍数计算": "直接除法思维→观察数量级→注意倍数与百分数的转换",
            "年均增长计算": "识别时间跨度→判断是否需要'翻旧账'→选择合适估算方法(开方/特征数字)",
            "隔年增长计算": "记忆公式q1+q2+q1×q2→观察增长率大小→估算乘积项是否可忽略",
            "数据比较题": "优先比较数量级→其次比较首位→灵活运用差分法/估算法→快速排除",
            "图表分析题": "快速浏览图表→识别关键信息(最大最小/趋势/占比)→结合文字材料验证",
            "综合分析题": "优先做确定性高的选项→运用排除法→注意时间管理(单个选项不超过30秒)"
        }
        return thinking_map.get(question_type, "结合材料,灵活运用估算技巧")

    def identify_solution_method(self, item: Dict, question_type: str) -> str:
        """
        解题方法: 用什么解题方法
        """
        analysis = item.get('解析', '')

        # 从解析中提取实际使用的方法
        methods = []

        if '十字交叉' in analysis:
            methods.append('十字交叉法')
        if 'n+1' in analysis or 'N+1' in analysis:
            methods.append('n+1原则')
        if '截位' in analysis or '直除' in analysis:
            methods.append('截位直除法')
        if '特征数字' in analysis:
            methods.append('特征数字法')
        if '百化分' in analysis:
            methods.append('百化分')
        if '差分法' in analysis:
            methods.append('差分法')
        if '首数法' in analysis:
            methods.append('首数法')
        if '尾数法' in analysis:
            methods.append('尾数法')
        if '排除法' in analysis:
            methods.append('排除法')
        if '估算' in analysis:
            methods.append('估算法')

        # 根据题型补充常用方法
        type_method_map = {
            "增长量计算": "公式法(增长量=现期量-基期量=现期量×r/(1+r))、n+1原则、特征数字法",
            "增长量计算(百分点)": "直接做差法",
            "增长率计算": "公式法(r=(现期量-基期量)/基期量)、截位直除法、特征数字法",
            "基期量计算": "公式法(基期量=现期量/(1+r))、化除为乘、特征数字法",
            "现期量计算": "直接查找法、简单加减法",
            "比重计算": "公式法(比重=部分/整体)、截位直除法、首数法",
            "比重变化计算": "增长率比较法、公式法(比重变化=现期比重×(部分增长率-整体增长率)/(1+整体增长率))",
            "平均数计算": "公式法(平均数=总量/份数)、截位直除法",
            "平均数增长率计算": "公式法(平均数增长率=(总量增长率-份数增长率)/(1+份数增长率))",
            "倍数计算": "除法直算、数量级判断",
            "年均增长计算": "公式法(末期=初期×(1+年均增长率)^n)、开方法、特征数字法",
            "隔年增长计算": "公式法(隔年增长率=q1+q2+q1×q2)、乘积估算",
            "数据比较题": "估算法、首数法、差分法、排除法",
            "图表分析题": "图表读数法、趋势分析法、排除法",
            "综合分析题": "逐项验证法、排除法、快速估算"
        }

        base_method = type_method_map.get(question_type, "综合运用各类方法")

        if methods:
            return f"{base_method} [本题实际使用: {'+'.join(methods)}]"
        else:
            return base_method

    def analyze_all_questions(self):
        """分析所有题目,添加新字段"""
        print("\n开始逐题深度分析...")
        for i, item in enumerate(self.data, 1):
            # 识别题型
            question_type = self.identify_question_type(item)
            item['题型识别'] = question_type

            # 识别考察内容
            exam_content = self.identify_exam_content(item, question_type)
            item['考察内容'] = exam_content

            # 识别思维方式
            thinking = self.identify_thinking_method(item, question_type)
            item['思维方式'] = thinking

            # 识别解题方法
            solution = self.identify_solution_method(item, question_type)
            item['解题方法'] = solution

            if i % 20 == 0:
                print(f"已分析 {i}/{len(self.data)} 道题目...")

        print(f"✓ 完成全部 {len(self.data)} 道题目的深度分析")

    def save_enriched_json(self):
        """保存增强后的JSON"""
        output_path = self.json_path.replace('.json', '_增强版.json')
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
        print(f"✓ 已保存增强版JSON: {output_path}")
        return output_path

    def generate_frequency_table(self) -> str:
        """生成题型频率统计表"""
        print("\n生成题型频率统计...")

        stats_by_year = defaultdict(lambda: defaultdict(list))
        stats_overall = defaultdict(list)

        for item in self.data:
            year = item.get('年份', 'Unknown')
            qtype = item.get('题型识别', '未识别')
            uid = item.get('UID', '')
            qnum = item.get('题目编号', '')

            stats_by_year[year][qtype].append({'UID': uid, '题号': qnum})
            stats_overall[qtype].append({'UID': uid, '题号': qnum, '年份': year})

        md_content = "# 资料分析题型频率统计表\n\n"
        md_content += "## 一、分年度题型分布\n\n"

        # 按年份统计
        for year in sorted(stats_by_year.keys()):
            md_content += f"### {year}年\n\n"
            md_content += "| 题型 | 数量 | 题号列表 | UID列表 |\n"
            md_content += "|------|------|----------|----------|\n"

            year_data = stats_by_year[year]
            for qtype in sorted(year_data.keys(), key=lambda x: len(year_data[x]), reverse=True):
                items = year_data[qtype]
                count = len(items)
                qnums = ', '.join([str(item['题号']) for item in items])
                uids = ', '.join([item['UID'] for item in items])
                md_content += f"| {qtype} | {count} | {qnums} | {uids} |\n"

            md_content += "\n"

        # 总体统计
        md_content += "## 二、五年总体题型分布\n\n"
        md_content += "| 题型 | 总数 | 占比 | 出现年份 | 高频年份 |\n"
        md_content += "|------|------|------|----------|----------|\n"

        total_count = len(self.data)
        for qtype in sorted(stats_overall.keys(), key=lambda x: len(stats_overall[x]), reverse=True):
            items = stats_overall[qtype]
            count = len(items)
            percentage = f"{count/total_count*100:.1f}%"

            years = [item['年份'] for item in items]
            year_counter = Counter(years)
            unique_years = ', '.join(sorted(set(years)))
            high_freq_years = ', '.join([f"{y}({c}题)" for y, c in year_counter.most_common(2)])

            md_content += f"| {qtype} | {count} | {percentage} | {unique_years} | {high_freq_years} |\n"

        # 详细清单
        md_content += "\n## 三、题型详细清单\n\n"
        for qtype in sorted(stats_overall.keys()):
            md_content += f"### {qtype}\n\n"
            md_content += "| 年份 | 题号 | UID | 题干摘要 |\n"
            md_content += "|------|------|-----|----------|\n"

            for item_ref in stats_overall[qtype]:
                # 找到完整题目信息
                full_item = next((x for x in self.data if x['UID'] == item_ref['UID']), None)
                if full_item:
                    question = full_item.get('题干', '')[:50] + '...' if len(full_item.get('题干', '')) > 50 else full_item.get('题干', '')
                    question = question.replace('\n', ' ').replace('|', '│')
                    md_content += f"| {item_ref['年份']} | {item_ref['题号']} | {item_ref['UID']} | {question} |\n"

            md_content += "\n"

        return md_content

    def generate_technique_mapping(self) -> str:
        """生成技巧映射表"""
        print("\n生成技巧映射表...")

        md_content = "# 资料分析技巧映射表\n\n"
        md_content += "## 核心理念:看到题目→识别题型→触发技巧→快速作答\n\n"

        technique_map = {
            "增长量计算": {
                "识别关键词": "增加、增长、多了、增长量",
                "触发条件": "题目问增加/增长了多少(绝对量)",
                "核心技巧": "①优先看选项数量级判断是否需要精算 ②增长率<5%用直接减法 ③增长率>5%用n+1原则或公式法",
                "秒杀技巧": "n+1原则:增长率化为1/n形式,增长量≈现期量/(n+1)",
                "常用公式": "增长量=现期量×r/(1+r) 或 增长量=基期量×r",
                "注意事项": "区分增长量与增长率,注意单位统一"
            },
            "增长量计算(百分点)": {
                "识别关键词": "百分点、个百分点",
                "触发条件": "题目出现'百分点'三个字",
                "核心技巧": "直接做差,无需任何计算",
                "秒杀技巧": "百分点=直接相减,不需要除以基期",
                "常用公式": "百分点差=A%-B%",
                "注意事项": "百分点≠百分数,不要多此一举计算"
            },
            "增长率计算": {
                "识别关键词": "增长率、增速、增幅、同比增长",
                "触发条件": "题目问增长百分之几",
                "核心技巧": "①观察选项差距选精度 ②截位直除法(保留前2-3位) ③特征数字法",
                "秒杀技巧": "选项差距大用首位法,差距小用截位直除",
                "常用公式": "增长率=(现期-基期)/基期×100%",
                "注意事项": "注意负增长(下降)的情况"
            },
            "基期量计算": {
                "识别关键词": "上年、去年、基期",
                "触发条件": "已知现期量和增长率,求过去的量",
                "核心技巧": "①观察增长率特征 ②选择分母处理方式 ③特征数字法最优",
                "秒杀技巧": "增长率化为特征分数,如25%=1/4,则基期=现期×4/5",
                "常用公式": "基期=现期/(1+r)",
                "注意事项": "分母是(1+r)不是r,注意下降时r为负"
            },
            "比重计算": {
                "识别关键词": "占、比重、占比、比例、份额",
                "触发条件": "题目问某部分占整体的百分之几",
                "核心技巧": "①识别部分与整体 ②截位直除法 ③首数法",
                "秒杀技巧": "选项首位不同只算第一位,相同算两位",
                "常用公式": "比重=部分/整体×100%",
                "注意事项": "部分一定小于整体,比重<100%"
            },
            "比重变化计算": {
                "识别关键词": "比重上升、比重下降、比重变化",
                "触发条件": "题目问比重变化了多少或升降",
                "核心技巧": "①先判断升降:部分增长率>整体增长率则上升 ②若需精确计算再用公式",
                "秒杀技巧": "判断升降后直接排除2个选项,剩余选项估算",
                "常用公式": "比重变化=现期比重-基期比重",
                "注意事项": "比重变化单位是百分点,不是百分数"
            },
            "平均数计算": {
                "识别关键词": "平均、人均、每、单位",
                "触发条件": "题目问平均每个/每人/单位多少",
                "核心技巧": "①识别总量和份数 ②截位直除 ③首数法",
                "秒杀技巧": "观察选项数量级,确定计算精度",
                "常用公式": "平均数=总量/份数",
                "注意事项": "单位要统一(如万人与人)"
            },
            "年均增长计算": {
                "识别关键词": "年均增长、年均增速",
                "触发条件": "题目出现'年均'二字",
                "核心技巧": "①江苏省考需要'翻旧账' ②开方估算 ③特征数字法",
                "秒杀技巧": "n年增长m倍,年均增长率≈m/n(粗略估算)",
                "常用公式": "末期=初期×(1+r)^n",
                "注意事项": "注意时间跨度n的计算,江苏省考'翻旧账'"
            },
            "隔年增长计算": {
                "识别关键词": "比某某年增长",
                "触发条件": "跨越一年的增长",
                "核心技巧": "①记住公式q1+q2+q1×q2 ②观察q1×q2是否可忽略",
                "秒杀技巧": "两个增长率都较小(<10%)时,q1×q2可忽略",
                "常用公式": "隔年增长率=q1+q2+q1×q2",
                "注意事项": "注意q1、q2的正负号"
            },
            "数据比较题": {
                "识别关键词": "最大、最小、最多、最少、排序",
                "触发条件": "题目要求比较多个数据大小",
                "核心技巧": "①数量级比较 ②首位比较 ③差分法",
                "秒杀技巧": "优先排除数量级明显不同的选项",
                "常用公式": "差分法:A/B与C/D比较,看(A-C)/(B-D)与A/B大小关系",
                "注意事项": "不要精算每个选项,用排除法"
            },
            "图表分析题": {
                "识别关键词": "饼图、柱状图、折线图",
                "触发条件": "题目含图表",
                "核心技巧": "①快速浏览图表关键信息 ②识别最大最小值 ③观察趋势",
                "秒杀技巧": "图表题优先排除法,无需精算",
                "常用公式": "结合图表数据与文字材料",
                "注意事项": "注意单位、图例、时间轴"
            },
            "综合分析题": {
                "识别关键词": "能够推出、不能推出、正确的是",
                "触发条件": "题目要求判断4个选项",
                "核心技巧": "①优先做确定性选项 ②排除法 ③单个选项限时30秒",
                "秒杀技巧": "优先看选项中有明显错误的(时间、概念、数量级)",
                "常用公式": "综合运用各类公式",
                "注意事项": "注意时间管理,不要在一个选项上耗费过多时间"
            }
        }

        # 生成表格
        md_content += "| 题型 | 识别关键词 | 触发条件 | 核心技巧 | 秒杀技巧 |\n"
        md_content += "|------|-----------|----------|----------|----------|\n"

        for qtype, info in technique_map.items():
            keywords = info['识别关键词']
            trigger = info['触发条件']
            technique = info['核心技巧']
            quick = info['秒杀技巧']
            md_content += f"| {qtype} | {keywords} | {trigger} | {technique} | {quick} |\n"

        # 详细说明
        md_content += "\n## 详细技巧说明\n\n"
        for qtype, info in technique_map.items():
            md_content += f"### {qtype}\n\n"
            md_content += f"**识别关键词**: {info['识别关键词']}\n\n"
            md_content += f"**触发条件**: {info['触发条件']}\n\n"
            md_content += f"**核心技巧**: {info['核心技巧']}\n\n"
            md_content += f"**秒杀技巧**: {info['秒杀技巧']}\n\n"
            md_content += f"**常用公式**: {info['常用公式']}\n\n"
            md_content += f"**注意事项**: {info['注意事项']}\n\n"
            md_content += "---\n\n"

        return md_content

    def generate_keyword_stats(self) -> str:
        """生成题干关键词统计"""
        print("\n生成关键词统计...")

        md_content = "# 资料分析题干关键词统计\n\n"

        # 统计关键词
        keywords_counter = Counter()
        action_words = Counter()

        key_patterns = [
            r'增长', r'增加', r'增速', r'增幅',
            r'比重', r'占比', r'比例', r'份额',
            r'平均', r'人均',
            r'最[大多少高低小]',
            r'同比', r'环比',
            r'百分点',
            r'倍',
            r'年均',
            r'基期', r'现期',
            r'上年', r'去年', r'当年'
        ]

        for item in self.data:
            question = item.get('题干', '')
            for pattern in key_patterns:
                matches = re.findall(pattern, question)
                keywords_counter.update(matches)

            # 提取疑问词
            if '多少' in question:
                action_words['计算数值'] += 1
            if any(x in question for x in ['是否', '能否', '正确', '错误']):
                action_words['判断正误'] += 1
            if any(x in question for x in ['最大', '最小', '最多', '最少']):
                action_words['比较大小'] += 1

        md_content += "## 一、高频关键词TOP20\n\n"
        md_content += "| 排名 | 关键词 | 出现次数 | 占比 |\n"
        md_content += "|------|--------|----------|------|\n"

        total = len(self.data)
        for i, (word, count) in enumerate(keywords_counter.most_common(20), 1):
            percentage = f"{count/total*100:.1f}%"
            md_content += f"| {i} | {word} | {count} | {percentage} |\n"

        md_content += "\n## 二、题目行为类型\n\n"
        md_content += "| 行为类型 | 数量 | 占比 |\n"
        md_content += "|----------|------|------|\n"

        for action, count in action_words.most_common():
            percentage = f"{count/total*100:.1f}%"
            md_content += f"| {action} | {count} | {percentage} |\n"

        # 按题型统计关键词
        md_content += "\n## 三、分题型关键词分布\n\n"

        type_keywords = defaultdict(Counter)
        for item in self.data:
            qtype = item.get('题型识别', '未识别')
            question = item.get('题干', '')
            for pattern in key_patterns:
                matches = re.findall(pattern, question)
                type_keywords[qtype].update(matches)

        for qtype in sorted(type_keywords.keys()):
            md_content += f"### {qtype}\n\n"
            md_content += "| 关键词 | 出现次数 |\n"
            md_content += "|--------|----------|\n"
            for word, count in type_keywords[qtype].most_common(10):
                md_content += f"| {word} | {count} |\n"
            md_content += "\n"

        return md_content

    def generate_solution_templates(self) -> str:
        """生成解题模板库"""
        print("\n生成解题模板库...")

        md_content = "# 资料分析解题模板库\n\n"
        md_content += "> 考场速用版:看到题目→套用模板→快速作答\n\n"

        templates = {
            "增长量计算": {
                "识别": "题目问'增加了多少'、'增长量'",
                "思路": "定位数据→判断数量级→选择方法→计算",
                "模板": """
**Step1**: 定位现期量和增长率
**Step2**: 观察选项数量级差异
**Step3**: 选择计算方法:
  - 选项差距大: 估算法
  - 增长率<5%: 直接减法
  - 增长率>5%: n+1原则
**Step4**: 快速计算并选择

**公式**: 增长量 = 现期量 × r/(1+r)
**n+1速算**: 增长率=1/n,则增长量≈现期量/(n+1)
**示例**: 增长率25%=1/4,增长量≈现期量/5
                """,
                "注意": "①单位统一 ②区分增长量与增长率 ③注意负增长"
            },
            "增长率计算": {
                "识别": "题目问'增长百分之几'、'增长率'、'增幅'",
                "思路": "定位现期和基期→观察选项→选择除法方法→计算",
                "模板": """
**Step1**: 定位现期量和基期量
**Step2**: 观察选项首位差异
**Step3**: 选择计算方法:
  - 首位不同: 首位法
  - 首位相同: 截位直除(保留2-3位)
**Step4**: 计算(现期-基期)/基期

**公式**: r = (现期-基期)/基期 × 100%
**速算技巧**: 选项差距大时只算首位
**示例**: 1234/5678,首位不同时算1/5=20%即可
                """,
                "注意": "①负增长是下降 ②百分数不要忘记 ③看清是否求增长率差值"
            },
            "基期量计算": {
                "识别": "题目问'上年'、'去年'的数据",
                "思路": "定位现期量和增长率→转化增长率→除法计算",
                "模板": """
**Step1**: 定位现期量和增长率
**Step2**: 观察增长率是否为特征数字
**Step3**: 选择计算方法:
  - 特征数字: 化为分数计算
  - 非特征: 截位直除
**Step4**: 计算现期/(1+r)

**公式**: 基期 = 现期/(1+r)
**特征数字法**: 25%=1/4,则基期=现期×4/5
**示例**: 现期120,增长率25%,基期=120×4/5=96
                """,
                "注意": "①分母是(1+r)不是r ②下降时r为负 ③注意数量级"
            },
            "比重计算": {
                "识别": "题目问'占比'、'比重'、'比例'",
                "思路": "定位部分量和整体量→除法计算",
                "模板": """
**Step1**: 识别部分量和整体量
**Step2**: 观察选项首位差异
**Step3**: 截位直除:
  - 首位不同: 保留1位
  - 首位相同: 保留2位
**Step4**: 计算部分/整体

**公式**: 比重 = 部分/整体 × 100%
**速算**: 选项首位不同只算第一位
**验证**: 比重一定<100%
                """,
                "注意": "①部分<整体 ②单位统一 ③比重<100%"
            },
            "比重变化": {
                "识别": "题目问'比重上升/下降'、'比重变化'",
                "思路": "先判断升降→再计算变化量",
                "模板": """
**Step1**: 定位部分增长率和整体增长率
**Step2**: 比较大小判断升降:
  - 部分>整体: 比重上升
  - 部分<整体: 比重下降
**Step3**: 若需精确计算,用公式
**Step4**: 排除错误选项

**判断口诀**: 部分快则比重升,部分慢则比重降
**精确公式**: 比重变化 = 现期比重 × (部分增长率-整体增长率)/(1+整体增长率)
**秒杀**: 多数题判断升降即可排除2个选项
                """,
                "注意": "①比重变化单位是百分点 ②升降判断是核心 ③变化量通常很小"
            },
            "平均数计算": {
                "识别": "题目问'平均'、'人均'、'每'",
                "思路": "定位总量和份数→除法计算",
                "模板": """
**Step1**: 定位总量和份数
**Step2**: 单位统一
**Step3**: 截位直除
**Step4**: 选择答案

**公式**: 平均数 = 总量/份数
**速算**: 观察选项差距确定精度
**验证**: 平均数应介于最大最小之间
                """,
                "注意": "①单位统一 ②总量和份数对应 ③注意倍数关系"
            },
            "年均增长": {
                "识别": "题目出现'年均增长'、'年均增速'",
                "思路": "识别时间跨度→套用公式→估算",
                "模板": """
**Step1**: 确定起止时间,计算跨度n
**Step2**: 江苏省考判断是否需要'翻旧账'
**Step3**: 套用公式计算
**Step4**: 开方估算或特征数字

**公式**: 末期 = 初期 × (1+r)^n
**江苏特色**: 2001-2019年指从2000年末到2019年末
**估算技巧**: n年m倍,年均增长率≈m/n(粗算)
                """,
                "注意": "①江苏省考翻旧账 ②n的计算要准确 ③估算时开方"
            },
            "隔年增长": {
                "识别": "题目问'比某某年增长'(跨年)",
                "思路": "识别两个增长率→套用公式→估算乘积项",
                "模板": """
**Step1**: 定位连续两年的增长率q1、q2
**Step2**: 套用公式 q1+q2+q1×q2
**Step3**: 判断q1×q2是否可忽略:
  - 都<10%: 可忽略
  - 有一个>10%: 需计算
**Step4**: 计算并选择

**公式**: 隔年增长率 = q1 + q2 + q1×q2
**速算**: q1、q2都较小时,q1×q2可忽略
**示例**: q1=5%, q2=6%, 隔年≈11%(忽略0.3%)
                """,
                "注意": "①两个增长率的正负 ②乘积项是否可忽略 ③单位是百分数"
            },
            "数据比较": {
                "识别": "题目要求比较'最大'、'最小'、'排序'",
                "思路": "不要全算→逐步排除→确定答案",
                "模板": """
**Step1**: 定位所有待比较数据
**Step2**: 数量级比较,排除明显不对的
**Step3**: 首位比较,进一步排除
**Step4**: 剩余项精确比较(差分法)

**技巧**:
  - 优先比较数量级
  - 其次比较首位
  - 差分法: A/B vs C/D → (A-C)/(B-D)
**秒杀**: 不要每项都算
                """,
                "注意": "①排除法是核心 ②不要精算每项 ③注意单位"
            },
            "综合分析": {
                "识别": "题目要求判断4个选项正误",
                "思路": "优先做确定性选项→排除法→时间控制",
                "模板": """
**Step1**: 快速浏览4个选项
**Step2**: 优先做确定性选项(一眼看出对错的)
**Step3**: 运用排除法,找到答案
**Step4**: 时间控制,单个选项≤30秒

**技巧**:
  - 优先看时间、概念、数量级错误
  - 计算复杂的选项留到最后
  - 找到答案后其他选项不用算
**秒杀**: 找明显错误选项
                """,
                "注意": "①时间管理最重要 ②不要每个选项都精算 ③排除法优先"
            }
        }

        for qtype, template in templates.items():
            md_content += f"## {qtype}\n\n"
            md_content += f"### 🔍 题型识别\n{template['识别']}\n\n"
            md_content += f"### 💡 解题思路\n{template['思路']}\n\n"
            md_content += f"### 📋 解题模板\n{template['模板']}\n\n"
            md_content += f"### ⚠️ 注意事项\n{template['注意']}\n\n"
            md_content += "---\n\n"

        return md_content

    def generate_traps_and_tips(self) -> str:
        """生成常见陷阱与高分技巧"""
        print("\n生成常见陷阱与高分技巧...")

        md_content = "# 资料分析常见陷阱与高分技巧\n\n"

        # 统计实际出现的陷阱
        traps_counter = defaultdict(list)

        for item in self.data:
            question = item.get('题干', '')
            analysis = item.get('解析', '')
            qtype = item.get('题型识别', '')
            uid = item.get('UID', '')

            # 识别陷阱
            if '注意' in analysis or '易错' in analysis:
                traps_counter[qtype].append(uid)

        md_content += "## 一、分题型陷阱与技巧总表\n\n"
        md_content += "| 题型 | 识别关键词 | 常见陷阱 | 高分技巧 | 易错点数量 |\n"
        md_content += "|------|-----------|----------|----------|------------|\n"

        traps_tips = {
            "增长量计算": {
                "识别": "增加、增长量",
                "陷阱": "①混淆增长量与增长率 ②单位不统一(万/亿) ③负增长当正增长",
                "技巧": "n+1原则秒杀,增长率<5%直接减法"
            },
            "增长量计算(百分点)": {
                "识别": "百分点",
                "陷阱": "①混淆百分点与百分数 ②多此一举除以基期",
                "技巧": "看到百分点直接做差,0秒出答案"
            },
            "增长率计算": {
                "识别": "增长率、增幅、增速",
                "陷阱": "①看错现期基期 ②忘记×100% ③下降当增长",
                "技巧": "截位直除法,选项首位不同只算一位"
            },
            "基期量计算": {
                "识别": "上年、去年、基期",
                "陷阱": "①分母用r而不是(1+r) ②下降时r符号错误 ③数量级错误",
                "技巧": "特征数字法最快,25%=1/4记住常用转换"
            },
            "比重计算": {
                "识别": "占、比重、比例",
                "陷阱": "①部分整体搞反 ②单位不统一 ③比重>100%",
                "技巧": "截位直除,首位法秒杀"
            },
            "比重变化": {
                "识别": "比重上升/下降",
                "陷阱": "①混淆百分点和百分数 ②升降判断错误 ③用增长量变化判断比重变化",
                "技巧": "部分增长率>整体增长率→比重上升,判断升降直接排除2个选项"
            },
            "平均数计算": {
                "识别": "平均、人均、每",
                "陷阱": "①总量份数不对应 ②单位不统一(万人vs人) ③看错数据",
                "技巧": "截位直除,注意数量级"
            },
            "年均增长": {
                "识别": "年均增长、年均增速",
                "陷阱": "①时间跨度n算错 ②江苏省考不翻旧账 ③公式记错",
                "技巧": "江苏省考特色:2001-2019指从2000年末算起"
            },
            "隔年增长": {
                "识别": "比XX年增长",
                "陷阱": "①两个增长率找错 ②忘记乘积项 ③符号错误",
                "技巧": "q1、q2都<10%时,乘积项可忽略"
            },
            "数据比较": {
                "识别": "最大、最小、排序",
                "陷阱": "①每个都精算浪费时间 ②看错单位 ③计算错误",
                "技巧": "排除法,数量级→首位→差分法,逐步缩小范围"
            },
            "图表分析": {
                "识别": "饼图、柱状图、折线图",
                "陷阱": "①看错图例 ②单位看错 ③时间轴看反",
                "技巧": "先看图表关键信息,再看选项,用排除法"
            },
            "综合分析": {
                "识别": "能够推出、正确的是",
                "陷阱": "①时间陷阱(题目问2020年给的2019年数据) ②概念陷阱(增长量vs增长率) ③计算陷阱",
                "技巧": "优先看确定性选项,排除法,单个选项限时30秒"
            }
        }

        for qtype, info in traps_tips.items():
            trap_count = len(traps_counter.get(qtype, []))
            md_content += f"| {qtype} | {info['识别']} | {info['陷阱']} | {info['技巧']} | {trap_count} |\n"

        # 详细说明
        md_content += "\n## 二、详细陷阱分析与破解方法\n\n"

        for qtype, info in traps_tips.items():
            md_content += f"### {qtype}\n\n"
            md_content += f"**识别关键词**: {info['识别']}\n\n"
            md_content += f"#### 常见陷阱\n{info['陷阱']}\n\n"
            md_content += f"#### 高分技巧\n{info['技巧']}\n\n"

            # 如果有实际案例,列出来
            if qtype in traps_counter and traps_counter[qtype]:
                md_content += f"**真题案例**: {', '.join(traps_counter[qtype][:3])}\n\n"

            md_content += "---\n\n"

        # 通用高分技巧
        md_content += "\n## 三、资料分析通用高分技巧\n\n"
        md_content += """
### 1. 时间管理黄金法则
- **单题时间**: 简单题30秒,中等题60秒,难题90秒
- **材料阅读**: 不要通读,带着问题找数据
- **综合分析**: 最后做,单个选项限时30秒

### 2. 估算技巧优先级
1. **数量级判断**: 第一优先,可排除50%选项
2. **首位法**: 选项首位不同时使用
3. **特征数字法**: 记住常用转换(1/4=25%, 1/8=12.5%)
4. **截位直除**: 保留2-3位有效数字
5. **n+1原则**: 增长量计算的神器

### 3. 选项观察技巧
- 做题前先看选项差距
- 差距大(>10%): 估算即可
- 差距小(<5%): 需要精算
- 选项单位不同: 注意数量级陷阱

### 4. 材料阅读技巧
- **不要通读**: 浪费时间
- **看题找数**: 带着问题找数据
- **标注关键**: 在材料上标注时间、主体
- **注意单位**: 圈出单位,防止陷阱

### 5. 计算技巧
- **能估不算**: 估算优于精算
- **能除不乘**: 除法比乘法好估
- **能减不加**: 减法比加法简单
- **能比不算**: 比较比计算快

### 6. 排除法使用
- **时间陷阱**: 题目问2020年,选项给2019年数据
- **概念陷阱**: 增长量vs增长率,百分点vs百分数
- **数量级陷阱**: 万vs亿,人vs万人
- **常识陷阱**: 比重>100%,增长率>1000%

### 7. 常用速算公式
```
1. 增长量 = 现期×r/(1+r) ≈ 现期/(n+1)  [r=1/n]
2. 基期 = 现期/(1+r) = 现期×n/(n+1)    [r=1/n]
3. 增长率 = (现期-基期)/基期
4. 比重 = 部分/整体
5. 比重变化 = 现期比重-基期比重
6. 隔年增长率 = q1+q2+q1×q2
7. 平均数增长率 = (总量增长率-份数增长率)/(1+份数增长率)
```

### 8. 特征数字速记表
| 分数 | 百分数 | 小数 |
|------|--------|------|
| 1/2  | 50%    | 0.5  |
| 1/3  | 33.3%  | 0.33 |
| 1/4  | 25%    | 0.25 |
| 1/5  | 20%    | 0.2  |
| 1/6  | 16.7%  | 0.17 |
| 1/7  | 14.3%  | 0.14 |
| 1/8  | 12.5%  | 0.125|
| 1/9  | 11.1%  | 0.11 |
| 1/10 | 10%    | 0.1  |

### 9. 考场答题流程
```
看题→识别题型→观察选项→定位数据→选择方法→快速估算→排除选项→确定答案
(5秒) (3秒)   (5秒)   (10秒)  (5秒)   (20秒)  (5秒)   (2秒)
总计: 55秒/题
```

### 10. 江苏省考特色
- **年均增长需要"翻旧账"**: 2001-2019年指从2000年末算起
- **十字交叉法常用**: 平均数问题优先考虑
- **综合分析题常规**: 每篇材料最后一题
        """

        return md_content

    def generate_pattern_report(self) -> str:
        """生成命题规律报告"""
        print("\n生成命题规律报告...")

        md_content = "# 江苏省考资料分析命题规律报告(2021-2025)\n\n"
        md_content += f"> 基于{len(self.data)}道真题的深度分析\n\n"

        # 统计数据
        year_stats = defaultdict(lambda: defaultdict(int))
        year_total = defaultdict(int)
        type_trend = defaultdict(lambda: defaultdict(int))

        for item in self.data:
            year = item.get('年份', 'Unknown')
            qtype = item.get('题型识别', '未识别')
            year_stats[year][qtype] += 1
            year_total[year] += 1
            type_trend[qtype][year] += 1

        # 1. 每年模块比重
        md_content += "## 一、每年题量统计\n\n"
        md_content += "| 年份 | 题量 | 占五年总题量比重 |\n"
        md_content += "|------|------|------------------|\n"

        total_all = len(self.data)
        for year in sorted(year_total.keys()):
            count = year_total[year]
            percentage = f"{count/total_all*100:.1f}%"
            md_content += f"| {year} | {count} | {percentage} |\n"

        # 2. 题型占比
        md_content += "\n## 二、题型占比分析\n\n"
        md_content += "### 2.1 五年总体题型占比\n\n"

        type_total = defaultdict(int)
        for year_data in year_stats.values():
            for qtype, count in year_data.items():
                type_total[qtype] += count

        md_content += "| 题型 | 数量 | 占比 | 级别 |\n"
        md_content += "|------|------|------|------|\n"

        for qtype, count in sorted(type_total.items(), key=lambda x: x[1], reverse=True):
            percentage = f"{count/total_all*100:.1f}%"
            if count >= total_all * 0.15:
                level = "⭐⭐⭐ 超高频"
            elif count >= total_all * 0.10:
                level = "⭐⭐ 高频"
            elif count >= total_all * 0.05:
                level = "⭐ 中频"
            else:
                level = "低频"
            md_content += f"| {qtype} | {count} | {percentage} | {level} |\n"

        # 2.2 分年度题型占比
        md_content += "\n### 2.2 分年度题型占比\n\n"

        for year in sorted(year_stats.keys()):
            md_content += f"#### {year}年\n\n"
            md_content += "| 题型 | 数量 | 占比 |\n"
            md_content += "|------|------|------|\n"

            year_data = year_stats[year]
            year_sum = year_total[year]
            for qtype, count in sorted(year_data.items(), key=lambda x: x[1], reverse=True):
                percentage = f"{count/year_sum*100:.1f}%"
                md_content += f"| {qtype} | {count} | {percentage} |\n"
            md_content += "\n"

        # 3. 高频考点(≥3次)
        md_content += "\n## 三、高频考点分析(出现≥3次)\n\n"
        md_content += "| 题型 | 总数 | 频率 | 年均数量 | 必考指数 |\n"
        md_content += "|------|------|------|----------|----------|\n"

        num_years = len(year_total)
        high_freq_types = []

        for qtype, count in sorted(type_total.items(), key=lambda x: x[1], reverse=True):
            if count >= 3:
                avg_per_year = count / num_years
                must_test = "⭐⭐⭐ 必考" if avg_per_year >= 2 else "⭐⭐ 常考" if avg_per_year >= 1 else "⭐ 偶考"
                md_content += f"| {qtype} | {count} | {count}次/{num_years}年 | {avg_per_year:.1f}题/年 | {must_test} |\n"
                high_freq_types.append(qtype)

        # 4. 新趋势分析
        md_content += "\n## 四、命题趋势分析\n\n"

        # 计算每个题型的趋势
        trends = {}
        for qtype in type_total.keys():
            years = sorted(type_trend[qtype].keys())
            if len(years) >= 3:
                # 比较近两年与前两年的平均
                recent_avg = sum(type_trend[qtype].get(y, 0) for y in years[-2:]) / 2
                early_avg = sum(type_trend[qtype].get(y, 0) for y in years[:2]) / 2
                if early_avg > 0:
                    change = (recent_avg - early_avg) / early_avg
                    trends[qtype] = (change, recent_avg, early_avg)

        md_content += "### 4.1 上升趋势题型(近两年均值 > 前两年均值)\n\n"
        md_content += "| 题型 | 前两年均值 | 近两年均值 | 增幅 | 趋势 |\n"
        md_content += "|------|-----------|-----------|------|------|\n"

        rising = []
        for qtype, (change, recent, early) in sorted(trends.items(), key=lambda x: x[1][0], reverse=True):
            if change > 0:
                md_content += f"| {qtype} | {early:.1f} | {recent:.1f} | +{change*100:.0f}% | 📈 上升 |\n"
                rising.append(qtype)

        if not rising:
            md_content += "| - | - | - | - | 暂无明显上升趋势 |\n"

        md_content += "\n### 4.2 下降趋势题型(近两年均值 < 前两年均值)\n\n"
        md_content += "| 题型 | 前两年均值 | 近两年均值 | 降幅 | 趋势 |\n"
        md_content += "|------|-----------|-----------|------|------|\n"

        falling = []
        for qtype, (change, recent, early) in sorted(trends.items(), key=lambda x: x[1][0]):
            if change < 0:
                md_content += f"| {qtype} | {early:.1f} | {recent:.1f} | {change*100:.0f}% | 📉 下降 |\n"
                falling.append(qtype)

        if not falling:
            md_content += "| - | - | - | - | 暂无明显下降趋势 |\n"

        # 5. 命题规律总结
        md_content += "\n## 五、命题规律总结\n\n"
        md_content += "### 5.1 核心发现\n\n"

        top3_types = sorted(type_total.items(), key=lambda x: x[1], reverse=True)[:3]
        md_content += f"1. **题型分布**: 资料分析共{total_all}道题,平均每年{total_all/num_years:.0f}题\n"
        md_content += f"2. **高频三甲**: {top3_types[0][0]}({top3_types[0][1]}题)、{top3_types[1][0]}({top3_types[1][1]}题)、{top3_types[2][0]}({top3_types[2][1]}题)\n"
        md_content += f"3. **必考题型**: {len(high_freq_types)}种题型为高频考点(≥3次)\n"

        if rising:
            md_content += f"4. **上升趋势**: {', '.join(rising[:3])}等题型出现频率上升\n"
        if falling:
            md_content += f"5. **下降趋势**: {', '.join(falling[:3])}等题型出现频率下降\n"

        md_content += "\n### 5.2 备考建议\n\n"
        md_content += """
#### 重点题型(必须掌握)
"""
        for i, (qtype, count) in enumerate(top3_types, 1):
            md_content += f"{i}. **{qtype}**: 五年{count}题,必须熟练掌握\n"

        md_content += """
#### 常规题型(熟练掌握)
"""
        for qtype in high_freq_types[3:]:
            if type_total[qtype] >= 5:
                md_content += f"- **{qtype}**: 五年{type_total[qtype]}题,需要熟练\n"

        md_content += """
#### 新兴题型(关注趋势)
"""
        for qtype in rising[:3]:
            md_content += f"- **{qtype}**: 出现频率上升,需要关注\n"

        md_content += "\n### 5.3 江苏省考特色\n\n"
        md_content += """
1. **综合分析题必考**: 每篇材料最后一题通常是综合分析
2. **年均增长特殊处理**: 需要"翻旧账",注意时间计算
3. **十字交叉法高频**: 平均数相关问题常用十字交叉
4. **图表题占比稳定**: 每年都有图表分析题
5. **比重题型多样**: 比重计算、比重变化都是常考
        """

        md_content += "\n### 5.4 考场策略\n\n"
        md_content += """
1. **时间分配**: 20题60分钟,平均3分钟/题,实际应控制在2.5分钟
2. **做题顺序**: 先做简单题(现期量、百分点),再做计算题,最后做综合分析
3. **估算为主**: 80%的题目估算即可,不要过度精算
4. **排除法优先**: 综合分析题必用排除法
5. **材料不通读**: 带着问题找数据,节省时间
        """

        return md_content

    def save_all_reports(self):
        """保存所有报告"""
        print("\n开始生成所有分析报告...")

        reports = {
            "01_题型频率统计表.md": self.generate_frequency_table(),
            "02_技巧映射表.md": self.generate_technique_mapping(),
            "03_关键词统计报告.md": self.generate_keyword_stats(),
            "04_解题模板库.md": self.generate_solution_templates(),
            "05_常见陷阱与高分技巧.md": self.generate_traps_and_tips(),
            "06_命题规律报告.md": self.generate_pattern_report()
        }

        for filename, content in reports.items():
            filepath = f"/home/user/GongKao_2021-2025/资料分析_{filename}"
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ 已生成: {filename}")

        print(f"\n✓ 所有报告生成完成,共{len(reports)}个文件")

def main():
    print("="*60)
    print("资料分析题型深度分析系统")
    print("="*60)

    json_path = "/home/user/GongKao_2021-2025/2021-2025_资料分析_合并.json"

    # 初始化分析器
    analyzer = ZiLiaoAnalyzer(json_path)

    # 分析所有题目
    analyzer.analyze_all_questions()

    # 保存增强版JSON
    enhanced_json_path = analyzer.save_enriched_json()

    # 生成所有报告
    analyzer.save_all_reports()

    print("\n" + "="*60)
    print("分析完成!")
    print("="*60)
    print(f"\n输出文件:")
    print(f"1. 增强版JSON: {enhanced_json_path}")
    print(f"2. 分析报告: 资料分析_01~06.md (共6个文件)")

if __name__ == "__main__":
    main()
