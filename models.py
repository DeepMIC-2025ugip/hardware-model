import uuid
from datetime import date, datetime, timezone

from db.database import Base
from sqlalchemy import Boolean, Column, Date, DateTime, String, Text
from sqlalchemy.dialects.postgresql import ARRAY, JSON, UUID


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    from_system = Column(
        Boolean, nullable=False
    )  # AIの応答(True) or ユーザーの質問(False)
    content = Column(String, nullable=False)
    visible = Column(Boolean, default=True)  # 親に見せるかどうか
    timestamp = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )


class Analysis(Base):
    __tablename__ = "analyses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    report = Column(Text, nullable=False)  # 1日の会話からのAI分析レポート
    keyword = Column(ARRAY(String), nullable=False)  # 1日の会話で出たキーワードのリスト
    feelings = Column(JSON, nullable=False)  # 喜怒哀楽の感情スコア (dict[str, int])
    date = Column(Date, default=date.today, nullable=False)  # その日の日付 (YYYY-MM-DD)


class Character(Base):
    __tablename__ = "characters"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    personality = Column(String, nullable=False)  # 子どもの性格
    strengths = Column(ARRAY(String), nullable=False)  # 子どもの強み
    weaknesses = Column(ARRAY(String), nullable=False)  # 子どもの弱み
    hobbies = Column(ARRAY(String), nullable=False)  # 子どもの趣味
    family = Column(String, nullable=False)  # 家族との関係
    friends = Column(ARRAY(String), nullable=False)  # 友達との関係
    school_life = Column(String, nullable=False)  # 学校生活
    future_dream = Column(String, nullable=False)  # 将来の夢
    likes = Column(ARRAY(String), nullable=False)  # 好きなこと
    dislikes = Column(ARRAY(String), nullable=False)  # 嫌いなこと
    stress = Column(String, nullable=False)  # ストレス要因
    worries = Column(String, nullable=False)  # 悩み事
    favorite_food = Column(
        ARRAY(String), nullable=False
    )  # 好きな食べ物・スポーツ・本・音楽・テレビ番組・映画
    other = Column(String, nullable=False)  # その他
    timestamp = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
