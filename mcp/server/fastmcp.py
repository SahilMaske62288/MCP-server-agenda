class FastMCP:
    def __init__(self, name, lifespan=None):
        self.name = name
        self.lifespan = lifespan

    def tool(self):
        def decorator(func):
            # You can optionally register the tool here
            return func
        return decorator

