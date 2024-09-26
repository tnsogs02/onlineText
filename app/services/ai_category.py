import pandas as pd
import fasttext
import jieba
import re

class AiCategory():
    def __init__(self):
        jieba.load_userdict('app/models/zh-tw_jieba_custom_dict.txt')

        
    def get_available_processors(self):
        object_processors = [
            processor_name for processor_name in dir(self)
            if (processor_name.startswith("proc_")) and callable(getattr(self, processor_name))
        ]
        return object_processors
    
    def run_predict(self, processor_name, dataframe):
        try:
            processor = getattr(self, processor_name)
            if(callable(processor)):
                predictionDf = pd.DataFrame()
                predictionDf[["pred_category_identifier", "pred_category_name"]] = dataframe.apply(processor, axis=1, result_type="expand", target_column=self.__scan_target_column(dataframe))
                dataframe.insert(3, '建議分類名稱', predictionDf['pred_category_name'])
                dataframe.insert(3, '建議分類identifier', predictionDf['pred_category_identifier'])
                return dataframe
        except:
            return None
        
    def proc_en_raw(self, row, target_column):
        model = fasttext.load_model("app/models/model_en.bin")
        if(len(str(row[target_column])) > 1):
            prediction = model.predict(str(row[target_column]), k = 1)[0][0].replace("__label__", "")
            prediction = prediction.split("__")
            return prediction[0], prediction[1]
        else:
            return "", ""
    
    def proc_zh_tw_jieba(self, row, target_column):
        model = fasttext.load_model("app/models/model_zh-tw_jieba.bin")
        if(len(str(row[target_column])) > 1):
            product_name = self.__zh_standardization(str(row[target_column]))
            product_name_cut = ' '.join(jieba.cut(product_name))
            prediction = model.predict(product_name_cut, k = 1)[0][0].replace("__label__", "")
            prediction = prediction.split("__")
            return prediction[0], prediction[1]
        else:
            return "", ""
    
    def __scan_target_column(self, dataframe):
        column_list = dataframe.columns.to_list()
        for column_name in ["name", "名稱", "商品名稱"]:
            if(column_name in column_list):
                return column_name
        
    def __remove_parentheses(self, text):    
        stack = []
        result = []

        for char in text:
            if char == '(':
                stack.append(len(result))
            elif char == ')':
                if stack:
                    stack.pop()
            elif not stack:
                result.append(char)

        return ''.join(result)   
        
    def __zh_standardization(self, product_name):
        replacements = {
            '{': '(',
            '[': '(',
            '【': '(',
            '「': '(',
            '『': '(',
            '}': ')',
            ']': ')',
            '】': ')',
            '」': ')',
            '』': ')'
        }
        
        for old, new in replacements.items():
            product_name = product_name.replace(old, new)

        placeholder = "恤恤恤的佔位符"
        string = product_name.replace("T恤", placeholder)
        string = self.__remove_parentheses(product_name)

        patterns = [
            r'\d+個入',
            r'\d+入',
            r'\d+個',
            r'等車款',
            r'車款',
            r'男用',
            r'女用',
            r'[^\u4e00-\u9fff]',
        ]

        replacement = ""
        for pattern in patterns:
            string = re.sub(pattern, replacement, string)

        string = string.replace('、', ' ')
        string = string.replace('〜', ' ')
        string = string.replace('・', ' ')

        string = string.replace(placeholder, "T恤")

        return string.strip()