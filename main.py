from views import main
from database import create_table
if __name__ == '__main__':
    
    # bot UPDATES database at 5 AM UTC +5:30 everyday
    x = input('''\tMenu: 
    \t0. Create Table (if this is your first time running this) 
    \t1. Start Bot
    ''')
    if(x == "0"):
        create_table()
        print('TABLE CREATED')
        pass
        
    if x == "1":
        main()

    
    
