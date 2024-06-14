from datetime import date


class StockItemRecord():
    """Handles a single item in the stock."""

    def __init__(self, **kwargs) -> None:
        for arg, value in kwargs.items():
            setattr(self, arg, value)

    def __bool__(self) -> bool:
        try:
            stock = float(self.stock)
            unitprice = float(self.unitprice)
            date = date.fromisoformat(self.productiondate)
            return (stock >= 0) and (unitprice >= 0)
        except (AttributeError, ValueError):
            return False
