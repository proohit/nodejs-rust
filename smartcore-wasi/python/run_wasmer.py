from lib.python.glue import load_model

output = load_model()

print(output)

# May be used for dynamic lib loading
# import time
# import importlib
# import lib.python.glue as glue

# for i in range(5):
#     output = glue.load_model()
#     print(output)
#     importlib.reload(glue)
#     time.sleep(5)
