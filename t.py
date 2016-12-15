import os
import codestreak

is_test_run = 'TEST' in os.environ

if __name__ == '__main__' and not is_test_run:
    codestreak.app.run()
