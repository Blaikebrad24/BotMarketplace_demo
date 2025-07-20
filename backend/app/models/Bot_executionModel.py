# File: app/models/bot_execution.py
from sqlalchemy import Column, String, Integer, Text, DateTime
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from app.models.BaseModel import BaseModel

class BotExecutionModel(BaseModel):
    """
    Bot execution model for tracking bot runs.
    
    New SQLAlchemy concepts:
    - JSONB: PostgreSQL's JSON with indexing support
    - Flexible data storage for bot parameters and results
    """
    
    __tablename__ = "bot_executions"
    # Foreign keys
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey('users.id', ondelete='SET NULL'),
        comment="User who executed the bot"
    )
    
    bot_id = Column(
        UUID(as_uuid=True),
        ForeignKey('bots.id', ondelete='SET NULL'),
        comment="Bot that was executed"
    )
    
    # Execution status
    execution_status = Column(
        String(50),
        default="queued",
        comment="Status: queued, running, completed, failed, cancelled"
    )
    
    # Flexible data storage using JSONB
    input_parameters = Column(
        JSONB,
        comment="Bot input parameters as JSON"
    )
    
    output_data = Column(
        JSONB,
        comment="Bot execution results as JSON"
    )
    
    # Execution metrics
    execution_time = Column(
        Integer,
        comment="Execution time in seconds"
    )
    
    error_message = Column(
        Text,
        comment="Error message if execution failed"
    )
    
    # Container tracking
    container_id = Column(
        String(255),
        comment="Docker container ID for this execution"
    )
    
    # Timing
    started_at = Column(
        DateTime(timezone=True),
        comment="When execution started"
    )
    
    completed_at = Column(
        DateTime(timezone=True),
        comment="When execution completed"
    )
    
    # Relationships
    user = relationship(
        "UserModel",
        back_populates="bot_executions",
       
    )
    
    bot = relationship(
        "BotModel",
        back_populates="executions",
    )
    
    execution_logs = relationship(
        "ExecutionLogModel",
        back_populates="execution",
        cascade="all, delete-orphan",
    )
    
    def __repr__(self):
        return f"<BotExecution(bot_id='{self.bot_id}', status='{self.execution_status}')>"