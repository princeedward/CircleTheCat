class node:
  def __init__(self,node_id,item_id,coor,pos):
    self.Node = node_id
    self.Item = item_id
    self.Coor = coor
    self.Pos = pos
    self.Neighboors = []
    self.Edge = False
    # Need to be reset
    self.color = "yellow"
    self.Score = 0
    self.Priority = 0
    self.Distance = 0
    self.EdgePoint = 10
    self.TmpPoint = 10

  def AddNeighboor(self, a_node):
    self.Neighboors.append(a_node)

  def SetEdge(self):
    self.Edge = True

  def AddPror(self, extra_prior):
    self.Priority += extra_prior
    self.Score = self.Priority+self.Distance

  def SetDistance(self,dis):
    self.Distance = dis
    self.Score = self.Priority+self.Distance

  def SetEdgePoint(self,point):
    self.EdgePoint = point

  def Reset(self):
    self.color = "yellow"
    self.Score = 0
    self.Priority = 0
    self.Distance = 0
    self.EdgePoint = 10
    self.TmpPoint = 10
