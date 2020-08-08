from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, String, PrimaryKeyConstraint, and_
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError, IntegrityError, OperationalError
import os

RDS_ENDPOINT = os.getenv('RDS_ENDPOINT')
RDS_USER = os.getenv('RDS_USER')
RDS_PASSWORD = os.getenv('RDS_PASSWORD')


engine = create_engine('mysql+pymysql://{}:{}@{}:3306/telegram_stock_bot'.format(RDS_USER, RDS_PASSWORD, RDS_ENDPOINT))
# engine = create_engine('mysql+pymysql://root:@localhost:3306/telegram_stock_bot') #for local
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

class Portfolio(Base):
    __tablename__ = 'portfolio'

    telegram_id = Column(String)
    stock_ticker = Column(String)

    __table_args__ = (
        PrimaryKeyConstraint('telegram_id', 'stock_ticker'),
        {},
    )        


    def dictRepr(self):
        return (self.telegram_id, self.stock_ticker)

    def __repr__(self):
        return '{}:{}'.format(self.telegram_id, self.stock_ticker)

def addTicker(telegramId: str, stockTicker: str):
    try:
        row = Portfolio(telegram_id=telegramId, stock_ticker=stockTicker)
        session.add(row)
        session.commit()
    except OperationalError as e:
        return "Unable to connect to database!"
    except IntegrityError as e:
        return "Ticker already exists!"
    except SQLAlchemyError as e:
        print(e)
        return "An unexpected error occurred!"

    return "{} added to portfolio successfully".format(stockTicker)

def deleteTicker(telegramId: str, stockTicker: str):
    try:
        row = session.query(Portfolio).filter(and_(Portfolio.telegram_id==telegramId, Portfolio.stock_ticker==stockTicker)).first()
        if row == None:
            return "{} does not exist in portfolio!".format(stockTicker)
        session.delete(row)
        session.commit()
    except OperationalError as e:
        return "Unable to connect to database!"
    except SQLAlchemyError as e:
        print(e)
        return "An unexpected error occurred!"

    return "{} deleted from portfolio successfully".format(stockTicker)

def getTickerByTelegramId(telegramId: str):
    try:
        stockTickers = [row.stock_ticker for row in session.query(Portfolio).filter(Portfolio.telegram_id==telegramId).all()]
    except OperationalError as e:
        return "Unable to connect to database!"
    except SQLAlchemyError as e:
        print(e)
        return "An unexpected error occurred!"

    return(stockTickers)