# File: app/models/order.py
from sqlalchemy import Column, String, DECIMAL, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from app.models.BaseModel import BaseModel

class OrderModel(BaseModel):
    """
    Order model representing bot purchases.
    
    New SQLAlchemy concepts:
    - ForeignKey: Links to other tables
    - server_default: Database-level default values
    - Decimal precision for money
    """
    
    # Foreign key to user
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey('users.id', ondelete='SET NULL'),
        comment="User who placed the order"
    )
    
    # Order financial details
    total_amount = Column(
        DECIMAL(10, 2),
        nullable=False,
        comment="Total order amount in USD"
    )
    
    # Payment integration
    stripe_payment_intent_id = Column(
        String(255),
        comment="Stripe payment intent ID for tracking"
    )
    
    # Order status tracking
    payment_status = Column(
        String(50),
        default="pending",
        comment="Payment status: pending, completed, failed, refunded"
    )
    
    order_status = Column(
        String(50),
        default="processing",
        comment="Order status: processing, completed, cancelled"
    )
    
    # Relationships
    user = relationship(
        "UserModel",
        back_populates="orders",
        
    )
    
    order_items = relationship(
        "OrderItemModel",
        back_populates="order",
        cascade="all, delete-orphan",
        
    )
    
    def __repr__(self):
        return f"<Order(id='{self.id}', total={self.total_amount}, status='{self.order_status}')>"