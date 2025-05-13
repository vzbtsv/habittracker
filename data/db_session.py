import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session

SqlAlchemyBase = orm.declarative_base()

__factory = None


def global_init(db_file: str) -> None:
    global __factory

    if __factory:
        return

    if not db_file or not db_file.strip():
        raise ValueError("Необходимо указать файл базы данных.")

    conn_str = f'sqlite:///{db_file.strip()}?check_same_thread=False'
    print(f"Подключение к базе данных по адресу {conn_str}")

    engine = sa.create_engine(
        conn_str,
        echo=False,
        pool_pre_ping=True
    )

    __factory = orm.sessionmaker(
        bind=engine,
        autoflush=False,
        expire_on_commit=False
    )

    from . import __all_models  # noqa
    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    if not __factory:
        raise RuntimeError("Сначала вызовите global_init()")
    return __factory()
