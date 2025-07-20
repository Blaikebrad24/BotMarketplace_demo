# File: app/models/execution_log.py
from sqlalchemy import Column, String, Text, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from app.models.BaseModel import BaseModel

class ExecutionLogModel(BaseModel):
    """
    Execution log model for detailed bot execution logging.
    
    This allows us to track what happened during bot execution
    for debugging and monitoring purposes.
    """
    
    
    # Foreign key
    execution_id = Column(
        UUID(as_uuid=True),
        ForeignKey('bot_executions.id', ondelete='CASCADE'),
        nullable=False,
        comment="Reference to the bot execution"
    )
    
    # Log details
    log_level = Column(
        String(20),
        default="INFO",
        comment="Log level: DEBUG, INFO, WARNING, ERROR, CRITICAL"
    )
    
    message = Column(
        Text,
        nullable=False,
        comment="Log message content"
    )
    
    timestamp = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        comment="When the log entry was created"
    )
    
    # Relationships
    execution = relationship(
        "BotExecutionModel",
        back_populates="execution_logs",
       
    )
    
    def __repr__(self):
        return f"<ExecutionLog(level='{self.log_level}', message='{self.message[:50]}...')>"