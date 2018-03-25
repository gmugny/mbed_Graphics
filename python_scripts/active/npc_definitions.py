import pandas as pd

class NPC():
    def __init__(self):
        self.left1 = 0
        self.left2 = 0
        self.right1 = 0
        self.right2 = 0
        self.up1 = 0
        self.up2 = 0
        self.down1 = 0
        self.down1 = 0
        self.NPC_id = ""
        self.NPC_id_num = 0
        
    def set_NPC_details(self, id_string, id_num):
        self.NPC_id = id_string
        self.NPC_id_num = id_num
        
    def set_left(self, left1, left2):
        self.left1 = left1
        self.left2 = left2
        
    def set_right(self, right1, right2):
        self.right1 = right1
        self.right2 = right2
        
    def set_up(self, up1, up2):
        self.up1 = up1
        self.up2 = up2
        
    def set_down(self, down1, down2):
        self.down1 = down1
        self.down2 = down2

npc_list = pd.Series()
npc = NPC()
npc.set_NPC_details("skeleman", 2)
npc.set_left(30, 31)
npc.set_right(30, 31)
npc.set_up(28, 29)
npc.set_down(24, 25)
this_npc = pd.Series(npc, index=[npc.NPC_id])
npc_list = npc_list.append(this_npc)

npc = NPC()
npc.set_NPC_details("skelemage", 3)
npc.set_left(34, 35)
npc.set_right(34, 35)
npc.set_up(32, 33)
npc.set_down(26, 27)
this_npc = pd.Series(npc, index=[npc.NPC_id])
npc_list = npc_list.append(this_npc)

npc = NPC()
npc.set_NPC_details("slimedood", 4)
npc.set_left(40, 41)
npc.set_right(40, 41)
npc.set_up(38, 39)
npc.set_down(36, 37)
this_npc = pd.Series(npc, index=[npc.NPC_id])
npc_list = npc_list.append(this_npc)

npc = NPC()
npc.set_NPC_details("femalenpc2", 5)
npc.set_left(49, 50)
npc.set_right(49, 50)
npc.set_up(47, 48)
npc.set_down(45, 46)
this_npc = pd.Series(npc, index=[npc.NPC_id])
npc_list = npc_list.append(this_npc)

npc = NPC()
npc.set_NPC_details("angryslime", 6)
npc.set_left(74, 75)
npc.set_right(74, 75)
npc.set_up(72, 73)
npc.set_down(70, 71)
this_npc = pd.Series(npc, index=[npc.NPC_id])
npc_list = npc_list.append(this_npc)

npc = NPC()
npc.set_NPC_details("ratto", 7)
npc.set_left(89, 90)
npc.set_right(89, 90)
npc.set_up(87, 88)
npc.set_down(85, 86)
this_npc = pd.Series(npc, index=[npc.NPC_id])
npc_list = npc_list.append(this_npc)

npc = NPC()
npc.set_NPC_details("magidude", 8)
npc.set_left(105, 106)
npc.set_right(105, 106)
npc.set_up(103, 104)
npc.set_down(101, 102)
this_npc = pd.Series(npc, index=[npc.NPC_id])
npc_list = npc_list.append(this_npc)

npc = NPC()
npc.set_NPC_details("mage", 9)
npc.set_left(111, 112)
npc.set_right(111, 112)
npc.set_up(109, 110)
npc.set_down(107, 108)
this_npc = pd.Series(npc, index=[npc.NPC_id])
npc_list = npc_list.append(this_npc)

npc = NPC()
npc.set_NPC_details("frogman", 10)
npc.set_left(117, 118)
npc.set_right(117, 118)
npc.set_up(115, 116)
npc.set_down(113, 114)
this_npc = pd.Series(npc, index=[npc.NPC_id])
npc_list = npc_list.append(this_npc)

npc = NPC()
npc.set_NPC_details("slimecat", 11)
npc.set_left(136, 137)
npc.set_right(136, 137)
npc.set_up(134, 135)
npc.set_down(132, 133)
this_npc = pd.Series(npc, index=[npc.NPC_id])
npc_list = npc_list.append(this_npc)


