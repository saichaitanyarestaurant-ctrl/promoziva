from sqlalchemy import Column, Integer, String, Text, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    context = Column(Text)  # Conversation context/summary
    
    # Conversation metadata
    session_id = Column(String(100), index=True)
    conversation_type = Column(String(50))  # voice, text, mixed
    
    # State tracking
    is_active = Column(String(10), default="active")  # active, paused, ended
    current_topic = Column(String(255))
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    ended_at = Column(DateTime(timezone=True))
    
    # Relationships
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="conversations")
    
    tasks = relationship("Task", back_populates="conversation")
    messages = relationship("ConversationMessage", back_populates="conversation")

    def __repr__(self):
        return f"<Conversation(id={self.id}, title='{self.title}', session_id='{self.session_id}')>"

class ConversationMessage(Base):
    __tablename__ = "conversation_messages"

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"))
    
    # Message content
    content = Column(Text, nullable=False)
    message_type = Column(String(50))  # user, assistant, system, error
    
    # Message metadata
    role = Column(String(20))  # user, assistant, system
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    # Additional data
    metadata = Column(JSON)  # Additional message metadata
    
    # Relationships
    conversation = relationship("Conversation", back_populates="messages")

    def __repr__(self):
        return f"<ConversationMessage(id={self.id}, type='{self.message_type}', role='{self.role}')>"