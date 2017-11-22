from haystack import indexes
from df_goods.models import Goods

# 指定对于某个类的某些数据建立索引
# 索引类的类名:一般格式:模型类名+Index
class GoodsIndex(indexes.SearchIndex, indexes.Indexable):
    # 直接根据表格中的哪些字段建立索引
    # use_template=True说明会在一个文件中指定根据哪些字段建立索引
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        # 返回你的模型类
        return Goods

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
