from Tkinter import *
from guiHelper import *
from node import *
from math import *
import copy
import time
import pdb

WINDOW_SIZE = (650,550)
BOX_SIZE = (600,500)
DOT_RADIUS = 16
HEIGHT = 11
WIDTH = 11
RESIZE_FACTOR = 40
QUA_X = 4.0
QUA_Y = 1.0/QUA_X
MINI_MAX_depth = 6
BFS_DEPTH = 4

class CatSolver:
  def __init__(self, canvas):
    self.c = canvas
    self.dots = []
    self.nodeMap = {}
    self.nodeCoorMap = {}
    self.Edges = []
    # Need to be reset
    self.redID = 1
    self.blacks = []

    # test variables
    self.grey = []
    self.drawBoard()
    self.calculatePar(QUA_X,QUA_Y)

  def calculatePar(self,x,y):
    x0 = 1.0
    x1 = x
    y0 = y
    y1 = 1.0
    self.pa = (y0 -y1)/(2.0 * x1 * (x0 - x1) - (pow(x0,2) - pow(x1,2)))
    self.pb = 2 * x1 * self.pa
    self.pc = y0 + self.pa * pow(x0,2)- self.pb * x0

  def reset(self,event):
    self.redID = 1
    self.blacks = []
    for each_dot in self.dots:
      self.c.itemconfigure(each_dot.Item,fill="yellow")
      each_dot.Reset()

  def pressHedge(self,event,canvas,dot):
    canvas.itemconfigure(dot,fill="black")
    self.nodeMap[dot].color = "black"
    self.blacks.append(self.nodeMap[dot])
    self.updatePrior(self.nodeMap[dot])

  def pressCat(self,event,canvas,dot):
    if self.nodeMap[dot].color == "yellow":
      if len(self.grey) > 0:
        for each_node in self.grey:
          canvas.itemconfigure(each_node.Item,fill="yellow")
        self.grey = []
      try:
        for each_node in self.recommand_node:
          if each_node.color == "yellow":
            canvas.itemconfigure(each_node.Item,fill="yellow")
      except Exception, e:
        pass
      canvas.itemconfigure(dot,fill="red")
      self.nodeMap[dot].color = "red"
      if self.redID != 1:
        canvas.itemconfigure(self.redID,fill="yellow")
        self.nodeMap[self.redID].color = "yellow"
      self.redID = dot
      # self.updateDistance(self.nodeMap[dot])
      # self.recommand_node = self.solve(self.nodeMap[dot])
      #------------ MiniMax ------------------------
      self.recommand_node = self.solveMiniMax(self.nodeMap[dot])

      for idx,each_node in enumerate(self.recommand_node):
        if idx == 0:
          canvas.itemconfigure(each_node.Item,fill="DarkGreen")
        else:
          canvas.itemconfigure(each_node.Item,fill="DarkSeaGreen")
      # self.checkCatch(self.nodeMap[dot])

  def updatePrior(self,node):
    frontier = copy.copy(node.Neighboors)
    secondary = []
    finished = [node]
    level = 1.0
    while len(frontier)>0:
      for each_node in frontier:
        secondary += [x for x in each_node.Neighboors if not x in frontier+secondary+finished]
        each_node.AddPror(1.0/level)
      finished += frontier
      frontier = secondary
      secondary = []
      level += 1.0 

  def updateDistance(self,node,test = False):
    frontier = [node]
    secondary = []
    finished = []
    edge_points = []
    level = 0.0
    while len(frontier)>0:
      for each_node in frontier:
        if test:
          each_node.TmpPoint = level
        else:
          each_node.SetEdgePoint(level)
        secondary += [x for x in each_node.Neighboors if not x in frontier+secondary+finished \
            and x.color == "yellow"]
        each_node.SetDistance(-self.pa*pow(level,2) + self.pb*level + self.pc)
        # print "qua: ",level," ",each_node.Distance
        if each_node.Edge:
          edge_points.append(each_node)
      finished += frontier
      frontier = secondary
      secondary = []
      level += 1.0
    total_edge_point = 0  
    for a_edge_point in self.Edges:
      if not a_edge_point in edge_points:
        if test:
          a_edge_point.TmpPoint = 10
        else:
          a_edge_point.EdgePoint = 10
        total_edge_point += 10
      else:
        if test:
          total_edge_point += a_edge_point.TmpPoint
        else:
          total_edge_point += a_edge_point.EdgePoint
    # self.Edges.sort(key=lambda a_node: a_node.EdgePoint)
    return total_edge_point

  def solve(self,node):
    seiged, edges, other, deepth, levels = self.checkCatch(node)
    frontier = levels[len(levels)-1]
    examine_nodes = []
    search_level = len(levels)-2
    while search_level >= 0:
      tmp_store = []
      for each_node in frontier:
        for each_other_node in each_node.Neighboors:
          if each_other_node in levels[search_level] and (not each_other_node in \
              examine_nodes+frontier+tmp_store):
            tmp_store.append(each_other_node)
      examine_nodes += frontier
      frontier = tmp_store
      search_level -= 1
    examine_nodes += frontier
    # all_nodes = edges+other
    # all_nodes.sort(key=lambda a_node: a_node.Score, reverse=True)
    # if len(all_nodes)>20:
    #   search_length = 20
    # else:
    #   search_length = len(all_nodes)
    bestnode = []
    bestedges = []
    bestothers = []
    score = (HEIGHT+WIDTH)*2
    for each_node in examine_nodes:
      each_node.color = "black"
      if deepth > 3:
        tmp_seiged, tmp_edges, tmp_other, tmp_deepth, _ = self.checkCatch(node)
      else:
        tmp_seiged, tmp_edges, tmp_other, tmp_deepth, _ = self.checkCatch(node,deepth)
      each_node.color = "yellow"
      # self.c.itemconfigure(each_node.Item,fill="grey")
      # self.grey.append(each_node)
      if tmp_seiged:
        return [each_node]
      lft_edges = [a_node for a_node in tmp_edges if a_node in edges]
      lft_other = [a_node for a_node in tmp_other if a_node in other]
      current_score = len(lft_edges)+len(lft_other)/RESIZE_FACTOR
      print "Score: ",current_score
      print "edges: ",len(lft_edges),", others: ",len(lft_other)
      if current_score < score:
        score = current_score
        bestnode = [each_node]
        bestedges = lft_edges
        bestothers = lft_other
      elif current_score == score:
        bestnode.append(each_node)
    print "Best score", score
    print "depth",deepth 
    bestnode.sort(key=lambda a_node: a_node.Score, reverse=True)
    return bestnode

  def solveMiniMax(self,node):
    (score, a_path) = self.minMax(cat_node = node,player_node = None,depth = MINI_MAX_depth,maximizingPlayer = False,track_val = -1)
    return [a_path[-1]]

  def minMax(self,cat_node,player_node,depth,maximizingPlayer,track_val): # player's objective minimize the cat score
    # pdb.set_trace()
    has_a_node = False
    if player_node:
      has_a_node = True
    if maximizingPlayer :
      if has_a_node:
        player_node.color = "black"
      if depth == 0:  # cat
        _, edges, other, deepth, _ = self.checkCatch(cat_node,BFS_DEPTH)
        if has_a_node:
          player_node.color = "yellow"
        if cat_node.Edge:
          return (edges*RESIZE_FACTOR + other + 1000, [])
        else:
          return (edges*RESIZE_FACTOR + other, [])
    else:
      if depth == 0:  # player
        _, edges, other, deepth, _ = self.checkCatch(cat_node,BFS_DEPTH)
        if cat_node.Edge:
          return (edges*RESIZE_FACTOR + other + 1000, [player_node])
        else:
          return (edges*RESIZE_FACTOR + other, [player_node])
    if maximizingPlayer:  # cat
      bestValue = -1
      seiged = True
      for each_child in cat_node.Neighboors:
        if each_child.color == "yellow" or each_child.color == "red":
          seiged = False
          (score, a_path) = self.minMax(each_child,player_node,depth-1,False,bestValue)
          if score >= track_val and track_val != -1:
            if has_a_node:
              player_node.color = "yellow"
            return (score, a_path) 
          if bestValue == -1 or score > bestValue:
             bestValue = score
      if has_a_node:
        player_node.color = "yellow"
      if seiged and not cat_node.Edge:
        return (0, [])
      elif seiged and cat_node.Edge:
        return (1000, [])
      else:
        return (bestValue, a_path)
    else:                 # player
      bestValue = -1
      _, tmp_edges, tmp_other, deepth, _ = self.checkCatch(cat_node,BFS_DEPTH)
      for each_child in reversed(tmp_other+tmp_edges):
        (score, a_path) = self.minMax(cat_node,each_child,depth-1,True,bestValue)
        if score <= track_val and track_val != -1:
          a_path.append(each_child)
          return (score, a_path)
        if bestValue == -1 or score < bestValue:
          bestValue = score
          bestNode = each_child
      a_path.append(bestNode)
      # pdb.set_trace()
      return (bestValue, a_path)

  def checkCatch(self,node,ref = 0):
    # start_time = time.clock()
    edge_points = []
    frontier = [node]
    secondary = []
    finished = []
    levels = []
    level = 0
    while len(frontier)>0 and len(edge_points)==0 and (level<=ref or ref == 0):
      levels.append(frontier)
      for each_node in frontier:
        # self.c.itemconfigure(each_node.Item,fill="green")
        for each_other_node in each_node.Neighboors:
          if each_other_node.color != "black" and not each_other_node.Edge and \
              (not each_other_node in finished+frontier+secondary):
            secondary.append(each_other_node)
          elif each_other_node.color != "black" and each_other_node.Edge and \
              (not each_other_node in edge_points):
            edge_points.append(each_other_node)
            # self.c.itemconfigure(each_other_node.Item,fill="orange")
      if len(edge_points)>0:
        levels.append(edge_points)
      level += 1
      finished += frontier
      frontier = secondary
      secondary = []
    if finished[0] == node:
      del finished[0]
    del levels[0]
    if len(edge_points)==0:
      # print time.clock() - start_time, "seconds"
      if ref == 0:
        return (True,edge_points,finished,level-1,levels)
      else:
        return (False,edge_points,finished,level-1,levels)
    else:
      # print time.clock() - start_time, "seconds"
      return (False,edge_points,finished,level-1,levels)

  def drawBoard(self):
    init_pos = (-(5.0+1.0/2.0)*DOT_RADIUS*2,-DOT_RADIUS*5.0*sqrt(3.0))
    dot_pos =list(init_pos)
    for y in xrange(0,HEIGHT):
      for x in xrange(0,WIDTH):
        dot_id = drawPoint(self.c,dot_pos,'yellow',DOT_RADIUS-1 ,WINDOW_SIZE)
        a_dot = node(y*HEIGHT+x,dot_id,(x,y),tuple(dot_pos))
        if x == 0 or x == WIDTH-1 or y == 0 or y == HEIGHT-1:
          a_dot.SetEdge()
          self.Edges.append(a_dot)
        self.dots.append(a_dot)
        self.nodeMap[dot_id] = a_dot
        self.nodeCoorMap[(x,y)] = a_dot
        self.c.tag_bind(dot_id,"<Button-1>",lambda e, i_id=dot_id: \
            self.pressHedge(e, self.c, i_id))
        self.c.tag_bind(dot_id,"<Button-3>",lambda e, i_id=dot_id: \
            self.pressCat(e, self.c, i_id))
        dot_pos[0] += 2.0*DOT_RADIUS
      if y%2 == 1:
        dot_pos[0] = init_pos[0]
      else:
        dot_pos[0] = init_pos[0] + DOT_RADIUS
      dot_pos[1] += DOT_RADIUS*sqrt(3.0)
    for y in xrange(0,HEIGHT):
      for x in xrange(0,WIDTH):
        for y_shift in xrange(-1,2):
          for x_shift in xrange(-1,2):
            y_nb = y+y_shift
            x_nb = x+x_shift
            if y_nb>=0 and y_nb<HEIGHT and x_nb>=0 and x_nb<WIDTH and \
                not (y_shift == 0 and x_shift == 0):
              if sqrt(
                  pow(self.nodeCoorMap[(x_nb,y_nb)].Pos[0]-self.nodeCoorMap[(x,y)].Pos[0],2)+ \
                  pow(self.nodeCoorMap[(x_nb,y_nb)].Pos[1]-self.nodeCoorMap[(x,y)].Pos[1],2))- \
                  2.0*DOT_RADIUS<1.0:
                self.nodeCoorMap[(x,y)].AddNeighboor(self.nodeCoorMap[(x_nb,y_nb)])
    self.c.bind("<Button-2>",self.reset)
    self.c.bind("<Double-Button-1>",lambda e:self.checkCatch(self.nodeMap[self.redID]))

def main():
  c = InitalizeBoard(WINDOW_SIZE,BOX_SIZE)
  solver = CatSolver(c)
  c.mainloop()

if __name__ == '__main__':
  main()