from datetime import datetime
from sqlalchemy import func
from sqlalchemy.future import select
from utils.databaseManager import Database, Order, Card, ProdCag, ProdInfo
from utils.databaseSchemas import ProdCagResponse, ProdInfoResponse


class Statistical(Database):

    def get_daily_stats(self, model):
        """按天统计订单"""
        with self.session_scope() as session:
            today = datetime.now().date()
            stats = (
                session.query(func.date(model.updatetime), func.count(model.id)).group_by(func.date(model.updatetime)).all()
            )
        return stats

    @staticmethod
    def get_weekly_stats():
        stats = (
            db.query(func.strftime("%Y-%W", Order.created_at), func.count(Order.id))
            .group_by(func.strftime("%Y-%W", Order.created_at))
            .all()
        )
        return stats

    @staticmethod
    # 按月统计订单
    def get_monthly_stats(db):
        stats = (
            db.query(func.strftime("%Y-%m", Order.created_at), func.count(Order.id))
            .group_by(func.strftime("%Y-%m", Order.created_at))
            .all()
        )
        return stats


# Statistical().get_daily_stats(Order)

# exit()

class DisplayDataQuery(Database):
    def query_dashboard_data(self, show=True):
        """查询仪表盘数据"""
        info = {}
        info['total_order'] = len(self.get_all_records(Order))  # 总订单
        info['total_money'] = 0  # 总收入
        info['total_user'] = 5  # 总用户
        info['total_card'] = len(self.get_all_records(Card))  # 总卡密
        if show:
            print("info:", info)
        # 订单统计：天、周、月、年   订单数量、订单金额
        # try:
        #     print("1")
        #     print(func.sum(Order.total_price))
        #     info['total_income'] = round(self.get_all_records(func.sum(Order.total_price)).scalar(), 2)  # 总收入
        #     print("2")
        #     info['total_num'] = int(
        #         Order.query.with_entities(func.sum(Order.num)).scalar())  # 总销售数量--mysql模式下<Decimal('6')
        # except:
        #     info['total_income'] = '0.00'
        #     info['total_num'] = 0
        # # # 历史数据获取
        # orders = Order.query.filter(Order.updatetime >= NOW - timedelta(days=7)).all()
        # info['history_date'], info['history_price'] = sort_count(
        #     [(x.updatetime.strftime('%Y-%m-%d'), x.total_price) for x in orders])
        return info

    def query_classification_management(self, show=True):
        """查询分类管理"""
        items = self.get_all_records(ProdCag)  # 分类管理查询
        return items


class ProdCagManager(Database):
    def create(self, name, sort, state):
        """创建新记录"""
        newProdCag = ProdCag(name=name, sort=sort, state=state)
        with self.session_scope() as session:
            session.add(newProdCag)

    def read(self, skip=0, limit=10):
        """获取所有记录"""
        with self.session_scope() as session:
            result = session.execute(select(ProdCag).offset(skip).limit(limit))
            prodcags = result.scalars().all()
            return [ProdCagResponse.from_orm(prodcag) for prodcag in prodcags]

    def update(self, item_name, new_name=None, new_sort=None, new_state=None):
        """更新记录"""
        with self.session_scope() as session:
            prod_cag = session.query(ProdCag).filter_by(name=item_name).first()
            if prod_cag:
                if new_name:
                    prod_cag.name = new_name
                if new_sort:
                    prod_cag.sort = new_sort
                if new_state:
                    prod_cag.state = new_state
                session.commit()

    def delete(self, item_name):
        """删除记录"""
        with self.session_scope() as session:
            prod_cag = session.query(ProdCag).filter_by(name=item_name).first()
            if prod_cag:
                session.delete(prod_cag)
                session.commit()

    def unit_testing(self):
        """单元测试"""
        self.create("unit_test_create", 1, True)
        self.read()
        self.update("unit_test_create", new_name="unit_test_update", new_sort=100, new_state=False)
        self.delete("unit_test_update")
        print("========ProdCagManager 单元测试完成=========")


class ProdInfoManager(Database):
    def create(self, attributes):
        """创建新记录"""
        prodinfo = ProdInfo()
        for attr, value in attributes.items():
            if value:
                setattr(prodinfo, attr, value)
        with self.session_scope() as session:
            session.add(prodinfo)

    def read(self, skip=0, limit=10):
        """获取所有记录"""
        with self.session_scope() as session:
            result = session.execute(select(ProdInfo).offset(skip).limit(limit))
            prodinfos = result.scalars().all()
            return [ProdInfoResponse.from_orm(prodinfo) for prodinfo in prodinfos]

    def update(self, attributes):
        """更新记录"""
        with self.session_scope() as session:
            prod_info = session.query(ProdInfo).filter_by(name=attributes["old_name"]).first()
            for attr, value in attributes.items():
                if value:
                    setattr(prod_info, attr, value)
                session.commit()

    def delete(self, item_name):
        """删除记录"""
        with self.session_scope() as session:
            prod_info = session.query(ProdInfo).filter_by(name=item_name).first()
            if prod_info:
                session.delete(prod_info)
                session.commit()

    def unit_testing(self):
        """单元测试"""
        self.create({"name": "单元测试", "prod_cag_name": "单元测试", "prod_info": "单元测试",
                     "prod_img_url": "单元测试", "prod_discription": "示例：卡密格式：单元测试",
                     "prod_price": 9.99, "prod_sales": 0, "prod_tag": "单元测试", "auto": True, "sort": "100",
                     "state": True})
        # self.read()
        self.update({"old_name": "单元测试", "name": "单元测试_修改名称", "prod_cag_name": "单元测试_修改",
                     "prod_info": "单元测试_修改", "prod_img_url": "单元测试_修改",
                     "prod_discription": "示例：卡密格式：单元测试_修改", "prod_price": 99.99, "prod_sales": 100,
                     "prod_tag": "单元测试_修改", "auto": False, "sort": "50", "state": False})
        self.delete("单元测试_修改名称")
        print("========ProdInfoManager 单元测试完成=========")


# CardManager class
class CardManager(Database):
    def create(self):
        pass

    def read(self, skip=0, limit=10):
        pass

    def update(self):
        pass

    def delete(self):
        pass

    def unit_testing(self):
        pass


if __name__ == '__main__':
    ProdCagManager().unit_testing()
    ProdInfoManager().unit_testing()
    CardManager().unit_testing()
