# -*- coding: utf-8 -*-
from libs.db import OauthTable,oauth_engine
# from libs.db import test_engine,TestTable
from sqlmodel import Session,select
from dataclasses import dataclass

@dataclass
class A(object):
    a:DateTime

if __name__ == '__main__':
    with Session(test_engine) as session:
        result = session.exec(select(TestTable)).all()
        print(result)




