# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

from logging import root
import util
from game import Directions

# helper function for directions conversion 
def directions_to_instruction(direction_string):
    if direction_string  == "North":
        return Directions.NORTH
    if direction_string  == "South":
        return Directions.SOUTH
    if direction_string  == "East":
        return Directions.EAST
    if direction_string  == "West":
        return Directions.WEST


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    # print("Start:", problem.getStartState())
    # print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    # print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    "*** YOUR CODE HERE ***"

    # Initialise dfs fringe stack
    stack = util.Stack()
    visited = set()
    startState = problem.getStartState()
    stack.push((startState,[]))
    

    # DFS from start 
    while not stack.isEmpty():
        temp_node, path = stack.pop()
        visited.add(temp_node)

        if problem.isGoalState(temp_node):
            return path
                
        for successor in problem.getSuccessors(temp_node):
            if successor[0] not in visited:
                new_path = list(path) #create new copy since list is mutable and passed by ref
                new_path.append(successor[1])
                stack.push((successor[0], new_path))
                 
    

def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    # Initialise BFS fringe queue
    queue = util.Queue()
    visited = []
    startState = problem.getStartState()
    queue.push((startState,[]))
    visited.append(startState)

    # BFS from start 
    while not queue.isEmpty():
        temp_node, path = queue.pop()
        if problem.isGoalState(temp_node):
            return path
                
        for successor in problem.getSuccessors(temp_node):
            if successor[0] not in visited:
                new_path = list(path) #create new copy since list is mutable and passed by ref
                new_path.append(successor[1])
                queue.push((successor[0], new_path))
                visited.append(successor[0])

    
                

def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    # Initialise UCS fringe pq
    pq = util.PriorityQueue()
    visited = set()
    pq.push((problem.getStartState(), 0), 0) # distance of start from start is 0
    visited.add(problem.getStartState())
    
    
    successor_to_ancestor_map = {} #key = successor coordinates, value = (ancestor_coordinates, direction to successor, cost of moving from ancestor)

    # UCS from start 
    while not pq.isEmpty() :
        temp_node, cum_cost = pq.pop()
        
        if problem.isGoalState(temp_node):
            res = []
            while temp_node != problem.getStartState():
                ancestor, direction_from_ancestor, cost_from_ancestor = successor_to_ancestor_map[temp_node]
                temp_node = ancestor
                res.insert(0,direction_from_ancestor)
            return res

        for successor in problem.getSuccessors(temp_node):
         
            if successor[0] not in visited:
                pq.push((successor[0], cum_cost+successor[2]), cum_cost+successor[2])
                visited.add(successor[0])
                successor_to_ancestor_map[successor[0]] = (temp_node, successor[1], cum_cost+successor[2])
            
            # only update path of a visited node if the cost of getting there from another path is cheaper
            elif successor_to_ancestor_map.get(successor[0]) and successor_to_ancestor_map.get(successor[0])[2] > cum_cost+successor[2]:
                pq.push((successor[0], cum_cost+successor[2]), cum_cost+successor[2])
                successor_to_ancestor_map[successor[0]] = (temp_node, successor[1], cum_cost+successor[2])

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    #Initialise AStar priority queue
    pq = util.PriorityQueue()
    visited = []
    root_heuristics_cost = heuristic(problem.getStartState(), problem)
    root_state = (problem.getStartState(), 0, []) #(coordinates, path cost, path)
    pq_priority = 0 + root_heuristics_cost
    
    pq.push(root_state, pq_priority) 
   
    
    # A*Star from start 
    while not pq.isEmpty():
        temp_node, path_cost, path = pq.pop()
        
       
        if problem.isGoalState(temp_node):
            temp_node_heuristics = heuristic(temp_node, problem)
            return path

        if temp_node not in visited:
            visited.append(temp_node)
            for successor in problem.getSuccessors(temp_node):
                if successor[0] not in visited:
                    successor_heuristics_cost = heuristic(successor[0], problem)
                    pq_priority = path_cost + successor[2] + successor_heuristics_cost

                    new_path = list(path)
                    new_path.append(successor[1])
                    new_state = (successor[0], path_cost + successor[2], new_path)
                    pq.push(new_state, pq_priority)
             


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
