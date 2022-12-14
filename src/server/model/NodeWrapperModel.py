class NodeWrapper(object):
    def __init__(self, node, is_max, parent=None, curr_dist=0, pred_distance=0, elevation=0, route_path=None):
        self.id = node
        self.parent = parent
        self.curr_dist = curr_dist
        self.elevation = max(elevation, 0)
        self.route_path = route_path
        self.pred_dist = pred_distance
        self.is_max = is_max

    def __lt__(self, other):
        """Operation override for the less than or more than operation to compare two 
            objects of the same type, based on is_max parameter.

        Args:
            other: another object of the NodeWrapper, with which current object has to be compared

        Returns:
            A boolean representing if the current node is less than or more than the other node
        """
        if self.is_max:
            self_heuristic_dist = self.curr_dist + \
                (self.elevation * 15) - self.pred_dist
            other_heuristic_dist = other.curr_dist + \
                (other.elevation * 15) - other.pred_dist
            return self_heuristic_dist > other_heuristic_dist
        else:
            self_heuristic_dist = self.curr_dist + \
                (self.elevation * 15) + self.pred_dist
            other_heuristic_dist = other.curr_dist + \
                (other.elevation * 15) + other.pred_dist
            return self_heuristic_dist < other_heuristic_dist
