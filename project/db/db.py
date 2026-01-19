from collections.abc import Generator

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from project.config import Settings, get_settings


def get_engine(settings: Settings | None = None) -> Engine:
    """Create SQLAlchemy engine based on settings."""
    if settings is None:
        settings = get_settings()

    connect_args = {}
    if settings.DB_TYPE == "sqlite":
        connect_args["check_same_thread"] = False

    return create_engine(
        settings.DB_URL,
        echo=settings.SQLALCHEMY_ECHO,
        connect_args=connect_args,
    )


engine = get_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_session() -> Generator[Session, None, None]:
    """Dependency that provides a database session."""
    with SessionLocal() as session:
        yield session
