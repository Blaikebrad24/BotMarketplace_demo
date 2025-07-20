# File: app/models/order_item.py
from sqlalchemy import Column, Integer, DECIMAL
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from app.models.BaseModel import BaseModel

class OrderItemModel(BaseModel):
    """
    Order item model representing individual bots in an order.
    
    This is a classic e-commerce pattern where:
    - Order = Shopping cart/receipt
    - OrderItem = Individual line items on the receipt
    """
    
    # Foreign keys
    order_id = Column(
        UUID(as_uuid=True),
        ForeignKey('orders.id', ondelete='CASCADE'),
        nullable=False,
        comment="Reference to the parent order"
    )
    
    bot_id = Column(
        UUID(as_uuid=True),
        ForeignKey('bots.id', ondelete='SET NULL'),
        comment="Reference to the purchased bot"
    )
    
    # Item details
    quantity = Column(
        Integer,
        default=1,
        comment="Quantity purchased (usually 1 for digital products)"
    )
    
    price_at_purchase = Column(
        DECIMAL(10, 2),
        nullable=False,
        comment="Price when purchased (for historical accuracy)"
    )
    
    # Relationships
    order = relationship(
        "OrderModel",
        back_populates="order_items",
        
    )
    
    bot = relationship(
        "BotModel",
        back_populates="order_items",
        
    )
    
    def __repr__(self):
        return f"<OrderItem(bot_id='{self.bot_id}', quantity={self.quantity}, price={self.price_at_purchase})>"