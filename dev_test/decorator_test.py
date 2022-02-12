
availableComponent = []

def Component(title: str):
    print("Decorator Called!")
    def wrapper(func):
        availableComponent.append(func)
        func.__dict__['title'] = title
        print("before_function")
        def wrapper_call(*args, **kwargs):
            return func(*args, **kwargs)
        print("after_function")
        return wrapper_call
    return wrapper

@Component(title="TEST COMPONENT!")
def TestComponent():
    return f"Hi from test component"

def main():
    print(availableComponent)
    for component in availableComponent:
        print(component.__dict__)

if __name__ == "__main__": main()

"""
Decorator Called!
before_function
after_function
[<function TestComponent at 0x000001FF2D4FC430>]
{'title': 'TEST COMPONENT!'}
"""