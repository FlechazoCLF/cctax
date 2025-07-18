

#****************************************************************************************************
# File Start!
#***************************************************************************************************/

#*
 #
 #  Copyright (c) 2024-2025 by flechazo. All rights reserved.
 #
 # Author : CarlChai LinFeng Chai flechazo
 # Website: flechazo.mba
 #
 # Change Logs:
 # Date           Author       Notes
 # 2025-06-19     cc          the first version
 #
#/

#****************************************************************************************************
# Include
#***************************************************************************************************/

import tkinter as tk
from cctax_ui import cctax_ui

#****************************************************************************************************
# Define
#***************************************************************************************************/

#****************************************************************************************************
# Type Define
#***************************************************************************************************/

class cctax:
    def __init__(self):
        self.root = tk.Tk()
        self.app = cctax_ui(self.root)
        self.root.mainloop() 

#****************************************************************************************************
# Global Variable
#***************************************************************************************************/

#****************************************************************************************************
# Function Impletement
#***************************************************************************************************/

if __name__ == "__main__":
    tax = cctax()

#****************************************************************************************************
# exports
#***************************************************************************************************/

#****************************************************************************************************
# File End!
#***************************************************************************************************/
