from datetime import datetime
from sqlalchemy import func
from utils.databaseManager import Database
from utils.databaseManager import Order, Card, ProdCag


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


if __name__ == '__main__':
    # 测试获取所有dashboard数据
    ddq = DisplayDataQuery()
    ddq.query_dashboard_data()
    ddq.query_classification_management()