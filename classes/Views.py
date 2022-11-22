from discord.ui import View
from .Buttons import *
class CatchCatMessageView(View):
    def __init__(self, catchButtonCallback) -> None:
        """Creates a View object

        Args:
            catchButtonCallback (function): The callback for the catch button
        """
        super().__init__()
        btn = CatchButton()
        btn.callback = catchButtonCallback
        self.add_item(btn)
    
class InventoryNavigationView(View):
    def __init__(self, callbackPrevious, callbackNext, previousOff = False, nextOff = False):
        super().__init__()
        
        btnPrevious, btnNext = ButtonPreviousPage(disabled=previousOff), ButtonNextPage(disabled=nextOff)
        
        btnPrevious.callback, btnNext.callback = callbackPrevious, callbackNext
        self.add_item(btnPrevious)
        self.add_item(btnNext)